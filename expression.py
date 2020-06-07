from enum import Enum

class ARITHMETIC(Enum):
    '''Arithmetic operators'''
    PLUS = 1        # +
    MINUS = 2       # -
    TIMES = 3       # *
    QUOTIENT = 4    # /
    REMAINDER = 5   # %
    NEGATIVE = 6    # -
    ABS = 7         # abs

class LOGIC(Enum):
    '''Logic (booleans) operators'''
    NOT = 1         # !
    AND = 2         # &&
    XOR = 3         # xor
    OR = 4          # ||

class BYTE_(Enum):
    '''Byte operators'''
    NOTBW = 1       # ~ 
    ANDBW = 2       # &
    ORBW = 3        # |
    XORBW = 4       # ^
    SHL = 5         # <<
    SHR = 6         # >>

class RELATIONAL(Enum):
    '''Relational operators'''
    EQ = 1          # =
    NEQ = 2         # !=
    GR = 3          # >
    GRE = 4         # >=
    LS = 5          # <
    LSE = 6         # <=

class POINTER(Enum):
    '''Pointer operator'''
    AMP = 1         # &

class CAST(Enum):
    '''Casting operators'''
    INT = 1         # int
    FLOAT = 2       # float
    STRING = 3      # string

class NATIVE(Enum):
    '''Some native functions that works as operators'''
    READ = 1        # read()
    ARRAY = 2       # array()
