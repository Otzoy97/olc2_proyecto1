from expression import ValType, Operator
from instruction import ValExpression, RegisterType
import operation
from st import Symbol, SymbolTable, getSymbol, updateSymbol
from math import trunc
from PyQt5 import QtWidgets

def solve_val(i):
    '''This function returns a ValExpression'''
    if (i.type != ValType.REFVAR):
        #if is not a variable reference returns the ValExpression itself
        return i
    else: 
        #if is a variable reference, it looks for a coincidence on any symbol table
        #then create a ValExpression with the raw value (and its type) and returns it
        assign_instance = i.value
        #gets an array access
        arrAccess = None if (assign_instance.valExp == None) else createIdxCol(assign_instance.valExp)
        #gets a symbol
        symb_FromAssign = getSymbol(assign_instance.varName, assign_instance.varType)
        if symb_FromAssign == None:
            #There was not symbol returned
            #return a 0 integer value
            return ValExpression(0, ValType.INTEGER)
        else:
            #There was a symbol returned
            #is a pointer? -> solved the pointer
            if(symb_FromAssign.type == ValType.POINTER):
                symb_FromAssign = solve_pointer(symb_FromAssign)
                if (arrAccess != None):
                    #It is necesary to travel through the given symbol value
                    r = throughDict(symb_FromAssign.val, arrAccess)
                    if r == None:
                        return Symbol(None, ValType.INTEGER, 0)
                    else:
                        return ValExpression(r.val, r.type)
                else:
                    return ValExpression(symb_FromAssign.val, symb_FromAssign.type)
            #is an array? -> access through array
            elif(symb_FromAssign.type == ValType.ARRAY or symb_FromAssign.type == ValType.STRUCT):
                if (arrAccess != None):
                    #It is necesary to travel through the given symbol value
                    r = throughDict(symb_FromAssign.val, arrAccess)
                    if r == None:
                        return Symbol(None, ValType.INTEGER, 0)
                    else:
                        return ValExpression(r.val, r.type)
                else:
                    return ValExpression(symb_FromAssign.val, symb_FromAssign.type)
            else:
                #perhaps is a integer, string, float or a char
                return ValExpression(symb_FromAssign.val, symb_FromAssign.type)
            
def createIdxCol(col = []):
    '''create an array from the array returned by the parser in Assignment.valExp'''
    rcol = []
    for i in col:
        if isinstance(i, str):
            rcol.append(str(i))
        elif isinstance(i, int):
            rcol.append(int(i))
        elif isinstance(i, Assignment):
            #look for a symbol
            syym = getSymbol(i.varName,i.varType)
            if (syym != None):
                #a symbol was returned
                syym = solve_pointer(syym)
                if isinstance(syym.val, int) or isinstance(syym.val, str) :
                    rcol.append(syym.val)
                else:
                    print("Semantic error: unabled to retrieve value from ", str(i.varType), " ", str(i.varName))    
                    return None
            else:
                #a symbol was not returned, so the var does not exist
                print("Semantic error: the variable does not exists ", str(i.varType), " ", str(i.varName))
                #return a None value
                return None
    return rcol

def solve_pointer(sym):
    '''takes a symbol and finds out if it's a pointer
        if is, look for a reference in the symbol table
        else, returns the symbol 'sym'
        On erro returns an integer symbol with value 0'''
    if sym.ValType == ValType.POINTER:
        #Gets the assignment value
        valSym = sym.val
        #gets an array access
        arrAccess = None if (valSym.valExp == None) else createIdxCol(valSym.valExp)
        #Gets the Symbol referenced
        valSym = getSymbol(valSym.varName, valSym.varType)
        #Checks if valSymm is not None
        if valSym != None:
            #Checks if arrAccess is not None
            if arrAccess == None:
                #There is no need to travel through the given symbol value
                #Checks again if valSym is a pointer
                return solve_pointer(valSym)
            else:
                #It is necesary to travel through the given symbol value
                r = throughDict(valSym.val,arrAccess)
                if r == None:
                    return Symbol(None,ValType.INTEGER,0)
                else:
                    return r
        else:
            print("Semantic error: unable reference ",str(valSym.varType), " ", str(valSym.varName))
            return Symbol(None,ValType.INTEGER,0)
    else:
        return sym

