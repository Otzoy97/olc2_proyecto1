from expression import ValType, Operator
from instruction import ValExpression, RegisterType
import operation
from st import Symbol, SymbolTable

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
        if ValType.STRING in typear:
            r = Symbol(None, ValType.STRING, str(opl) + str(opr))            
            pass
    elif i.op == Operator.MINUS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.TIMES:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.QUOTIENT:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.REMAINDER:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.NEGATIVE:
        opl = solve_val(i.e1)
        pass
    elif i.op == Operator.ABS:
        opl = solve_val(i.e1)
        pass
    elif i.op == Operator.NOT:
        opl = solve_val(i.e1)
        pass
    elif i.op == Operator.AND:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.XOR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.OR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.NOTBW:
        opl = solve_val(i.e1)
        pass
    elif i.op == Operator.ANDBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.ORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.XORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.SHL:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.SHR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.EQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.NEQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.GR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.GRE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.LS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.LSE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        pass
    elif i.op == Operator.AMP:
        opr = solve_val(i.e1)
        pass
    elif (i.op == Operator.CINT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:        r.val = int(opr.value)
        elif opr.type == ValType.STRING:    r.val = ord(getFirst(opr.value)) % 256
        elif opr.type == ValType.FLOAT:     r.val = float(opr.value)
        if opr.type == ValType.INTEGER:     r.val = opr.value
        elif opr.type == ValType.POINTER:   
            pass
        elif opr.type == ValType.ARRAY:     r.val = 
        if opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to char (')
        elif opr.type == ValType.STRING:
            pass
        return r
    elif (i.op == Operator.CFLOAT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:
            pass
        elif opr.type == ValType.STRING:
            pass
        elif opr.type == ValType.FLOAT:
            pass
        if opr.type == ValType.INTEGER:
            pass
        elif opr.type == ValType.POINTER:
            pass
        elif opr.type == ValType.ARRAY:
            pass
        if opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to char (')
        elif opr.type == ValType.STRING:
            pass
        return r
    elif (i.op == Operator.CCHAR):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:
            pass
        elif opr.type == ValType.STRING:
            pass
        elif opr.type == ValType.FLOAT:
            pass
        if opr.type == ValType.INTEGER:
            pass
        elif opr.type == ValType.POINTER:
            pass
        elif opr.type == ValType.ARRAY:
            pass
        if opr.type == ValType.STRUCT:
            print(opr.type, ' cannot cast to char (')
        elif opr.type == ValType.STRING:
            pass
        return r
    elif i.op == Operator.READ:
        pass
    elif i.op == Operator.ARRAY:
        pass

def getFirst(arr):
    try:
        if isinstance(arr, list):   getFirst(arr[0])
        elif isinstance(arr, str):

            return arr[0]
        else:
            return arr
    except Exception as e: return 0



