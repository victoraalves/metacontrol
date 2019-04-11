import pathlib
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QCompleter
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QBrush

from gui.views.py_files.mainwindow import *
from gui.calls.callsimulationtree import LoadSimulationTreeDialog, AliasEditorDelegate
from gui.models.data_storage import DataStorage
from gui.models.math_check import ValidMathStr, is_expression_valid


class MainWindow(QMainWindow):
    def __init__(self):
        # initialization
        self.streams_file = None  # for when the tree txt files are specified
        self.blocks_file = None

        # AbstractItem rows database initialization for tree view in load simulation variables dialog
        self.application_database = DataStorage()

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)

        # internal variables initialization
        self.sim_filename = ""

        # signal/socket connections
        self.ui.buttonOpenSimFile.clicked.connect(self.openSimFileDialog)
        self.ui.buttonLoadVariables.clicked.connect(self.openSimTreeDialog)
        self.ui.buttonAddExpr.clicked.connect(self.insertRowExpression)
        self.ui.tableWidgetExpressions.itemChanged.connect(self.expressionTableCheck)  # expression table changed event

        # some widget initializations
        self.ui.tableWidgetExpressions.setColumnWidth(1, 700)
        self._expr_name_delegate = AliasEditorDelegate()
        self._math_expr_delegate = ExpressionEditorDelegate(self.ui.tableWidgetAliasDisplay, self.application_database)
        self._expr_type_delegate = ComboxBoxExpressionTypeDelegate()
        self.ui.tableWidgetExpressions.setItemDelegateForColumn(0, self._expr_name_delegate)
        self.ui.tableWidgetExpressions.setItemDelegateForColumn(1, self._math_expr_delegate)
        self.ui.tableWidgetExpressions.setItemDelegateForColumn(2, self._expr_type_delegate)
        self.ui.tableWidgetAliasDisplay.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidgetSimulationData.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.ui.tabMainWidget.setTabEnabled(1, False)  # disable sampling tab

    # open simulation file
    def openSimFileDialog(self):
        homedir = str(pathlib.Path.home())  # home directory (platform independent)
        sim_filename, sim_filetype = QFileDialog.getOpenFileName(self, "Select .bkp simulation file", homedir,
                                                                 "BKP files (*.bkp);; Input files (*.inp)")

        if sim_filename == "" or (sim_filetype != "BKP files (*.bkp)" and sim_filetype != "Input files (*.inp)"):
            # user canceled the file dialog or selected invalid file
            if self.ui.textBrowserSimFile.styleSheet() != "color: blue":  # if there isn't an invalid path already
                self.ui.textBrowserSimFile.setText("Invalid or no file selected.")
                self.ui.textBrowserSimFile.setStyleSheet("color: red")
                self.ui.buttonLoadVariables.setEnabled(False)  # deactivate load button

        else:
            # it's a valid file. Set its path as string and color. Also make its filepath available to the ui
            self.sim_filename = sim_filename
            self.ui.textBrowserSimFile.setText(sim_filename)
            self.ui.textBrowserSimFile.setStyleSheet("")
            self.ui.buttonLoadVariables.setEnabled(True)  # deactivate load button

    # open simulationtree dialog
    def openSimTreeDialog(self):
        if self.sim_filename != "":
            dialog = LoadSimulationTreeDialog(self.sim_filename, self.application_database,
                                              streams_file_txt_path=self.streams_file,
                                              blocks_file_txt_path=self.blocks_file)

            if dialog.exec_():
                # the ok button was pressed, get the variables the user selected and update other ui items
                vars_list = [self.application_database.getInputTableData(),
                             self.application_database.getOutputTableData()]

                simulation_form_data = self.application_database.getSimulationDataDictionary()

                # -------------------------------- set the simulation form data --------------------------------
                self.ui.lineEditComponents.setText(str(len(simulation_form_data['components'])))
                self.ui.lineEditBlocks.setText(str(len(simulation_form_data['blocks'])))
                self.ui.lineEditStreams.setText(str(len(simulation_form_data['streams'])))
                self.ui.lineEditMethodName.setText(str(simulation_form_data['therm_method'][0]))
                self.ui.lineEditReactions.setText(str(len(simulation_form_data['reactions'])))
                self.ui.lineEditSensAnalysis.setText(str(len(simulation_form_data['sens_analysis'])))
                self.ui.lineEditCalculators.setText(str(len(simulation_form_data['calculators'])))
                self.ui.lineEditOptimizations.setText(str(len(simulation_form_data['optimizations'])))
                self.ui.lineEditDesSpecs.setText(str(len((simulation_form_data['design_specs']))))

                # -------------------------------- set alias table data --------------------------------
                alias_table_view = self.ui.tableWidgetAliasDisplay

                new_aliases_to_insert = []
                new_types_to_insert = []

                for input_row in vars_list[0]:
                    new_aliases_to_insert.append(input_row['Alias'])
                    new_types_to_insert.append(input_row['Type'])

                for output_row in vars_list[1]:
                    new_aliases_to_insert.append(output_row['Alias'])
                    new_types_to_insert.append("Candidate (CV)")

                num_rows_alias = alias_table_view.rowCount()

                if num_rows_alias != 0:  # alias table is not empty
                    alias_table_view.setRowCount(0)  # delete all the present rows

                for i in range(len(new_aliases_to_insert)):
                    alias_table_view.insertRow(i)

                    alias_table_item_name = QTableWidgetItem(new_aliases_to_insert[i])
                    alias_table_item_type = QTableWidgetItem(new_types_to_insert[i])

                    alias_table_item_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    alias_table_item_type.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

                    alias_table_item_name.setTextAlignment(Qt.AlignCenter)
                    alias_table_item_type.setTextAlignment(Qt.AlignCenter)

                    alias_table_view.setItem(i, 0, alias_table_item_name)
                    alias_table_view.setItem(i, 1, alias_table_item_type)

                # do a check of expressions
                self.expressionTableCheck()

                # -------------------------------- set the simulation info table data --------------------------------
                n_rows = len(simulation_form_data[max(simulation_form_data,
                                                      key=lambda x: len(set(simulation_form_data[x])))])
                siminfo_table = self.ui.tableWidgetSimulationData

                # clear the table
                siminfo_table.setRowCount(0)
                siminfo_table.setRowCount(n_rows)

                keys_list = [key for key in simulation_form_data.keys() if key != 'therm_method']
                for col in range(len(keys_list)):
                    for r in range(len(simulation_form_data[keys_list[col]])):
                        item = QTableWidgetItem(simulation_form_data[keys_list[col]][r])
                        item.setTextAlignment(Qt.AlignCenter)
                        siminfo_table.setItem(r, col, item)

    def insertRowExpression(self):
        expr_table_view = self.ui.tableWidgetExpressions
        last_row = expr_table_view.rowCount()
        expr_table_view.insertRow(last_row)

        table_expr_name = QtWidgets.QTableWidgetItem('expr_' + str(last_row))
        table_expr_name.setTextAlignment(Qt.AlignCenter)

        table_expr_item = QtWidgets.QTableWidgetItem('Type expression')
        table_expr_item.setForeground(QBrush(Qt.red))
        table_expr_item.setTextAlignment(Qt.AlignCenter)

        table_item_type = QtWidgets.QTableWidgetItem('Choose a type')
        table_item_type.setData(Qt.BackgroundRole, QBrush(Qt.red))

        expr_table_view.setItem(last_row, 0, table_expr_name)
        expr_table_view.setItem(last_row, 1, table_expr_item)
        expr_table_view.setItem(last_row, 2, table_item_type)

    # mock function to load tree from txt file
    def setTreeTxtFilesPath(self, streams_file, blocks_file):
        self.streams_file = streams_file
        self.blocks_file = blocks_file

    def expressionTableCheck(self):
        """
        Check if there are duplicated expression names, invalid names and undefined expression types. If everything is
        ok, enable the sampling tab, otherwise update the expression table information.
        """
        # check if there are duplicated aliases
        expr_table_view = self.ui.tableWidgetExpressions
        expr_model = expr_table_view.model()

        expr_info = []
        for row in range(expr_model.rowCount()):
            expr_info.append({'Name': expr_model.data(row, 0),
                              'Expr': expr_model.data(row, 1),
                              'Type': expr_model.data(row, 2)})

        is_name_duplicated = True if len([entry['Name'] for entry in expr_info]) != \
                                     len(set([entry['Name'] for entry in expr_info])) else False

        # TODO: (10/04/2019) Finish expression check (REMEMBER: only enable the sampling tab is expr table is not
        #  empty and valid


