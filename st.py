from expression import ValType
from instruction import RegisterType
from err import addErr, ErrType

class Symbol():
    '''class that represents an abstracton of a symbol (a variable)'''
    def __init__(self, idn = None, typev = None, val = None):
        self.id = idn
        self.type = typev
        self.value = val

class SymbolTable():
    '''data struct to manage symbols'''
    def __init__(self, syms = {}):
        self.syms = syms

def getSymbol(idx,type_):
    '''given an index value and a register type
    looks for a value in the respective register'''
    if type_ == RegisterType.TVAR:
        if not idx in t_reg.syms:
            addErr(ErrType.SEMANTIC, "Error: t" + str(idx)+ " does not exists","")
        else:
            return t_reg.syms[idx]
    elif type_ == RegisterType.AVAR:
        if not idx in a_reg.syms:
            addErr(ErrType.SEMANTIC, "Error: a" + str(idx)+ " does not exists","")
        else:
            return a_reg.syms[idx]
    elif type_ == RegisterType.VVAR:
        if not idx in v_reg.syms:
            addErr(ErrType.SEMANTIC, "Error: v" + str(idx)+ " does not exists","")
        else:
            return v_reg.syms[idx]
    elif type_ == RegisterType.SVAR:
        if not idx in s_reg.syms:
            addErr(ErrType.SEMANTIC, "Error: s" + str(idx)+ " does not exists","")
        else:
            return s_reg.syms[idx]
    elif type_ == RegisterType.SPVAR:
        return sp_reg
    elif type_ == RegisterType.RVAR:
        return ra_reg
    return None
    
def findSymbol(idx,type_):
    '''look for a coincidence, returns de symbol if is there is one
    else returns none'''
    if type_ == RegisterType.TVAR:
        if idx in t_reg.syms:
            return t_reg.syms[idx]
    elif type_ == RegisterType.AVAR:
        if idx in a_reg.syms:
            return a_reg.syms[idx]
    elif type_ == RegisterType.VVAR:
        if idx in v_reg.syms:
            return v_reg.syms[idx]
    elif type_ == RegisterType.SVAR:
        if idx in s_reg.syms:
            return s_reg.syms[idx]
    elif type_ == RegisterType.SPVAR:
        return sp_reg
    elif type_ == RegisterType.RVAR:
        return ra_reg
    return None

def updateSymbol(idx, type_, sym):
    #create or update a symbol
    if type_ == RegisterType.TVAR:
        t_reg.syms[idx] = sym #update the symbol
    elif type_ == RegisterType.AVAR:
        a_reg.syms[idx] = sym
    elif type_ == RegisterType.VVAR:
        v_reg.syms[idx] = sym
    elif type_ == RegisterType.SVAR:
        s_reg.syms[idx] = sym
    elif type_ == RegisterType.SPVAR:
        if sym.type == ValType.INTEGER:
            sp_reg.value = sym.value    #updates the value
        else:
            addErr(ErrType.SEMANTIC, "Error: sp can't be " + str(sym.type)+ ". Only " + str(ValType.INTEGER),"")
    elif type_ == RegisterType.RVAR:
        if sym.type == ValType.INTEGER:
            ra_reg.value = sym.value
        else:
            addErr(ErrType.SEMANTIC, "Error: ra can't be " + str(sym.type)+ ". Only " + str(ValType.INTEGER),"")

def deleteSymbol(idx, type_):
    '''delete a symbol from the specified table'''
    if type_ == RegisterType.TVAR:
        del t_reg.syms[idx]
    elif type_ == RegisterType.AVAR:
        del a_reg.syms[idx]
    elif type_ == RegisterType.VVAR:
        del v_reg.syms[idx]
    elif type_ == RegisterType.SVAR:
        del s_reg.syms[idx]
    elif type_ == RegisterType.SPVAR:
        sp_reg.value = 0
    elif type_ == RegisterType.RVAR:
        ra_reg.value = 0

t_reg = SymbolTable({})
a_reg = SymbolTable({})
v_reg = SymbolTable({})
s_reg = SymbolTable({})
ra_reg = Symbol(None,ValType.INTEGER, 0)
sp_reg = Symbol(None,ValType.INTEGER, 0)