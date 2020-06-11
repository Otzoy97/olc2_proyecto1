from expression import ValType

class Symbol():
    '''class that represents an abstracton of a symbol (a variable)'''
    def __init__(self, id = None, type = None, val = None):
        self.id = id
        self.type = type
        self.val = val

class SymbolTable():
    '''data struct to manage symbols'''
    def __init__(self, syms = {}):
        self.syms = syms

    def add(self, sym):
        self.syms[sym.id] = sym

    def get(self, id):
        if not id in self.syms:
            print('tf dude? ', id, ' does not exist!')
        return self.syms[id]
    
    def update(self, sym):
        if not sym.id in self.syms:
            self.add(sym)
        else:
            self.syms[sym.id] = sym
