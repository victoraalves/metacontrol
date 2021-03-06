import numpy as np
import pandas as pd
from pydace import Dace
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QHeaderView
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QFont

from gui.models.data_storage import DataStorage
from gui.views.py_files.hessianextractiontab import Ui_Form
from gui.models.hessian_eval import hesscorrgauss
from gui.calls.dialogs.redspacemetamodel import ReducedSpaceMetamodelDialog
from gui.calls.dialogs.choleskymod import CholeskyDialog


class DiffTableModel(QAbstractTableModel):
    def __init__(self, app_data: DataStorage, parent: QTableView):
        QAbstractTableModel.__init__(self, parent)

        self.diff = pd.DataFrame()
        self.app_data = app_data

    def update_diff(self, diff: str):
        self.layoutAboutToBeChanged.emit()

        if diff == 'gy':
            self.diff = pd.DataFrame.from_dict(self.app_data.differential_gy)
        elif diff == 'gyd':
            self.diff = pd.DataFrame.from_dict(self.app_data.differential_gyd)
        elif diff == 'juu':
            self.diff = pd.DataFrame.from_dict(self.app_data.differential_juu)
        elif diff == 'jud':
            self.diff = pd.DataFrame.from_dict(self.app_data.differential_jud)
        else:
            raise ValueError('Invalid differential option.')

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self.diff.shape[0] if not self.diff.empty else 0

    def columnCount(self, parent=None):
        return self.diff.shape[1] if not self.diff.empty else 0

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):

        if self.diff.empty:
            return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.diff.columns[section]
            else:
                return self.diff.index[section]

        elif role == Qt.FontRole:
            df_font = QFont()
            df_font.setBold(True)
            return df_font

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        else:
            return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or self.diff.empty:
            return None

        row = index.row()
        col = index.column()

        value = self.diff.iat[row, col]

        if role == Qt.DisplayRole:
            return str(value)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        else:
            return None


