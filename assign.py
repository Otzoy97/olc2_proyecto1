from expression import ValType, Operator
from instruction import ValExpression, RegisterType
import operation
from st import Symbol, SymbolTable
from math import trunc
from PyQt5 import QtWidgets

t_reg = SymbolTable()
a_reg = SymbolTable()
v_reg = SymbolTable()
s_reg = SymbolTable()
ra_reg = Symbol()
sp_reg = Symbol()

def solve_val(i):
    '''This function returns a ValExpression'''
    if (i.type != ValType.REFVAR):
        #if is not a variable reference returns the ValExpression itself
        return i
    else: 
        #if is a variable reference, it look for a coincidence on any symbol table
        #then create a ValExpression with the raw value (and its type) and returns it
        # TODO: find a way to retrieve var values
        pass

def solve_assign(i):
    '''create a symbol'''
    #retrieve name 
    varName = i[0]
    #retrieve opr  
    varOpr = i[1] 
    #solve opr, returns a Symbol
    sym = solve_oper(varOpr)
    sym.id = varName
    if (varName.varType == RegisterType.TVAR):
        t_reg.update(sym)
    elif (varName.varType == RegisterType.VVAR):
        v_reg.update(sym)
    elif (varName.varType == RegisterType.AVAR):
        a_reg.update(sym)
    elif (varName.varType == RegisterType.SVAR):
        s_reg.update(sym)
    elif (varName.varType == RegisterType.SPVAR):
        sp_reg.val = sym.val
        sp_reg.type = sym.type
    elif (varName.varType == RegisterType.RVAR):
        ra_reg.val = sym.val
        ra_reg.type = sym.type

