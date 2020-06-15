from expression import ValType
from instruction import RegisterType

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

    #def add(self, sym):
    #    self.syms[sym.id] = sym

def getSymbol(idx,type_):
    '''given an index value and a register type
    looks for a value in the respective register'''
    if type_ == RegisterType.TVAR:
        if not idx in t_reg.syms:
            print("Semantic error: t%d does not exists", idx)
        else:
            return t_reg.syms[idx]
    elif type_ == RegisterType.AVAR:
        if not idx in a_reg.syms:
            print("Semantic error: a%d does not exists", idx)
        else:
            return a_reg.syms[idx]
    elif type_ == RegisterType.VVAR:
        if not idx in v_reg.syms:
            print("Semantic error: v%d does not exists", idx)
        else:
            return v_reg.syms[idx]
    elif type_ == RegisterType.SVAR:
        if not idx in s_reg.syms:
            print("Semantic error: s%d does not exists", idx)
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
        if type_ == ValType.INTEGER:
            sp_reg.value = sym.val    #updates the value
            sp_reg.type = sym.type  #updates the type
        else:
            print("Semantic error: sp can't take ", str(sym.val), " as value, only ", sym(ValType.INTEGER))
    elif type_ == RegisterType.RVAR:
        if type_ == ValType.INTEGER:
            ra_reg.value = sym.val
            ra_reg.type = sym.type
        else:
            print("Semantic error: ra can't take ", str(sym.val), " as value", sym(ValType.INTEGER))

t_reg = SymbolTable()
a_reg = SymbolTable()
v_reg = SymbolTable()
s_reg = SymbolTable()
ra_reg = Symbol(None,ValType.INTEGER, 0)
sp_reg = Symbol(None,ValType.INTEGER, 0)