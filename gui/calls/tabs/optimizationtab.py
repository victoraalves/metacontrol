import pandas as pd
from PyQt5.QtCore import (QAbstractTableModel, QModelIndex, Qt, QThread,
                          pyqtSignal)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QHeaderView, QMessageBox, QWidget
from surropt.core.options.nlp import DockerNLPOptions
from win32com.client import Dispatch

from gui.models.data_storage import DataStorage
from gui.models.sampling import CaballeroWorker, ReportObject
from gui.views.py_files.caballerotab import Ui_Form


class ResultsTableModel(QAbstractTableModel):
    def __init__(self, results_frame: pd.DataFrame, parent=None):
        super().__init__(parent)
        self.df = results_frame

    def load_results(self, results_frame: pd.DataFrame):
        self.layoutAboutToBeChanged.emit()
        self.df = results_frame
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):
        return self.df.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):
        if self.df.empty:
            return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.df.columns[section]
            else:
                return self.df.index[section]

        elif role == Qt.FontRole:
            df_font = QFont()
            df_font.setBold(True)
            return df_font

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        else:
            return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or self.df.empty:
            return None

        row = index.row()
        col = index.column()

        value = self.df.iat[row, col]

        if role == Qt.DisplayRole:
            return str(value)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        else:
            return None


