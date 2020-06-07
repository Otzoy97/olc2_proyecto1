class Instruction:
    '''This is an abstract class'''

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


""" class Read(Instruction):
    '''
        This class waits for user input and then saves it
    '''
    def __init__(self):
        self.inputVal = ""

class Array(Instruction):
    '''
        This class represents the declaration of an array
    '''
    def __init__(self) """

class Exit(Instruction):
    '''
        This class represents the end a procedure
    '''

class If(Instruction):
    '''
        This class make decisions upon a boolean given value 
    '''
    def __init__(self, bolVal, lblJmp):
        self.bolVal = bolVal
        self.lblJmp = lblJmp

class GoTo(Instruction):
    '''
        To make a jump to a given label 
    '''
    def __init__(self, lblJmp):
        self.lblJmp = lblJmp

class Assignment(Instruction):
    '''
        To set a value to a given variable
    '''
    def __init__(self, varName, exOp):
        self.varName = varName
        self.exOp = exOp

class Label(Instruction):
    '''
        Sets a label name that is then used to make a jump 
        inside the code
    '''
    def __init__(self, lblNm):
        self.lblNm = lblNm
