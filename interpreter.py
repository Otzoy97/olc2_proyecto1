from instruction import Print, Unset, Exit, If, GoTo, Assignment, Label
from assign import solve_assign, solve_oper, solve_val
from PyQt5 import QtWidgets
from operation import ValExpression, OperationExpression
from expression import ValType
from st import t_reg,a_reg,v_reg,s_reg,ra_reg,sp_reg, Symbol, SymbolTable
from datetime import datetime

class Interpreter():
    def __init__(self,astTree,QtOutpu):
        self.astTree = astTree
        self.nextLabel = None
        self.labelDict = {}
        self.QtOutput = QtOutpu
        global t_reg
        global a_reg
        global v_reg
        global s_reg
        global ra_reg
        global sp_reg
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
                print("Semantic error: The label '", i[1][0].name, "' already exists ", str(i[1][0].row))
                return False
        return True
    
    def run(self):
        '''
            This function checks if the first label name is main and start the execution
        '''
        if not 'main' in self.labelDict or self.labelDict['main'] != 0:
            print("Semantic error: 'main' label must be declared and must be at the start of the code")
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
                        print("Semantic errror: cannot print an array", objNode.row)
                    else:
                        prevTxt = str(self.QtOutput.toPlainText())
                        prevTxt += str(var_Temp.value).replace('\\n','\n')
                        self.QtOutput.setPlainText(prevTxt)
                elif isinstance(objNode, Unset):
                    #will delete a symbol or a position in array
                    pass
                elif isinstance(objNode, GoTo):
                    #load the value for the key given by label's name
                    if not objNode.name  in self.labelDict:
                        print("Semantic error: ",objNode.name ," does not exist")
                        return
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
                        print("Semantic error: if statement can't make decisions upon the given operation ", str(objNode.row))
                    elif (var_Temp.value != 0):
                        if not objNode.name in self.labelDict:
                            print("Semantic error: ",objNode.name ," does not exist")
                            return
                        cte_i = self.labelDict[objNode.name]
            elif lenNode == 2:
                solve_assign(self.astTree[cte_i])
            #increment the counter
            cte_i += 1
        now = datetime.now()
        cteTime = now.strftime("%H:%M:%S")
        self.QtOutput.appendPlainText("execution ended " + cteTime +"\n")
