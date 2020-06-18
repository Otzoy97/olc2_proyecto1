import sys
import codecs
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from QCodeEditor import QCodeEditor
from ascLexer import parse as ascParse, parser as ascParser, lexer as ascLexer
from descLexer import parse as descParse, parser as descParser, lexer as descLexer
from ascAST import createAST
from descAST import createASTD
import interpreter
from err import createReport, lexicArgs, semanticArgs, sintacticArgs, linesCount_, createReport
from st import t_reg, a_reg, v_reg, s_reg, sp_reg, ra_reg
import time

class Ui_augusApp(QtWidgets.QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__(None)
        self.setupUi()
        self.show()
        # reference to a file
        self.fileRef = ""
        self.fileSaved = False
        self.sT = None
        self.ascDebugger = None

    def setupUi(self):
        self.setObjectName("augusApp")
        self.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("augus.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        # -- ORGANIZADOR CENTRAL
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        # -- ORGANIZADOR INFERIOR
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        # -- TEXTO INDICANDO LA FILA ACTUAL EN EL TEXTO
        self.txtRow = QtWidgets.QLineEdit(self.centralwidget)
        self.txtRow.setEnabled(False)
        self.txtRow.setMinimumSize(QtCore.QSize(50, 0))
        self.txtRow.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtRow.setText("")
        self.txtRow.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtRow.setObjectName("txtRow")
        self.gridLayout_2.addWidget(self.txtRow, 0, 5, 1, 1)
        # -- ETIQUETA PARA LA COLUMNA DE TEXTO
        self.lblCol = QtWidgets.QLabel(self.centralwidget)
        self.lblCol.setTextFormat(QtCore.Qt.PlainText)
        self.lblCol.setWordWrap(False)
        self.lblCol.setObjectName("lblCol")
        self.gridLayout_2.addWidget(self.lblCol, 0, 2, 1, 1)
        # -- ETIQUETA PARA LA FILA DE TEXTO
        self.lblRow = QtWidgets.QLabel(self.centralwidget)
        self.lblRow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblRow.setTextFormat(QtCore.Qt.PlainText)
        self.lblRow.setObjectName("lblRow")
        self.gridLayout_2.addWidget(self.lblRow, 0, 4, 1, 1)
        # -- TEXTO INDICANDO LA COLUMNA ACTUAL EN EL TEXTO
        self.txtCol = QtWidgets.QLineEdit(self.centralwidget)
        self.txtCol.setEnabled(False)
        self.txtCol.setMinimumSize(QtCore.QSize(50, 0))
        self.txtCol.setMaximumSize(QtCore.QSize(200, 16777215))
        self.txtCol.setText("")
        self.txtCol.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txtCol.setObjectName("txtCol")
        self.gridLayout_2.addWidget(self.txtCol, 0, 3, 1, 1)
        # -- ETIQUETA QUE INDICA EL ESTADO ACTUAL DE LA APLICACION
        self.lblStatus = QtWidgets.QLabel(self.centralwidget)
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout_2.addWidget(self.lblStatus, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        # -- SEPERADOR INPUT/OUTPUT
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        # -- ENTRADA DE CODIGO
        self.txtInput = QCodeEditor(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtInput.setFont(font)
        self.txtInput.setObjectName("txtInput")
        self.txtInput.textChanged.connect(self.txtInputChanged_action)
        self.txtInput.cursorPositionChanged.connect(self.txtInputCursorPositionChanged_action)
        # -- SALIDA DE CODIGO (CMD)
        self.txtOutput =  QtWidgets.QPlainTextEdit(self.splitter)
        self.txtOutput.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtOutput.setFont(font)
        self.txtOutput.setUndoRedoEnabled(True)
        self.txtOutput.setObjectName("txtOutput")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        # -- BARRA DE MENÚ
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 962, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(self)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(self)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionUndo = QtWidgets.QAction(self)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(self)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtWidgets.QAction(self)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(self)
        self.actionPaste.setObjectName("actionPaste")
        self.actionFind = QtWidgets.QAction(self)
        self.actionFind.setObjectName("actionFind")
        self.actionReplace = QtWidgets.QAction(self)
        self.actionReplace.setObjectName("actionReplace")
        self.actionAbout = QtWidgets.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        #self.actionDark_Mode = QtWidgets.QAction(self)
        #self.actionDark_Mode.setCheckable(True)
        #self.actionDark_Mode.setObjectName("actionDark_Mode")
        self.actionAscendent_Debugging = QtWidgets.QAction(self)
        self.actionAscendent_Debugging.setObjectName("actionAscendent_Debugging")
        self.actionAscendent_Without_Debugging = QtWidgets.QAction(self)
        self.actionAscendent_Without_Debugging.setObjectName("actionAscendent_Without_Debugging")
        self.actionDescendent_Without_Debugging = QtWidgets.QAction(self)
        self.actionDescendent_Without_Debugging.setObjectName("actionDescendent_Without_Debugging")
        self.actionRestart_Debugging = QtWidgets.QAction(self)
        self.actionRestart_Debugging.setEnabled(False)
        self.actionRestart_Debugging.setObjectName("actionRestart_Debugging")
        self.actionStop_Debugging = QtWidgets.QAction(self)
        self.actionStop_Debugging.setEnabled(False)
        self.actionStop_Debugging.setObjectName("actionStop_Debugging")
        self.actionStep_Into = QtWidgets.QAction(self)
        self.actionStep_Into.setEnabled(False)
        self.actionStep_Into.setObjectName("actionStep_Into")
        self.actionContinue = QtWidgets.QAction(self)
        self.actionContinue.setEnabled(False)
        self.actionContinue.setObjectName("actionContinue")
        self.actionShowSymbolTable = QtWidgets.QAction(self)
        self.actionShowSymbolTable.setEnabled(False)
        self.actionShowSymbolTable.setObjectName("actionShowSymbolTable")
        self.actionGo_To = QtWidgets.QAction(self)
        self.actionGo_To.setObjectName("actionGo_To")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionReplace)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionGo_To)
        self.menuRun.addAction(self.actionAscendent_Debugging)
        self.menuRun.addAction(self.actionAscendent_Without_Debugging)
        self.menuRun.addAction(self.actionDescendent_Without_Debugging)
        self.menuRun.addSeparator()
        self.menuRun.addAction(self.actionRestart_Debugging)
        self.menuRun.addAction(self.actionStop_Debugging)
        self.menuRun.addAction(self.actionStep_Into)
        self.menuRun.addAction(self.actionContinue)
        self.menuRun.addAction(self.actionShowSymbolTable)
        #self.menuTools.addAction(self.actionDark_Mode)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        
        self.setWindowTitle("Augus 0.1 - fileName")
        self.lblCol.setText("Column")
        self.lblRow.setText("Row")
        self.lblStatus.setText("Not Saved")
        self.menuFile.setTitle("File")
        self.menuEdit.setTitle("Edit")
        self.menuRun.setTitle("Run")
        self.menuTools.setTitle("Tools")
        self.menuHelp.setTitle("Help")
        self.actionNew.setText("New")
        self.actionNew.setShortcut("Ctrl+N")
        self.actionOpen.setText("Open")
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionSave.setText("Save")
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave_As.setText("Save As")
        self.actionSave_As.setShortcut("Ctrl+Alt+S")
        self.actionExit.setText("Exit")
        self.actionUndo.setText("Undo")
        self.actionUndo.setShortcut("Ctrl+Z")
        self.actionRedo.setText("Redo")
        self.actionRedo.setShortcut("Ctrl+Y")
        self.actionCopy.setText("Copy")
        self.actionPaste.setText("Paste")
        self.actionCut.setText("Cut")
        self.actionCut.setText("Cut")
        self.actionCut.setShortcut("Ctrl+X")
        self.actionCopy.setText("Copy")
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionPaste.setText("Paste")
        self.actionPaste.setShortcut("Ctrl+V")
        self.actionFind.setText("Find")
        self.actionFind.setShortcut("Ctrl+F")
        self.actionReplace.setText("Replace")
        self.actionReplace.setShortcut("Ctrl+H")
        self.actionAbout.setText("About")
        #self.actionDark_Mode.setText("Dark Mode")
        self.actionAscendent_Debugging.setText("Ascendent Debugging")
        self.actionAscendent_Debugging.setShortcut("F5")
        self.actionAscendent_Without_Debugging.setText("Ascendent Without Debugging")
        self.actionAscendent_Without_Debugging.setShortcut("Ctrl+F5")
        self.actionDescendent_Without_Debugging.setText("Descendent Without Debugging")
        self.actionDescendent_Without_Debugging.setShortcut("Ctrl+Alt+F5")
        self.actionRestart_Debugging.setText("Restart Debugging")
        self.actionRestart_Debugging.setShortcut("Ctrl+Shift+F5")
        self.actionStop_Debugging.setText("Stop Debugging")
        self.actionStop_Debugging.setShortcut("Shift+F5")
        self.actionStep_Into.setText("Step Into")
        self.actionStep_Into.setShortcut("F11")
        self.actionContinue.setText("Continue")
        self.actionContinue.setShortcut("F6")
        self.actionShowSymbolTable.setText("Show Symbol Table")
        self.actionShowSymbolTable.setShortcut("Ctrl+T")
        self.actionGo_To.setText("Go To")
        self.actionGo_To.setShortcut("Ctrl+G")
        # -- File menu actions
        self.actionNew.triggered.connect(self.newFile_action)
        self.actionOpen.triggered.connect(self.openFile_action)
        self.actionSave.triggered.connect(self.saveFile_action)
        self.actionSave_As.triggered.connect(self.saveFileAs_action)
        self.actionExit.triggered.connect(self.close)
        # -- Edit menu actions
        self.actionGo_To.triggered.connect(self.goTo_action)
        # -- Run menu actions
        self.actionAscendent_Debugging.triggered.connect(self.ascendentDebug_action)
        self.actionAscendent_Without_Debugging.triggered.connect(self.ascendentRun_action)
        self.actionDescendent_Without_Debugging.triggered.connect(self.descendentRun_action)

        self.actionStop_Debugging.triggered.connect(self.stopDebug_action)
        self.actionContinue.triggered.connect(self.continue_action)
        self.actionRestart_Debugging.triggered.connect(self.restartDebug_action)
        self.actionStep_Into.triggered.connect(self.stepInto_action)
        self.actionShowSymbolTable.triggered.connect(self.showSymbolTable_action)
    
    def newFile_action(self):
        """Checks reference of actual file being edited. If it's saved then just clear the input text, if it isn't saveFile is called"""
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
            elif msg == QtWidgets.QMessageBox.Cancel:
                return
            self.txtInput.setPlainText("")
            self.setWindowTitle('Augus 0.1 - untitled')
            self.lblStatus.setText("Not saved")
            self.fileRef = ""
        else:
            self.txtInput.setPlainText("")
            self.setWindowTitle('Augus 0.1 - untitled')
            self.lblStatus.setText("Not saved")
            self.fileRef = ""

    def saveFile_action(self):
        """Checks the existence of a reference to a file. If there is one, then the file is uploaded, else saveFileAs is called"""
        # there is a file reference?
        if not self.fileRef.strip():
            # there is not -> call savefileas
            self.saveFileAs_action()
        else:
            # there is -> upload file
            with codecs.open(self.fileRef, 'w', encoding='utf8') as f:
                f.write(self.txtInput.toPlainText())
            self.fileSaved = True
            self.lblStatus.setText('Saved')
    
    def saveFileAs_action(self):
        """Shows a file dialog to save a file at a directory. Retrieve file name and puts it as a reference to a file"""
        #fileName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As', str(Path.home()), "Augus files (*.aug)")
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As', str(Path.home()))
        if fileName[0]:
            with codecs.open(fileName[0],'w', encoding='utf8') as f:
                f.write(self.txtInput.toPlainText())
            self.fileSaved = True
            self.lblStatus.setText('Saved')
            self.fileRef = fileName[0]
            self.setWindowTitle("Augus 0.1 - " + self.fileRef)

    def openFile_action(self):
        """Shows a file dialog to find a file. Retrieve file name and puts it as a reference to a file"""
        # call new file to verify if actual file is saved
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
            elif msg == QtWidgets.QMessageBox.Cancel:
                return
        #fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open', str(Path.home()), "Augus files (*.aug)")
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, 'Open', str(Path.home()))
        if fileName[0]:
            try:
                with codecs.open(fileName[0],'r', encoding='utf8') as f:
                    self.txtInput.setPlainText(f.read())
                self.fileSaved = True
                self.lblStatus.setText('Saved')
                self.fileRef = fileName[0]
                self.setWindowTitle("Augus 0.1 - " + self.fileRef)
            except:
                QtWidgets.QMessageBox.critical(self,"Error", "Couldn't open file")

    def goTo_action(self):
        """Shows a input dialog. The user must enter a number or a coordinate, then the cursor is settled on that row number or coordinate"""
        txt, msg = QtWidgets.QInputDialog.getText(
            self, 'Go To',
            'Type the row number or a coordinate (row,col)'
        )
        if msg:
            txt = txt.strip()
            txt = txt.split(",")
            try:
                # remove ending and starting spaces
                tRow = int(txt[0].strip()) 
                # tRow cannot be less than 1
                tRow = tRow if tRow > 0 else 1
                # if txt array lenght is greater then 1 -> cast to int stripped txt[1] 
                tCol = int(txt[1].strip()) if len(txt) > 1 else 1
                # input user of tCol cannot be less than 1
                tCol = tCol if tCol > 0 else 1
                doc = self.txtInput.document()
                n = doc.blockCount()
                if tRow > n:
                    # tRow is greater than number of lines in txtInput
                    # replace tRow actual value to number of lines in txtInput
                    # get index for line number
                    tRow = n - 1
                else:
                    # get index for vertical movement
                    tRow -= 1
                self.txtInput.setFocus()
                # create and set cursor for line number tRow
                cursor = QtGui.QTextCursor(doc.findBlockByLineNumber(tRow))
                # gets Textblock
                crBlock = cursor.block()
                # gets text's length on textblock
                lenBlock = len(crBlock.text())
                # if text's length is less than tCol then the cursor is set at the end of the line
                tCol = (tCol-1) if tCol <= lenBlock else (lenBlock)
                # move cursor to tCol
                cursor.movePosition(QtGui.QTextCursor.Right,QtGui.QTextCursor.MoveAnchor,tCol)
                # set cursor to txtInput
                self.txtInput.setTextCursor(cursor)
            except:
                QtWidgets.QMessageBox.critical(
                    self, "Error",
                    "It's not possible to go to the indicated position"
                )

    def ascendentRun_action(self):
        ascLexer.lineno = 1
        txt = self.txtInput.toPlainText()
        lexicArgs.clear()
        sintacticArgs.clear()
        semanticArgs.clear()
        # create the ast tree graph        
        createAST(txt)
        # create the ast tree execution
        astRunner = ascParse(txt)
        if(astRunner):
            # create an instance of interpreter
            run = interpreter.Interpreter(astRunner, self.txtOutput, self.txtInput)
            # checks the labels
            if (run.checkLabel()):
                #execute de ast tree
                run.run()
        createReport(self.txtInput.document().blockCount())
        ascParser.restart() 

    def descendentRun_action(self):
        descLexer.lineno = 1
        txt = self.txtInput.toPlainText()
        lexicArgs.clear()
        sintacticArgs.clear()
        semanticArgs.clear()
        #create the ast tree grpah
        createASTD(txt)
        #create the ast tree execution
        descRunner = descParse(txt)
        if (descRunner):
            run = interpreter.Interpreter(descRunner, self.txtOutput, self.txtInput)
            if (run.checkLabel()):
                run.run()
        createReport(self.txtInput.document().blockCount())
        descParser.restart()

    def ascendentDebug_action(self):
        '''start the execution step by step'''
        self.saveFile_action()
        self.lblStatus.setText("Debugging")
        #lexer and parser called
        ascLexer.lineno = 1
        txt = self.txtInput.toPlainText()
        lexicArgs.clear()
        sintacticArgs.clear()
        semanticArgs.clear()
        # create the ast tree graph        
        createAST(txt)
        # create the ast tree execution
        astRunner = ascParse(txt)
        if(astRunner):
            # create an instance of interpreter
            self.ascDebugger = interpreter.Interpreter(astRunner, self.txtOutput, self.txtInput)
            if (self.ascDebugger.checkLabel() and self.ascDebugger.checkMain()):  
                #shows the symbols table
                self.sT = SymbolsGrid(self)
                self.sT.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                self.sT.show()         
                #move the cursor at the begin of the text
                self.txtInput.moveCursor(QtGui.QTextCursor.Start,QtGui.QTextCursor.MoveAnchor)
                #block any posible edit
                self.txtInput.setReadOnly(True)
                self.txtInput.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                #restart index
                interpreter.Interpreter.idx_debug = 0
                #disable actions
                self.actionNew.setEnabled(False)
                self.actionOpen.setEnabled(False)
                self.actionAscendent_Debugging.setEnabled(False)
                self.actionAscendent_Without_Debugging.setEnabled(False)
                self.actionDescendent_Without_Debugging.setEnabled(False)
                #enable actions
                self.actionRestart_Debugging.setEnabled(True)
                self.actionStop_Debugging.setEnabled(True)
                self.actionStep_Into.setEnabled(True)
                self.actionContinue.setEnabled(True)
                self.actionShowSymbolTable.setEnabled(True)

    def restartDebug_action(self):
        '''restart the execution step by step'''
        #restart the debugger
        interpreter.Interpreter.idx_debug = 0
        self.ascDebugger.restartSymbols()
        self.sT.updateGrid()
        #enable edit
        self.txtInput.setReadOnly(False)
        self.txtInput.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        #move the cursor at the begin of the text
        self.txtInput.moveCursor(QtGui.QTextCursor.Start,QtGui.QTextCursor.MoveAnchor)
        #block any posible edit
        self.txtInput.setReadOnly(True)
        self.txtInput.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

    def stopDebug_action(self):
        self.lblStatus.setText("Saved")
        #create err reports
        createReport(self.txtInput.document().blockCount())
        try:
            ascParser.restart() 
        except:
            pass
        #move the cursor at the begin of the text
        self.txtInput.moveCursor(QtGui.QTextCursor.Start,QtGui.QTextCursor.MoveAnchor)
        #enable edit
        self.txtInput.setReadOnly(False)
        self.txtInput.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        #enable actions
        self.actionNew.setEnabled(True)
        self.actionOpen.setEnabled(True)
        self.actionAscendent_Debugging.setEnabled(True)
        self.actionAscendent_Without_Debugging.setEnabled(True)
        self.actionDescendent_Without_Debugging.setEnabled(True)
        #disable actions
        self.actionRestart_Debugging.setEnabled(False)
        self.actionStop_Debugging.setEnabled(False)
        self.actionStep_Into.setEnabled(False)
        self.actionContinue.setEnabled(False)
        self.actionShowSymbolTable.setEnabled(False)

    def stepInto_action(self):
        #enable edit
        self.txtInput.setReadOnly(False)
        self.txtInput.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.ascDebugger.drun()
        if interpreter.Interpreter.idx_debug < 0:
            #The execution has ended or an error ocurred
            self.stopDebug_action()
        else:
            #Fixs the cursor
            self.txtInputFixCursorDebug()
            #disable edit
            self.txtInput.setReadOnly(True)
            self.txtInput.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
            #update de symbols table
            self.sT.updateGrid()
            
    def continue_action(self):
        while interpreter.Interpreter.idx_debug != -1:
            self.stepInto_action()

    def showSymbolTable_action(self):
        '''show the symbol table'''
        try:
            self.sT.close()
        except:
            pass
        self.sT = SymbolsGrid(self)
        self.sT.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.sT.show()

    def txtInputFixCursorDebug(self):
        '''this function fixes the cursor position, puts the cursor at the beggining of the 
        first block with text'''
        while (True):
            txtcursor = self.txtInput.textCursor()
            #gets the text of the block in which the cursor is
            txtText = txtcursor.block().text().strip()
            if txtText and txtText[0] != '#':
                #there is something in that block and  
                # the first character isn't a #, so it isn't a commentary
                # leavs the loop
                break
            if  not self.txtInput.moveCursor(QtGui.QTextCursor.NextBlock, QtGui.QTextCursor.MoveAnchor):
                break

    def txtInputCursorPositionChanged_action(self):
        txtcursor = self.txtInput.textCursor()
        txtRow = txtcursor.blockNumber()
        txtCol = txtcursor.positionInBlock()
        self.txtCol.setText(str(txtCol+1))
        self.txtRow.setText(str(txtRow+1))
        pass
        
    def txtInputChanged_action(self):
        self.fileSaved = False
        self.lblStatus.setText("Not Saved")

    def closeEvent(self, event):
        if not self.fileSaved:
            msg = QtWidgets.QMessageBox.question(
                self,'New',
                'Do you want to save changes before?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
            if msg == QtWidgets.QMessageBox.Yes:
                self.saveFile_action()
                event.accept()
            elif msg == QtWidgets.QMessageBox.No:
                event.accept
            elif msg == QtWidgets.QMessageBox.Cancel:
                event.ignore()
    

class SymbolsGrid(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(SymbolsGrid, self).__init__(parent)
        self.setupUi()
        self.closeEvent
        self.installEventFilter(self)

    def setupUi(self):
        self.setObjectName("Form")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(640, 480)
        self.setModal(False)
        self.setMinimumSize(QtCore.QSize(640, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("augus.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.setWindowTitle("Symbols table")
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("Id.")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("Type")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("Value")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText("Dimension")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText("Ref.")

    def updateGrid(self):
        '''refresh the values on the symbols table'''
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(1)
        for i in t_reg.syms.values():
            rowpos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowpos)
            self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "t" + str(i.id)))
            self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(i.type)))
            self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(i.value)))
            dimen = ""
            if isinstance(i.value, dict):
                dimen = str(len(i.value))
            self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))
        for i in a_reg.syms.values():
            rowpos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowpos)
            self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "a" + str(i.id)))
            self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(i.type)))
            self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(i.value)))
            dimen = ""
            if isinstance(i.value, dict):
                dimen = str(len(i.value))
            self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))
        for i in v_reg.syms.values():
            rowpos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowpos)
            self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "v" + str(i.id)))
            self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(i.type)))
            self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(i.value)))
            dimen = ""
            if isinstance(i.value, dict):
                dimen = str(len(i.value))
            self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))
        for i in s_reg.syms.values():
            rowpos = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowpos)
            self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "s" + str(i.id)))
            self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(i.type)))
            self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(i.value)))
            dimen = ""
            if isinstance(i.value, dict):
                dimen = str(len(i.value))
            self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))
        dimen = ""
        if isinstance(ra_reg.value,dict):
            dimen = str(len(ra_reg.value))
        rowpos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowpos)
        self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "ra"))
        self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(ra_reg.type)))
        self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(ra_reg.value)))
        self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))
        dimen = ""
        if isinstance(sp_reg.value,dict):
            dimen = str(len(sp_reg.value))
        rowpos = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowpos)
        self.tableWidget.setItem(rowpos-1, 0,QtWidgets.QTableWidgetItem( "sp"))
        self.tableWidget.setItem(rowpos-1, 1,QtWidgets.QTableWidgetItem( str(sp_reg.type)))
        self.tableWidget.setItem(rowpos-1, 2,QtWidgets.QTableWidgetItem( str(sp_reg.value)))
        self.tableWidget.setItem(rowpos-1, 3,QtWidgets.QTableWidgetItem(dimen))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in (QtCore.Qt.Key_Return,
                QtCore.Qt.Key_Escape,
                QtCore.Qt.Key_Enter,):
                return True
        return super(SymbolsGrid, self).eventFilter(obj,event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    u = Ui_augusApp()
    sys.exit(app.exec_())


