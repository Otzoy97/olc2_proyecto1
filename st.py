from expression import ValType
from instruction import RegisterType

class Symbol():
    '''class that represents an abstracton of a symbol (a variable)'''
    def __init__(self, idn = None, typev = None, val = None):
        self.id = idn
        self.type = typev
        self.val = val

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
    
def updateSymbol(sym):
    #remove the dollar symbol and 
    #the register type
    #only leaves the number
    #and that number is used as keyvalue
    if sym.id.find('t') != -1:
        t_reg.syms[sym.id] = sym #update the symbol
    elif sym.id.find('a') != -1:
        a_reg.syms[sym.id] = sym
    elif sym.id.find('v') != -1:
        v_reg.syms[sym.id] = sym
    elif sym.id.find('s') != -1:
        s_reg.syms[sym.id] = sym
    elif sym.id.find('sp') != -1:
        if sym.type == ValType.INTEGER:
            sp_reg.val = sym.val    #updates the value
            sp_reg.type = sym.type  #updates the type
        else:
            print("Semantic error: sp can't take ", str(sym.val), " as value, only ", sym(ValType.INTEGER))
    elif sym.id.find('ra') != -1:
        if sym.type == ValType.INTEGER:
            ra_reg.val = sym.val
            ra_reg.type = sym.type
        else:
            print("Semantic error: ra can't take ", str(sym.val), " as value", sym(ValType.INTEGER))

t_reg = SymbolTable()
a_reg = SymbolTable()
v_reg = SymbolTable()
s_reg = SymbolTable()
ra_reg = Symbol(None,ValType.INTEGER, 0)
sp_reg = Symbol(None,ValType.INTEGER, 0)