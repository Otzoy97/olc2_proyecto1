from expression import Operator, ValType, Expression

class ValExpression(Expression):                                                                                  
    '''
    '''
    def __init__(self, value, type, row = -1):
        self.value = value
        self.type = type
        self.row = row

class OperationExpression(Expression):
    '''
    '''
    def __init__(self, op, e1 = None, e2 = None, row = -1):
        self.e1 = e1
        self.e2 = e2
        self.op = op 
        self.row = row
