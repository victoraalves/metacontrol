import numpy as np
import pandas as pd
import pythoncom
import win32com.client
from py_expression_eval import Parser
from pydace.utils import lhsdesign
from PyQt5.QtCore import QObject, QThread, pyqtSignal
# import ptvsd

from surropt.caballero import Caballero, CaballeroOptions
from surropt.caballero.problem import CaballeroReport
from surropt.core.options.nlp import DockerNLPOptions

from gui.models.data_storage import DataStorage
from gui.models.sim_connections import AspenConnection


def lhs(n_samples: int, lb: list, ub: list, n_iter: int, inc_vertices: bool) \
        -> np.ndarray:
    lb = np.asarray(lb)
    ub = np.asarray(ub)

    return lhsdesign(n_samples, lb, ub, k=n_iter,
                     include_vertices=inc_vertices)


class SamplerThread(QThread):
    """
    Sampling thread that opens the aspen connection to keep the sampling
    assistant GUI responsive while the sampling is
    performed
    """

    case_sampled = pyqtSignal(int, object)

    def __init__(self, input_design_data: pd.DataFrame, app_data: DataStorage,
                 parent=None):
        QThread.__init__(self, parent)
        self._input_des_data = input_design_data
        self._app_data = app_data

        # https://stackoverflow.com/questions/26764978/using-win32com-with-multithreading
        # initialize
        pythoncom.CoInitialize()
        self._aspen_connection = AspenConnection(app_data.simulation_file)

        # create id
        self._aspen_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
            pythoncom.IID_IDispatch,
            self._aspen_connection.get_connection_object())

        # clean up
        self.finished.connect(self.__del__)

    def __del__(self):
        # kill the connection on thread cleanup
        self._aspen_connection.close_connection()

    def run(self):
        # initialize
        pythoncom.CoInitialize()

        # get instance from id
        aspen_con = win32com.client.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(
                self._aspen_id, pythoncom.IID_IDispatch)
        )

        input_vars = [{'var': row['Alias'], 'Path': row['Path']}
                      for row in self._app_data.input_table_data
                      if row['Type'] == 'Manipulated (MV)']

        output_vars = [{'var': row['Alias'], 'Path': row['Path']}
                       for row in self._app_data.output_table_data]

        for row in range(self._input_des_data.shape[0]):
            [var.update({'value': self._input_des_data.loc[row, var['var']]})
             for var in input_vars]
            self.case_sampled.emit(row + 1,
                                   run_case(input_vars, output_vars, aspen_con)
                                   )

            if self.isInterruptionRequested():  # to allow task abortion
                return


def run_case(mv_values: list, output_data: list, aspen_obj):
    """
    Samples a single case of DOE.

    Parameters
    ----------
    mv_values : list
        List containing all the design values to sample.
    output_data : list
        List containing all the output variables info to sample.
    aspen_obj : COM object
        Object connection handle.

    Returns
    -------
    dict
        Dictionary with output alias as keys and values as data sampled.
    """

    # get the paths to feed to the aspen obj
    for var in mv_values:
        aspen_obj.Tree.FindNode(var['Path']).Value = var['value']

    # run the engine
    aspen_obj.Engine.Run2()

    # get the output
    res_dict = {}
    UOSTAT2_val = aspen_obj.Tree.FindNode(
        r"\Data\Results Summary\Run-Status\Output\UOSSTAT2").Value
    if UOSTAT2_val == 8:
        res_dict['success'] = 'ok'
        for out_var in output_data:
            res_dict[out_var['var']] = aspen_obj.Tree.FindNode(
                out_var['Path']).Value
    else:
        res_dict['success'] = 'error'
        for out_var in output_data:
            res_dict[out_var['var']] = np.spacing(1)

    return res_dict


class SamplerWorker(QObject):

    def __init__(self, app_data: DataStorage,
                 marshalled_sim_id):
        self.app_data = app_data
        self.marshall_id = marshalled_sim_id
        # alias to index mapping of variables for easy access
        self.inp_aliases = {var['Alias']: idx for var, idx in
                            enumerate(self.app_data.input_table_data)}

    def sample_case(self, mv_values: dict):
        """Samples a single case based on values provided in `mv_values`.

        Parameters
        ----------
        mv_values : dict
            Dictionary where the keys are the aliases of the input variables
            and the values are the numeric values of each variable.
        """

        pythoncom.CoInitialize()
        aspen_obj = win32com.client.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(self.marshall_id,
                                                     pythoncom.IID_IDispatch)
        )

        # set input values
        for alias, value in mv_values.items():
            if alias in self.inp_aliases:
                # if the value exists in the input variables, set it in the
                # simulation
                row = self.app_data.input_table_data[self.inp_aliases[alias]]
                aspen_obj.Tree.FindNode(row['Path']).Value = value

        # get the output
        res_dict = {}
        UOSTAT2_val = aspen_obj.Tree.FindNode(
            r"\Data\Results Summary\Run-Status\Output\UOSSTAT2").Value
        if UOSTAT2_val == 8:
            res_dict['success'] = True
            for out_var in self.app_data.output_table_data:
                res_dict[out_var['Alias']] = aspen_obj.Tree.FindNode(
                    out_var['Path']).Value

        else:
            res_dict['success'] = False
            for out_var in self.app_data.output_table_data:
                res_dict[out_var['Alias']] = 1.0

        pythoncom.CoUninitialize()  # unmarshal the thread
        return res_dict