class ExpressionEditorDelegate(QtWidgets.QItemDelegate):

    def __init__(self, alias_table, gui_data, parent=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.alias_table = alias_table
        self.gui_data = gui_data

    def createEditor(self, parent, option, index):
        line_editor = QtWidgets.QLineEdit(parent)
        line_editor.setAlignment(Qt.AlignCenter)

        completer = QCompleter()
        line_editor.setCompleter(completer)

        model = QStringListModel()
        completer.setModel(model)
        completer.setFilterMode(Qt.MatchContains)

        # get aliases in display and set them to the completer
        vars_list = [self.gui_data.getInputTableData(),
                     self.gui_data.getOutputTableData()]
        if vars_list[0] is not None and vars_list[1] is not None:
            aliases_in_display = []

            aliases_in_display.extend([input_row[1] for input_row in vars_list[0]])
            aliases_in_display.extend([output_row[1] for output_row in vars_list[1]])

            model.setStringList(aliases_in_display)

        # insert the validator
        exp_validator = ValidMathStr(line_editor)
        line_editor.setValidator(exp_validator)

        return line_editor

    def setModelData(self, editor, model, index):
        text = editor.text()
        aliases_in_display = editor.completer().model().stringList()

        model.setData(index, text, Qt.EditRole)
        if is_expression_valid(text, aliases_in_display):
            model.setData(index, QBrush(Qt.green), Qt.ForegroundRole)
        else:
            model.setData(index, QBrush(Qt.red), Qt.ForegroundRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ComboxBoxExpressionTypeDelegate(QtWidgets.QItemDelegate):

    def createEditor(self, parent, option, index):
        combo_box = QtWidgets.QComboBox(parent)
        type_list = ["Objective function (J)", "Constraint function"]

        combo_box.addItems(type_list)

        return combo_box

    def setEditorData(self, combo_box, index):
        combo_box.showPopup()

    def setModelData(self, combo_box, model, index):
        value = combo_box.itemText(combo_box.currentIndex())

        model.setData(index, value, Qt.EditRole)
        original_backgrd_color = combo_box.palette().color(combo_box.backgroundRole())
        model.setData(index, QBrush(original_backgrd_color), Qt.BackgroundRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