def throughDict(dic, idxcol = []):
    '''travels through a given symbol
        if theres is an error, returns None
        else, returns a Symbol'''
    tmp = dic
    try:
        for i in idxcol:
            if isinstance(tmp, dict):
                if not i in tmp:
                    print("Semantic error: given index value doesn't exist")
                else:
                    tmp = tmp[i]
            elif isinstance(tmp, str):
                if len(tmp) < i:
                    return Symbol(None,ValType.STRING,tmp[i])
                else:
                    print("Semantic error: index out of border")
                    return None
            else:
                print("Semantic error: can't access through array to given Symbol")
                return None
        # symbol about to be returned
        if isinstance(tmp, str):
            return Symbol(None,ValType.STRING,tmp)
        elif isinstance(tmp, float):
            return Symbol(None,ValType.FLOAT,tmp)
        elif isinstance(tmp, int):
            return Symbol(None,ValType.INTEGER,tmp)
        else:
            print("Semantic error: unknown value found in array")
    except:
        print("Semantic error: can't access through array")
    return None

def solve_assign(i):
    '''create a symbol'''
    #retrieve name 
    #TODO: FINISH THE CREATE AND ASSIGNMENT
    varName = i[0] #assignment instance
    #retrieve opr  
    varOpr = i[1] #operationexpression instance
    #solve opr, returns a Symbol
    sym = Symbol(varName,None,None)
    if isinstance(varOpr, ValExpression):
        tmp = solve_val(varOpr) #returns ValExpression
        sym.type = tmp.type
        sym.val = tmp.value
    elif isinstance(varOpr, OperationExpression):
        tmp = solve_oper(varOpr) #returns Symbol
        sym.type = tmp.type
        sym.val = tmp.val

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
        # checks if variable exist
        r = getSymbol(i.e1.varName, i.e1.varType)
        if (r != None):
            return Symbol(None, ValType.POINTER, i.e1)
        else:
            print("Semantic error: can't use & on ",str(i.e1.varType), " ", str(i.e1.varName))
            return Symbol(None, ValType.INTEGER, 0)
    elif (i.op == Operator.CINT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.INTEGER, 0)
        if opr.type == ValType.CHAR:        r.val = int(opr.value)
        elif opr.type == ValType.STRING:    r.val = ord(opr.value[0])
        elif opr.type == ValType.FLOAT:     r.val = trunc(opr.value)
        elif opr.type == ValType.INTEGER:   r.val = opr.value
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to int ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = ord(tmp[0])
            elif isinstance(tmp, float):    r.val = trunc(tmp)
            elif isinstance(tmp, int):      r.val = tmp
            else:                           print(opr.type, ' cannot cast to int', i.row)
        elif opr.type == ValType.STRUCT:
            print("Semantic error: ",opr.type, ' cannot cast to int ', i.row)
        else:
            print("Semantic error: Can't cast this operand %d", i.row)
        return r
    elif (i.op == Operator.CFLOAT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.FLOAT, 0)
        if opr.type == ValType.CHAR:        r.val = float(opr.value)
        elif opr.type == ValType.STRING:    r.val = float(ord(opr.value[0]))
        elif opr.type == ValType.FLOAT:     r.val = opr.value
        elif opr.type == ValType.INTEGER:   r.val = float(opr.value)
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to float ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = float(ord(tmp[0]))
            elif isinstance(tmp, float):    r.val = tmp
            elif isinstance(tmp, int):      r.val = float(tmp)
            else:                           print(opr.type, ' cannot cast to float', i.row)
        elif opr.type == ValType.STRUCT:
            print("Semantic error: ",opr.type, ' cannot cast to float ', i.row)
        else:
            print("Semantic error: Can't cast this operand %d", i.row)
        return r
    elif (i.op == Operator.CCHAR):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:        r.val = abs(opr.value)
        elif opr.type == ValType.STRING:    r.val = abs(ord(opr.value[0]) % 256)
        elif opr.type == ValType.FLOAT:     r.val = abs(trunc(opr.value) % 256)
        elif opr.type == ValType.INTEGER:   r.val = abs(opr.value % 256)
        elif opr.type == ValType.POINTER:   
            print(opr.type, ' cannot cast to char ', i.row)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.val = abs(ord(opr.value[0]) % 256)
            elif isinstance(tmp, float):    r.val = abs(trunc(opr.value) % 256)
            elif isinstance(tmp, int):      r.val = abs(tmp)%256
            else:                           print(opr.type, ' cannot cast to char', i.row)
        elif opr.type == ValType.STRUCT:
            print("Semantic error: ",opr.type, ' cannot cast to char ', i.row)
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
        if isinstance(arr, dict):
            v_values = arr.values()
            v_it = iter(v_values)
            v_first = next(v_it)
            return getFirst(v_first)
        elif isinstance(arr, str): return arr
        elif isinstance(arr, float): return arr
        elif isinstance(arr, int): return arr
        else:
            print("Semantic error: Can't access through unknown data structure (a)")
    except: 
        print("Semantic error: Can't access through unknown data structure (b)")
        return 0
    return 0