class ReportObject(CaballeroReport, QObject):
    iteration_printed = pyqtSignal(str)

    def __init__(self, terminal=False, plot=False):
        super().__init__(terminal=terminal, plot=plot)

    def print_iteration(self, movement, iter_count, x, f_pred, f_actual,
                        g_actual, header=False, color_font=None):
        # capture message from Report class and send it to the gui
        str_msg = super().print_iteration(movement, iter_count, x, f_pred,
                                          f_actual, g_actual, header=header,
                                          color_font=color_font)
        self.iteration_printed.emit(str_msg)
        return str_msg

    def get_results_report(self, index, r, x, f, lb, ub, fun_evals):
        res_msg = super().get_results_report(index, r, x, f, lb, ub, fun_evals)
        self.iteration_printed.emit(res_msg)
        return res_msg


class CaballeroWorker(QObject):
    opening_connection = pyqtSignal()
    connection_opened = pyqtSignal()
    optimization_finished = pyqtSignal()

    def __init__(self, app_data: DataStorage, params: dict,
                 report: ReportObject, parent=None):
        super().__init__(parent=parent)

        self.app_data = app_data
        self.params = params
        self.parser = Parser()
        self.report = report

    def __del__(self):
        if hasattr(self, 'asp_obj'):
            self.asp_obj.close_connection()

    def start_optimization(self):
        # ptvsd.debug_this_thread()
        params = self.params

        # unzip parameter data
        first_factor = params['first_factor']
        sec_factor = params['sec_factor']
        tol_contract = params['tol_contract']
        con_tol = params['con_tol']
        penalty = params['penalty']
        tol1 = params['tol1']
        tol2 = params['tol2']
        maxfunevals = params['maxfunevals']
        regrpoly = params['regrpoly']
        server_url = params['server_url']
        ipopt_tol = params['ipopt_tol']
        ipopt_max_iter = params['ipopt_max_iter']
        ipopt_con_tol = params['ipopt_con_tol']

        # setup the problem data
        inp_aliases = [var['Alias'] for var in self.app_data.input_table_data
                       if var['Type'] == 'Manipulated (MV)']
        con_aliases = [var['Alias']
                       for var in self.app_data.expression_table_data
                       if var['Type'] == 'Constraint function']
        obj_alias = [var['Alias']
                     for var in self.app_data.expression_table_data
                     if var['Type'] == 'Objective function (J)']

        doe = pd.DataFrame(self.app_data.doe_sampled_data)
        x = doe.loc[:, inp_aliases].to_numpy()
        g = doe.loc[:, con_aliases].to_numpy()
        f = doe.loc[:, obj_alias].to_numpy().flatten()

        # open the aspen connection
        self.open_connection()

        # define model function
        def model_fun(pt): return self.model_function(pt)

        # nlp bounds
        lb_list, ub_list = map(
            list, zip(*[(row['lb'], row['ub'])
                        for row in self.app_data.doe_mv_bounds])
        )

        # nlp options (assumes that the user already tested the connection)
        nlp_opts = DockerNLPOptions(name='nlp-server',
                                    server_url=server_url)

        # algorithm options
        cab_opts = CaballeroOptions(max_fun_evals=maxfunevals,
                                    feasible_tol=con_tol,
                                    penalty_factor=penalty,
                                    ref_tol=tol1, term_tol=tol2,
                                    first_factor=first_factor,
                                    second_factor=sec_factor,
                                    contraction_tol=tol_contract)

        opt_obj = Caballero(x=x, g=g, f=f, model_function=model_fun,
                            lb=lb_list, ub=ub_list, regression=regrpoly,
                            options=cab_opts, nlp_options=nlp_opts,
                            report_options=self.report)

        opt_obj.optimize()

        self.asp_obj.close_connection()

        self.optimization_finished.emit()

    def open_connection(self):
        # warn others that a simulation engine connection is about to be opened
        self.opening_connection.emit()

        pythoncom.CoInitialize()
        asp_obj = AspenConnection(self.app_data.simulation_file)
        self.asp_obj = asp_obj
        self._aspen_connection = asp_obj.get_connection_object()

        # emit the signal to warn others that the connection is done
        self.connection_opened.emit()

    def model_function(self, x):
        input_vars = [{'var': row['Alias'], 'Path': row['Path']}
                      for row in self.app_data.input_table_data
                      if row['Type'] == 'Manipulated (MV)']

        output_vars = [{'var': row['Alias'], 'Path': row['Path']}
                       for row in self.app_data.output_table_data]

        # update input values
        [var.update({'value': x[idx]}) for idx, var in enumerate(input_vars)]

        # query the simulation engine, store the results
        results = run_case(input_vars, output_vars, self._aspen_connection)

        # evaluate constraint and objective functions
        expr_values = {}
        parser = self.parser
        for expr in self.app_data.expression_table_data:
            expr_to_parse = parser.parse(expr['Expr'])
            var_list = expr_to_parse.variables()
            expr_values[expr['Alias']] = expr_to_parse.evaluate(results)

        # separate constraints values
        g = [expr_values[row['Alias']]
             for row in self.app_data.expression_table_data
             if row['Type'] == 'Constraint function']

        # objective function
        f = [expr_values[row['Alias']]
             for row in self.app_data.expression_table_data
             if row['Type'] == 'Objective function (J)']

        res = {
            'status': results['success'] == 'ok',
            'f': np.array(f).item(),
            'g': g,
            'extras': []
        }

        return res