class OptimizationTab(QWidget):
    iteration_printed = pyqtSignal(str)
    opening_connection = pyqtSignal()
    connection_opened = pyqtSignal()

    def __init__(self, application_database: DataStorage, parent_tab=None):
        # ------------------------ Form Initialization ------------------------
        super().__init__()
        self.ui = Ui_Form()
        parent_tab = parent_tab if parent_tab is not None else self
        self.ui.setupUi(parent_tab)

        # ------------------------ Internal Variables -------------------------
        self.application_database = application_database

        # ----------------------- Widget Initialization -----------------------
        res_tab = self.ui.resultsTableView
        res_model = ResultsTableModel(results_frame=pd.DataFrame({}))
        res_tab.setModel(res_model)

        res_tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # disable abort button (for now, while surropt api does not implement)
        self.ui.abortOptPushButton.setEnabled(False)

        # --------------------------- Signals/Slots ---------------------------
        self.ui.startOptPushButton.clicked.connect(self.on_start_pressed)
        self.ui.ipoptTestConnectionPushButton.clicked.connect(
            self.on_ipopt_test_connection_pressed)

        # control panel related stuff
        self.opening_connection.connect(self.on_opening_sim_connection)
        self.connection_opened.connect(self.on_sim_connection_opened)
        self.iteration_printed.connect(self.on_iteration_printed)
        # ---------------------------------------------------------------------

    def on_start_pressed(self):
        # get caballero parameters from ui
        first_factor = float(self.ui.firstFactorLineEdit.text())
        sec_factor = float(self.ui.secondFactorLineEdit.text())
        tol_contract = float(self.ui.tolContractLineEdit.text())
        con_tol = float(self.ui.conTolLineEdit.text())
        penalty = float(self.ui.penaltyFactorLineEdit.text())
        tol1 = float(self.ui.tol1LineEdit.text())
        tol2 = float(self.ui.tol2LineEdit.text())
        maxfunevals = int(self.ui.maxFunEvalsLineEdit.text())
        regrpoly = self.ui.regrpolyComboBox.currentText()

        nlp_solver_type = self.ui.selectSolverComboBox.currentText()

        if nlp_solver_type == "IpOpt (local)":
            ipopt_tol = float(self.ui.ipoptLocalDualFeasLineEdit.text())
            ipopt_max_iter = int(self.ui.ipoptLocalMaxIterLineEdit.text())
            ipopt_con_tol = float(self.ui.ipoptLocalConTolLineEdit.text())
            nlp_dict = {'solver': "ipopt_local",
                        'ipopt_tol': ipopt_tol,
                        'ipopt_max_iter': ipopt_max_iter,
                        'ipopt_con_tol': ipopt_con_tol}

        elif nlp_solver_type == "IpOpt (server)":
            server_url = self.ui.ipoptServerAddressLineEdit.text()
            ipopt_tol = float(self.ui.ipoptLocalDualFeasLineEdit.text())
            ipopt_max_iter = int(self.ui.ipoptLocalMaxIterLineEdit.text())
            ipopt_con_tol = float(self.ui.ipoptLocalConTolLineEdit.text())
            nlp_dict = {'solver': "ipopt_server",
                        'server_url': server_url,
                        'ipopt_tol': ipopt_tol,
                        'ipopt_max_iter': ipopt_max_iter,
                        'ipopt_con_tol': ipopt_con_tol}

        else:
            raise ValueError("Invalid NLP solver selected.")

        params = {
            'first_factor': first_factor,
            'sec_factor': sec_factor,
            'tol_contract': tol_contract,
            'con_tol': con_tol,
            'penalty': penalty,
            'tol1': tol1,
            'tol2': tol2,
            'maxfunevals': maxfunevals,
            'regrpoly': regrpoly,
            'nlp_dict': nlp_dict
        }

        # disable ui elements
        self.ui.startOptPushButton.setEnabled(False)
        self.ui.regrpolyComboBox.setEnabled(False)
        self.ui.ipoptTestConnectionPushButton.setEnabled(False)

        # instantiate the optimization thread and worker
        self.opt_thread = QThread()
        self.opt_worker = CaballeroWorker(
            app_data=self.application_database,
            params=params,
            iteration_printed=self.iteration_printed,
            opening_connection=self.opening_connection,
            connection_opened=self.connection_opened
        )

        # worker signals connection
        self.opt_worker.results_ready.connect(self.on_opt_results_ready)

        # move the worker to another thread
        self.opt_worker.moveToThread(self.opt_thread)

        self.opt_worker.optimization_finished.connect(self.opt_thread.quit)
        self.opt_worker.optimization_finished.connect(
            self.on_optimization_finished)
        self.opt_thread.started.connect(self.opt_worker.start_optimization)

        # start the thread
        self.opt_thread.start()

    def on_opt_results_ready(self, report: dict):
        report = pd.DataFrame(report, index=['Values']).copy(deep=True)

        model = self.ui.resultsTableView.model()

        model.load_results(report)

    def on_optimization_finished(self):
        # enable ui elements
        self.ui.startOptPushButton.setEnabled(True)
        self.ui.regrpolyComboBox.setEnabled(True)
        self.ui.ipoptTestConnectionPushButton.setEnabled(True)

    def on_ipopt_test_connection_pressed(self):
        # tests the connection with the server specified in the UI
        srv_url = self.ui.ipoptAddressLineEdit.text()
        try:
            nlp_opts = DockerNLPOptions(name='test wsl', server_url=srv_url)
        except ValueError as con_err:
            # connection failed, inform the user
            fail_box = QMessageBox(QMessageBox.Critical, 'Connection failed!',
                                   str(con_err), buttons=QMessageBox.Ok,
                                   parent=None)
            fail_box.exec_()
        else:
            # connection succeed, let the user know it
            suc_box = QMessageBox(QMessageBox.Information, 'Connection OK!',
                                  'Connection to the ipopt was successful!',
                                  buttons=QMessageBox.Ok, parent=None)
            suc_box.exec_()

    def on_iteration_printed(self, iter_msg: str):
        self.ui.controlPanelTextBrowser.append(iter_msg)

    def on_opening_sim_connection(self):
        self.on_iteration_printed("Connecting to the simulation engine...\n")

    def on_sim_connection_opened(self):
        self.on_iteration_printed("Simulation engine connection successful!\n")


if __name__ == "__main__":
    import sys
    from gui.calls.base import my_exception_hook
    from tests_.mock_data import DOE_TAB_MOCK_DS

    app = QApplication(sys.argv)

    ds = DOE_TAB_MOCK_DS
    w = OptimizationTab(application_database=ds,
                        parent_tab=None)
    w.show()

    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())