class HessianExtractionTab(QWidget):
    def __init__(self, application_database: DataStorage, parent_tab=None):
        # ------------------------ Form Initialization ------------------------
        super().__init__()
        self.ui = Ui_Form()
        parent_tab = parent_tab if parent_tab is not None else self
        self.ui.setupUi(parent_tab)

        # ------------------------ Internal Variables -------------------------
        self.application_database = application_database

        # ----------------------- Widget Initialization -----------------------
        gy_table = self.ui.gyTableView
        gy_model = DiffTableModel(self.application_database, parent=gy_table)
        gy_table.setModel(gy_model)

        gy_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        gyd_table = self.ui.gydTableView
        gyd_model = DiffTableModel(self.application_database, parent=gyd_table)
        gyd_table.setModel(gyd_model)

        gyd_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        juu_table = self.ui.juuTableView
        juu_model = DiffTableModel(self.application_database, parent=juu_table)
        juu_table.setModel(juu_model)

        juu_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        jud_table = self.ui.judTableView
        jud_model = DiffTableModel(self.application_database, parent=jud_table)
        jud_table.setModel(jud_model)

        jud_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # --------------------------- Signals/Slots ---------------------------
        # differential data tables update
        # FIXME: this an ugly hack. Probably using a Signal Mapper is the right
        # way
        self.application_database.differential_gy_data_changed.connect(
            gy_model.update_diff
        )

        self.application_database.differential_gyd_data_changed.connect(
            gyd_model.update_diff
        )

        self.application_database.differential_juu_data_changed.connect(
            juu_model.update_diff
        )

        self.application_database.differential_jud_data_changed.connect(
            jud_model.update_diff
        )

        self.ui.genGradHessPushButton.clicked.connect(
            self.on_generate_grad_hess_pressed
        )

        self.ui.trainMetamodelPushButton.clicked.connect(
            self.on_reduced_space_metamodel_pressed
        )

        self.ui.cholmodPushButton.clicked.connect(
            self.on_cholesky_mod_pressed
        )
        # ---------------------------------------------------------------------

    def on_cholesky_mod_pressed(self):
        dialog = CholeskyDialog(self.application_database)
        dialog.exec_()

    def on_reduced_space_metamodel_pressed(self):
        dialog = ReducedSpaceMetamodelDialog(self.application_database)
        dialog.exec_()

    def on_generate_grad_hess_pressed(self):
        # get reduced space inputs from reduced theta data
        t_data = self.application_database.reduced_metamodel_theta_data
        X_labels = t_data.loc[:, 'Alias'].tolist()

        # sampled data
        sampled_data = self.application_database.reduced_doe_sampled_data

        G = self.get_differentials(X_labels, sampled_data, difftype='gradient')

        # split G in Gy and Gyd
        inps = self.application_database.input_table_data
        d_labels = inps.loc[inps['Type'] ==
                            self.application_database._INPUT_ALIAS_TYPES['d'],
                            'Alias'].tolist()

        u_labels = [label for label in X_labels if label not in d_labels]

        Gyd = G[d_labels]
        Gy = G[u_labels]

        self.application_database.differential_gy = Gy.to_dict(orient='dict')
        self.application_database.differential_gyd = Gyd.to_dict(orient='dict')

        # hessian
        J = self.get_differentials(X_labels, sampled_data, difftype='hessian')

        # split between juu and jud
        Jud = J.loc[u_labels, d_labels]
        Juu = J.loc[u_labels, u_labels]

        self.application_database.differential_juu = Juu.to_dict(orient='dict')
        self.application_database.differential_jud = Jud.to_dict(orient='dict')

    def get_differentials(self, X_labels: list, sampled_data: pd.DataFrame,
                          difftype: str):

        app_data = self.application_database
        t_data = app_data.reduced_metamodel_selected_data

        # get output data labels
        if difftype == 'gradient':
            Y_labels = t_data.loc[
                (t_data['Checked']) &
                (t_data['Type'] == app_data._OUTPUT_ALIAS_TYPES['cv']), 'Alias'
            ].tolist()
        else:
            Y_labels = t_data.loc[
                (t_data['Type'] == app_data._EXPR_ALIAS_TYPES['obj']), 'Alias'
            ].tolist()

        # extract data
        X = sampled_data.loc[
            (sampled_data['status'] == 'ok'),
            X_labels
        ].to_numpy()
        Y = sampled_data.loc[
            (sampled_data['status'] == 'ok'),
            Y_labels
        ].to_numpy()

        Y_dim = Y.shape[1] if Y.ndim > 1 else 1
        if len(Y_labels) == 1:
            # single variable, convert to column vector
            Y = Y.reshape(-1, 1)

        # regression model
        regr = self.application_database.differential_regression_model

        # correlation model
        corr = self.application_database.differential_correlation_model

        # theta and bounds values
        theta_data = app_data.reduced_metamodel_theta_data.set_index('Alias')

        theta0 = theta_data.loc[X_labels, 'theta0'].tolist()
        lob = theta_data.loc[X_labels, 'lb'].tolist()
        upb = theta_data.loc[X_labels, 'ub'].tolist()

        theta0 = np.asarray(theta0)
        lob = np.asarray(lob)
        upb = np.asarray(upb)

        # get nominal values
        # FIXME: implement better way to ensure order of MV's are correct
        doe_bnds = app_data.reduced_doe_d_bounds
        values = doe_bnds.loc[:, 'nominal'].tolist()
        x_nom = np.array([values])

        if difftype == 'gradient':
            # G dataFrame (Transposed because skogestad nomeclature)
            G = pd.DataFrame(columns=X_labels, index=Y_labels)

            # train the models
            for j in range(Y_dim):
                ph = Dace(regression=regr, correlation=corr)
                ph.fit(S=X, Y=Y[:, j], theta0=theta0, lob=lob, upb=upb)

                _, gy_ph, *_ = ph.predict(X=x_nom, compute_jacobian=True)

                for i in range(x_nom.size):
                    # store G values in the dataframe
                    G.at[Y_labels[j], X_labels[i]] = gy_ph[i, 0]

            return G
        else:
            # J dataFrame
            J = pd.DataFrame(columns=X_labels, index=X_labels)
            dmodel = Dace(regression=regr, correlation=corr)
            dmodel.fit(S=X, Y=Y, theta0=theta0, lob=lob, upb=upb)

            j_np = hesscorrgauss(x_nom, dmodel)
            for i in range(len(X_labels)):
                for j in range(len(X_labels)):
                    J.at[X_labels[i], X_labels[j]] = j_np[i, j]

            return J


if __name__ == "__main__":
    import sys
    from gui.calls.base import my_exception_hook
    from tests_.mock_data import REDSPACE_TAB_MOCK_DS

    app = QApplication(sys.argv)
    ds = REDSPACE_TAB_MOCK_DS
    w = HessianExtractionTab(application_database=ds)
    w.show()

    sys.excepthook = my_exception_hook
    sys.exit(app.exec_())
