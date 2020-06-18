from instruction import Print, Unset, Exit, If, GoTo, Assignment, Label
from assign import solve_assign, solve_oper, solve_val
from PyQt5 import QtWidgets, QtGui, QtCore
from operation import ValExpression, OperationExpression
from expression import ValType
from st import t_reg,a_reg,v_reg,s_reg,ra_reg,sp_reg, Symbol, SymbolTable, getSymbol, deleteSymbol, createReport
from datetime import datetime
from err import addErr, ErrType

class Interpreter():
    #index to keep track of the index beign executed
    idx_debug = 0    
    def __init__(self,astTree,QtOutput,QtInput):
        self.astTree = astTree
        self.nextLabel = None
        self.labelDict = {}
        self.QtOutput = QtOutput
        self.QtInput = QtInput
        t_reg.syms.clear()
        a_reg.syms.clear()
        v_reg.syms.clear()
        s_reg.syms.clear()
        ra_reg.value = 0
        ra_reg.type = ValType.INTEGER
        sp_reg.value = 0
        sp_reg.type = ValType.INTEGER

    def checkLabel(self):
        '''This function filter all Label instances from
            astTree then proceeds to add those filtered elements
            to labelDict dictionary'''
        #It filters the indices and the object itself of all Labels instance of astTree
        labelList = [(i,lbl) for i,lbl in enumerate(self.astTree) if isinstance(lbl[0], Label)]
        #labelList looks like this:
        # [(index, [Label instance]),...]
        for i in labelList:
            # i is a tuple where index 0 is a index to use as key and 
            # index 1 is a value (a Label instance)
            if not i[1][0].name in self.labelDict:
                self.labelDict[i[1][0].name] = i[0]
            else:
                #if the Label's name already exists, an error pops up
                addErr(ErrType.SEMANTIC, "Error: The label '" + str(i[1][0].name) + "' already exists", i[1][0].row)
                return False
        return True

    def checkMain(self):
        '''
            This function checks if the first label name is main
        '''
        if not 'main' in self.labelDict or self.labelDict['main'] != 0:
            addErr(ErrType.SEMANTIC, "Error: 'main' label must be at the begging of the code", "")
            return False
        return True

    def run(self):
        '''
            This function start the execution of the code
        '''
        if not self.checkMain():
            return
        # this variable will work as a counter and 
        # will specify what position of the syntax tree is running
        now = datetime.now()
        cteTime = now.strftime("%H:%M:%S")
        self.QtOutput.appendPlainText("starting execution..." + cteTime+"\n")
        cte_i = self.labelDict['main'] + 1
        while(cte_i < len(self.astTree)):
            lenNode = len(self.astTree[cte_i])
            if lenNode == 1:
                objNode = self.astTree[cte_i][0]
                if isinstance(objNode, Exit):
                    #print("Execution ended")
                    break
                elif isinstance(objNode, Print):
                    var_Temp = None
                    #solve oper and print the result
                    if isinstance(objNode.oper, ValExpression):
                        #call solve_var, this function returns an instance of ValExpression
                        var_Temp = solve_val(objNode.oper)
                    elif isinstance(objNode.oper, OperationExpression):
                        #call solve_opr, this function return an instance of Symbol
                        var_Temp = solve_oper(objNode.oper) #returns Symbol
                    if (var_Temp.type != ValType.FLOAT and var_Temp.type != ValType.STRING and 
                    var_Temp.type != ValType.INTEGER and var_Temp.type != ValType.CHAR):
                        addErr(ErrType.SEMANTIC, "Error: cannot print an array", objNode.row)
                    else:
                        prevTxt = str(self.QtOutput.toPlainText())
                        prevTxt += str(var_Temp.value).replace('\\n','\n')
                        self.QtOutput.setPlainText(prevTxt)
                elif isinstance(objNode, Unset):
                    #will delete a symbol
                    assig = objNode.varn
                    s = getSymbol(assig.varName, assig.varType)
                    if s:
                        deleteSymbol(assig.varName,assig.varType)
                    else:
                        addErr(ErrType.SEMANTIC, "Error: can't unset variable", objNode.row)                    
                elif isinstance(objNode, GoTo):
                    #load the value for the key given by label's name
                    if not objNode.name  in self.labelDict:
                        addErr(ErrType.SEMANTIC, "Error: Label '"+objNode.name +"' does not exist", objNode.row)
                        break
                    cte_i = self.labelDict[objNode.name]
                elif isinstance(objNode, If):
                    #solve oper and if the result is not 0 then it will make a jump
                    var_Temp = None
                    #solve oper and make decision
                    if isinstance(objNode.oper, ValExpression):
                        #call solve_var, this function returns an instance of ValExpression
                        var_Temp = solve_val(objNode.oper)
                    elif isinstance(objNode.oper, OperationExpression):
                        #call solve_opr, this function return an instance of Symbol
                        var_Temp = solve_oper(objNode.oper) #returns Symbol
                    #var_Temp.value has to be an integer type
                    if not isinstance(var_Temp.value, int):
                        addErr(ErrType.SEMANTIC, "Error: If statment can't make decision upon the given operation", objNode.row)
                    elif (var_Temp.value != 0):
                        if not objNode.name in self.labelDict:
                            addErr(ErrType.SEMANTIC, "Error: Label '"+objNode.name +"' does not exist", objNode.row)
                            break
                        cte_i = self.labelDict[objNode.name]
            elif lenNode == 2:
                solve_assign(self.astTree[cte_i])
            #increment the counter
            cte_i += 1
        now = datetime.now()
        cteTime = now.strftime("%H:%M:%S")
        createReport()
        self.QtOutput.appendPlainText("execution ended " + cteTime +"\n")

    def restartSymbols(self):
        t_reg.syms.clear()
        a_reg.syms.clear()
        v_reg.syms.clear()
        s_reg.syms.clear()
        ra_reg.value = 0
        ra_reg.type = ValType.INTEGER
        sp_reg.value = 0
        sp_reg.type = ValType.INTEGER

    def drun(self):
        '''
            This function starts the debuggin
        '''
        if Interpreter.idx_debug >= 0 and Interpreter.idx_debug < len(self.astTree):
            lenNode = len(self.astTree[Interpreter.idx_debug])
            if lenNode == 1:
                objNode = self.astTree[Interpreter.idx_debug][0]
                if isinstance(objNode, Exit):
                    #print("Execution ended")
                    Interpreter.idx_debug = -1
                    return
                elif isinstance(objNode, Print):
                    var_Temp = None
                    #solve oper and print the result
                    if isinstance(objNode.oper, ValExpression):
                        #call solve_var, this function returns an instance of ValExpression
                        var_Temp = solve_val(objNode.oper)
                    elif isinstance(objNode.oper, OperationExpression):
                        #call solve_opr, this function return an instance of Symbol
                        var_Temp = solve_oper(objNode.oper) #returns Symbol
                    if (var_Temp.type != ValType.FLOAT and var_Temp.type != ValType.STRING and 
                    var_Temp.type != ValType.INTEGER and var_Temp.type != ValType.CHAR):
                        addErr(ErrType.SEMANTIC, "Error: cannot print an array", objNode.row)
                    else:
                        prevTxt = str(self.QtOutput.toPlainText())
                        prevTxt += str(var_Temp.value).replace('\\n','\n')
                        self.QtOutput.setPlainText(prevTxt)
                elif isinstance(objNode, Unset):
                    #will delete a symbol
                    assig = objNode.varn
                    s = getSymbol(assig.varName, assig.varType)
                    if s:
                        deleteSymbol(assig.varName,assig.varType)
                    else:
                        addErr(ErrType.SEMANTIC, "Error: can't unset variable", objNode.row)                    
                elif isinstance(objNode, GoTo):
                    #load the value for the key given by label's name
                    if not objNode.name  in self.labelDict:
                        addErr(ErrType.SEMANTIC, "Error: Label '"+objNode.name +"' does not exist", objNode.row)
                        Interpreter.idx_debug = -1
                        return
                    else:
                        Interpreter.idx_debug = self.labelDict[objNode.name]
                        #Attemps to put the cursor on the label
                        cursor = self.QtInput.textCursor()
                        match = str(objNode.name) + ":"
                        regex = QtCore.QRegExp(match)
                        idx = regex.indexIn(self.QtInput.toPlainText(),0)
                        cursor.setPosition(idx)
                        self.QtInput.setTextCursor(cursor)
                        #cursor.movePosition(QtGui.QTextCursor.StartOfLine)                
                elif isinstance(objNode, If):
                    #solve oper and if the result is not 0 then it will make a jump
                    var_Temp = None
                    #solve oper and make decision
                    if isinstance(objNode.oper, ValExpression):
                        #call solve_var, this function returns an instance of ValExpression
                        var_Temp = solve_val(objNode.oper)
                    elif isinstance(objNode.oper, OperationExpression):
                        #call solve_opr, this function return an instance of Symbol
                        var_Temp = solve_oper(objNode.oper) #returns Symbol
                    #var_Temp.value has to be an integer type
                    if not isinstance(var_Temp.value, int):
                        addErr(ErrType.SEMANTIC, "Error: If statment can't make decision upon the given operation", objNode.row)
                    elif (var_Temp.value != 0):
                        if not objNode.name in self.labelDict:
                            addErr(ErrType.SEMANTIC, "Error: Label '"+objNode.name +"' does not exist", objNode.row)
                            Interpreter.idx_debug = -1
                            return
                        else:
                            Interpreter.idx_debug = self.labelDict[objNode.name]
                            #Attemps to put the cursor on the label
                            cursor = self.QtInput.textCursor()
                            match = str(objNode.name) + ":"
                            regex = QtCore.QRegExp(match)
                            idx = regex.indexIn(self.QtInput.toPlainText(),0)
                            cursor.setPosition(idx)
                            self.QtInput.setTextCursor(cursor)
            elif lenNode == 2:
                solve_assign(self.astTree[Interpreter.idx_debug])
            #increment the counter
            Interpreter.idx_debug += 1
            #moves the cursor
            self.QtInput.moveCursor(QtGui.QTextCursor.NextBlock, QtGui.QTextCursor.MoveAnchor)
        else:
            Interpreter.idx_debug = -1
            return