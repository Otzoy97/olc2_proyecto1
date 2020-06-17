from expression import ValType
from instruction import RegisterType
from err import addErr, ErrType
from datetime import datetime
from graphviz import Digraph

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

def createReport():
    lblDot = '<<table align="center" cellspacing="0" cellborder="1" border="0">\n'
    lblDot += "<tr><td colspan='5'> Symbols Table report </td> </tr>\n"
    lblDot += "<tr>\n<td>Id</td>\n<td>Type</td>\n<td>Value</td>\n<td>Dimension</td>\n<td>Ref.</td>\n</tr>\n"
    for i in t_reg.syms.values():
        dimen = ""
        if isinstance(i.value,dict):
            dimen = str(len(i.value))
        lblDot += "<tr>\n<td>t"+ str(i.id)+"</td>\n<td>" + str(i.type) +"</td>\n<td>"+ str(i.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    for i in a_reg.syms.values():
        dimen = ""
        if isinstance(i.value,dict):
            dimen = str(len(i.value))
        lblDot += "<tr>\n<td>a"+ str(i.id)+"</td>\n<td>" + str(i.type) +"</td>\n<td>"+ str(i.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    for i in v_reg.syms.values():
        dimen = ""
        if isinstance(i.value,dict):
            dimen = str(len(i.value))
        lblDot += "<tr>\n<td>v"+str(i.id)+"</td>\n<td>" + str(i.type) +"</td>\n<td>"+ str(i.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    for i in s_reg.syms.values():
        dimen = ""
        if isinstance(i.value,dict):
            dimen = str(len(i.value))
        lblDot += "<tr>\n<td>s"+ str(i.id)+"</td>\n<td>" + str(i.type) +"</td>\n<td>"+ str(i.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    dimen = ""
    if isinstance(ra_reg.value,dict):
        dimen = str(len(ra_reg.value))
    lblDot += "<tr>\n<td>ra</td>\n<td>" + str(ra_reg.type) +"</td>\n<td>"+ str(ra_reg.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    dimen = ""
    if isinstance(sp_reg.value,dict):
        dimen = str(len(sp_reg.value))
    lblDot += "<tr>\n<td>sp</td>\n<td>" + str(sp_reg.type) +"</td>\n<td>"+ str(sp_reg.value) +"</td>\n<td>"+dimen +"</td>\n<td></td>\n</tr>\n"
    now = datetime.now()
    fstr = now.strftime("%d%m%y-%H%M%S")
    lblDot += "<tr><td colspan='5'>"+fstr+"</td> </tr></table>>"
    g = Digraph(name="Symbols_table",node_attr={'shape':'plaintext', 'color':'gray'})
    g.node("d1", lblDot)
    try:
        g.render("Symbols table" + fstr,'report',False,True,'pdf')
    except Exception as e:
        print(e)

t_reg = SymbolTable({})
a_reg = SymbolTable({})
v_reg = SymbolTable({})
s_reg = SymbolTable({})
ra_reg = Symbol(None,ValType.INTEGER, 0)
sp_reg = Symbol(None,ValType.INTEGER, 0)