def solve_oper(i):
    if i.op == Operator.PLUS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            return Symbol(None, ValType.STRING, str(opl.value) + str(opr.value))
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value + opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value + opr.value))
        else:
            print("Semantic error: can't add these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.MINUS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't substract strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value - opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value - opr.value))
        else:
            print("Semantic error: can't substract these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.TIMES:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't multiply strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value * opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value * opr.value))
        else:
            print("Semantic error: can't multiply these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.QUOTIENT:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't divide strings %d", i.row)
            return Symbol(None, ValType.FLOAT, 0.0)
        elif any(i is ValType.INTEGER or ValType.FLOAT or ValType.CHAR for i in typear):
            if opr.value == 0:
                print("Semantic error: division by zero")
                return Symbol(None, ValType.FLOAT, 0.0)
            else:
                return Symbol(None, ValType.FLOAT, opl.value / opr.value)
        else:
            print("Semantic error: can't divide these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.REMAINDER:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't get remainder from strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            if opr.value == 0:
                print("Semantic error: division by zero")
                return Symbol(None, ValType.FLOAT, 0.0)
            else:
                return Symbol(None, ValType.FLOAT, float(opl.value % opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            if opr.value == 0:
                print("Semantic error: division by zero")
                return Symbol(None, ValType.INTEGER, 0)
            else:
                return Symbol(None, ValType.INTEGER, int(opl.value % opr.value))
        else:
            print("Semantic error: can't get remainder of these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NEGATIVE:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            print("Semantic error: can't get a negative value from string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.FLOAT:
            return Symbol(None, ValType.FLOAT, float(opl.value*-1))
        elif (opl.type == ValType.INTEGER or  opl.type == ValType.CHAR) :
            return Symbol(None, ValType.INTEGER, int(opl.value*-1))
        else:
            print("Semantic error: can't a negative value of this operand %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.ABS:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            print("Semantic error: can't get absolute value from string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.FLOAT:
            return Symbol(None, ValType.FLOAT, abs(opl.value))
        elif opl.type == ValType.INTEGER:
            return Symbol(None, ValType.INTEGER, abs(opl.value))
        elif opl.type == ValType.CHAR:
            return Symbol(None, ValType.CHAR, opl.value)
        else:
            print("Semantic error: Can't get absolute value from this operand %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NOT:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            print("Semantic error: can't negate a string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.INTEGER or opl.type == ValType.CHAR or opl.type == ValType.FLOAT:
            temp = 0 if opl.value != 0 else 1
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't negate this operand %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.AND:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't compare strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            return Symbol(None, ValType.INTEGER, tmpl and tmpr)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.XOR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't compare strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            tmpl_n = 0 if opl.value != 0 else 1
            tmpr_n = 0 if opl.value != 0 else 1
            return Symbol(None, ValType.INTEGER, (tmpl and tmpr_n)  or (tmpl_n and tmpr))
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.OR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't compare strings %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            return Symbol(None, ValType.INTEGER, tmpl or tmpr)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NOTBW:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            print("Semantic error: can't negate a string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        else:
            temp = ~int(opl.value)
            return Symbol(None, ValType.INTEGER, temp)
    elif i.op == Operator.ANDBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use and-bitwise on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) & int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.ORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use or-bitwise on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) | int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.XORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use xor-bitwise on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) ^ int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.SHL:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use shift-left on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) << int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.SHR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use shift-right on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) >> int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.EQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        tmp = 1 if (opl.value == opr.value) else 0
        return Symbol(None, ValType.INTEGER, temp)7
    elif i.op == Operator.NEQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        tmp = 1 if (opl.value != opr.value) else 0
        return Symbol(None, ValType.INTEGER, temp)
    elif i.op == Operator.GR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use 'greater than' on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value > opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.GRE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use 'greater than or equal' on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value >= opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.LS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use 'less than' on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value < opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.LSE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            print("Semantic error: can't use 'less than or equal' on string %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value <= opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            print("Semantic error: Can't compare these operands %d", i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.AMP:
        # stores de whole object (name, typeval, array access)
        return Symbol(None, ValType.POINTER, i)
    elif (i.op == Operator.CINT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.INTEGER, 0)
        if opr.type == ValType.CHAR:        r.val = int(opr.value)
        elif opr.type == ValType.STRING:    r.val = ord(getFirst(opr.value)) % 256
        elif opr.type == ValType.FLOAT:     r.val = trunc(opr.value)
        elif opr.type == ValType.INTEGER:   r.val = opr.value
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to int ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = ord(tmp) % 256
            elif isinstance(tmp, float):    r.val = trunc(tmp)
            elif isinstance(tmp, int):      r.val = tmp
            else:                           print(opr.type, ' cannot cast to int', i.row)
        elif opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to int ', i.row)
        else:
            print("Semantic error: Can't cast this operand %d", i.row)
        return r
    elif (i.op == Operator.CFLOAT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.FLOAT, 0)
        if opr.type == ValType.CHAR:        r.val = float(opr.value)
        elif opr.type == ValType.STRING:    r.val = float(ord(getFirst(opr.value)) % 256)
        elif opr.type == ValType.FLOAT:     r.val = opr.value
        elif opr.type == ValType.INTEGER:   r.val = float(opr.value)
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to float ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = float(ord(tmp) % 256)
            elif isinstance(tmp, float):    r.val = tmp
            elif isinstance(tmp, int):      r.val = float(tmp)
            else:                           print(opr.type, ' cannot cast to float', i.row)
        elif opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to float ', i.row)
        else:
            print("Semantic error: Can't cast this operand %d", i.row)
        return r
    elif (i.op == Operator.CCHAR):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:        r.val = abs(opr.value)
        elif opr.type == ValType.STRING:    r.val = abs(ord(getFirst(opr.value)) % 256)
        elif opr.type == ValType.FLOAT:     r.val = abs(trunc(opr.value) % 256)
        elif opr.type == ValType.INTEGER:   r.val = abs(opr.value % 256)
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to char ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = abs(ord(getFirst(opr.value)) % 256)
            elif isinstance(tmp, float):    r.val = abs(trunc(opr.value) % 256)
            elif isinstance(tmp, int):      r.val = abs(float(tmp))
            else:                           print(opr.type, ' cannot cast to char', i.row)
        elif opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to char ', i.row)
        else:
            print("Semantic error: Can't cast this operand %d", i.row)
        return r
    elif i.op == Operator.READ:
        # shows an input box and save a string
        # creates an string symbol
        r = Symbol(None, ValType.STRING, "")
        txt, msg = QtWidgets.QInputDialog.getText(None, 'Read')
        if msg:
            r.val = txt
        return r
    elif i.op == Operator.ARRAY:
        # creates an array symbol
        r = Symbol(None,ValType.ARRAY,None)
        return r

def getFirst(arr):
    try:
        if isinstance(arr, list):  getFirst(arr[0])
        elif isinstance(arr, str): return arr[0]
        elif isinstance(arr, dict):
            print("Can't access through dictionary struct")
        else:
            print("Can't access through unknown data structure")
    except: return 0



