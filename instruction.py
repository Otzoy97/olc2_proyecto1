from enum import Enum
from operation import ValExpression, OperationExpression

class Instruction:
    '''This is an abstract class'''

class RegisterType(Enum):
    TVAR = 1
    AVAR = 2
    VVAR = 3
    RVAR = 5
    SVAR = 6
    SPVAR = 7
    #ARRAY = 8

class Print(Instruction):
    '''
        This class saves a value that is then used to print a message
    '''
    def __init__(self, msg):
        self.msg = msg

class Unset(Instruction):
    '''
        This class saves a variable name that must be deleted
    '''
    def __init__(self, varn):
        self.varn = varn

class Exit(Instruction):
    '''
        This class represents the end a procedure
    '''

class If(Instruction):
    '''
        This class make decisions upon a boolean given value 
    '''
    def __init__(self, bolVal, lblJmp, row):
        self.bolVal = bolVal
        self.lblJmp = lblJmp
        self.row = row

class GoTo(Instruction):
    '''
        To make a jump to a given label 
    '''
    def __init__(self, lblJmp, row):
        self.lblJmp = lblJmp
        self.row = row

class Assignment(Instruction):
    '''
        To set a value to a given variable
    '''
    def __init__(self, varName, varType, valExp = []):
        '''varName: name of the variable
           varType: type of the variable
           valExpe: saves the access for an array'''
        self.varName = varName
        self.varType = varType
        self.valExp = valExp

class Label(Instruction):
    '''
        Sets a label name that is then used to make a jump 
        inside the code
    '''
    def __init__(self, lblNm, row):
        self.lblNm = lblNm
        self.row = row