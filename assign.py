from expression import ValType, Operator
from instruction import ValExpression, RegisterType, Assignment
from operation import OperationExpression
from st import Symbol, SymbolTable, getSymbol, updateSymbol, findSymbol
from math import trunc
from PyQt5 import QtWidgets
from err import addErr, ErrType

def solve_val(i):
    '''This function returns a ValExpression'''
    if (i.type != ValType.REFVAR):
        #if is not a variable reference returns the ValExpression itself
        return i
    else: 
        #if is a variable reference, it looks for a coincidence on any symbol table
        #then create a ValExpression with the raw value (and its type) and returns it
        assign_instance = i.value
        #gets an array access
        arrAccess = None if (assign_instance.valExp == None) else createIdxCol(assign_instance.valExp)
        #gets a symbol
        symb_FromAssign = getSymbol(assign_instance.varName, assign_instance.varType)
        if symb_FromAssign == None:
            #There was not symbol returned
            #return a 0 integer value
            #THIS IS AN ERROR
            return ValExpression(0, ValType.INTEGER)
        else:
            #There was a symbol returned
            #is a pointer? -> solve the pointer
            if(symb_FromAssign.type == ValType.POINTER):
                symb_FromAssign = solve_pointer(symb_FromAssign)
                if (arrAccess != None):
                    #It is necesary to travel through the given symbol value
                    r = throughDict(symb_FromAssign.value, arrAccess)
                    if r == None:
                        addErr(ErrType.SEMANTIC, "","")
                        return ValExpression(0, ValType.INTEGER)
                    else:
                        return ValExpression(r.value, r.type)
                else:
                    return ValExpression(symb_FromAssign.value, symb_FromAssign.type)
            #is an array? -> access through array
            elif(symb_FromAssign.type == ValType.ARRAY or symb_FromAssign.type == ValType.STRUCT or symb_FromAssign.type == ValType.STRING):
                if (arrAccess != None):
                    #It is necesary to travel through the given symbol value
                    r = throughDict(symb_FromAssign.value, arrAccess)
                    if r == None:
                        return ValExpression(0, ValType.INTEGER)
                    else:
                        return ValExpression(r.value, r.type)
                else:
                    #if the <else> statement is executed perhabps createIdxCol poped an error
                    # or there is a string, or
                    #although is possible to copy an array, this practice is not recomended
                    return ValExpression(symb_FromAssign.value, symb_FromAssign.type)
            else:
                #perhaps is a integer, string, float or a char
                return ValExpression(symb_FromAssign.value, symb_FromAssign.type)
            
def createIdxCol(col = []):
    '''create an array from the array returned by the parser in Assignment.valExp'''
    rcol = []
    for i in col:
        if isinstance(i, str):
            rcol.append(str(i))
        elif isinstance(i, int):
            rcol.append(int(i))
        elif isinstance(i, Assignment):
            #look for a symbol
            syym = getSymbol(i.varName,i.varType)
            if (syym != None):
                #a symbol was returned
                syym = solve_pointer(syym)
                #The symbol returned must be a integer or a string
                if isinstance(syym.value, int) or isinstance(syym.value, str) :
                    rcol.append(syym.value)
                else:
                    addErr(ErrType.SEMANTIC, "Error: unabled to retrieve value from "+ str(i.varType)+ ""+ str(i.varName),i.row)    
                    return None
            else:
                #a symbol was not returned, so the var does not exist
                addErr(ErrType.SEMANTIC, "Error: the variable does not exists "+ str(i.varType)+ ""+ str(i.varName), i.row)
                #return a None value
                return None
    return rcol

def solve_pointer(sym):
    '''takes a symbol and finds out if it's a pointer
        if is, look for a reference in the symbol table
        else, returns the symbol 'sym'
        On erro returns an integer symbol with value 0'''
    if sym.type == ValType.POINTER:
        #Gets the assignment value
        valSym = sym.value
        #gets an array access
        arrAccess = None if (valSym.valExp == None) else createIdxCol(valSym.valExp)
        #Gets the Symbol referenced
        valSym = getSymbol(valSym.varName, valSym.varType)
        #Checks if valSymm is not None
        if valSym != None:
            #Checks if arrAccess is not None
            if arrAccess == None:
                #There is no need to travel through the given symbol value
                #Checks again if valSym is a pointer
                return solve_pointer(valSym)
            else:
                #It is necesary to travel through the given symbol value
                r = throughDict(valSym.value,arrAccess)
                if r == None:
                    #an error took place when 'throughDict' were executed
                    return Symbol(None,ValType.INTEGER,0)
                else:
                    return r
        else:
            #the symbol was not found so, an error pops up and returns a zero
            addErr(ErrType.SEMANTIC, "Error: unable to reference "+str(valSym.varType)+ str(valSym.varName),"")
            return Symbol(None,ValType.INTEGER,0)
    else:
        return sym

def throughDict(dic, idxcol = []):
    '''travels through a given symbol
        if theres is an error, returns None
        else, returns a Symbol'''
    tmp = dic
    try:
        for i in idxcol:
            if isinstance(tmp, dict):
                if not i in tmp:
                    addErr(ErrType.SEMANTIC, "Error: given index value doesn't exist","")
                    return None
                else:
                    tmp = tmp[i]
            elif isinstance(tmp, str):
                #if the index is not integer
                if not isinstance(i, int):
                    addErr(ErrType.SEMANTIC,"Error: illegal index for a string value " + str(i) ,"")
                #if the index is an integer but is out of bonds
                if len(tmp)-1 > i:
                    return Symbol(None,ValType.STRING,tmp[i])
                else:
                    addErr(ErrType.SEMANTIC,"Error: index out of border, string: " +str(i) ,"")
                    return None
            else:
                addErr(ErrType.SEMANTIC, "Error: can't access through array to given symbol. " +str(tmp),"")
                return None
        # symbol is about to be returned
        if isinstance(tmp, str):
            return Symbol(None,ValType.STRING,tmp)
        elif isinstance(tmp, float):
            return Symbol(None,ValType.FLOAT,tmp)
        elif isinstance(tmp, int):
            return Symbol(None,ValType.INTEGER,tmp)
        else:
            #if the else statment is executed, perhaps there was a partial access
            # and reached object/element in the arrays is not a "flat value"
            addErr(ErrType.SEMANTIC, "Error: unknown value found in array " + str(tmp), "")
    except:
        addErr(ErrType.SEMANTIC, "Error: unable to access through array" ,"")
    return None

def setValueInArray(array, idxcol, value):
    '''
        This function tries to write the given <value> in the <array> at the
        indicated position by <idxcol>
    '''
    if not isinstance(array, dict):
        #if the array parameter is not a dictionary instance then an error will pop up
        addErr(ErrType.SEMANTIC, "Error: cannot set a value at index " +str(idxcol[0]) + ". \nThe given symbol is not an array or the index '" +str(idxcol[0]) +"' is already occupied","")
        return
    if len(idxcol) == 1:
        #If only one value remains in idxcol then it is assumed that the 
        #desired position as already been reached and the <value> can already
        #be written there
        temp = idxcol.pop(0)
        if temp in array and isinstance(array[temp], dict):
            #If the 'temp' position has already been taken and is not
            # a 'flat value' (integer, string, float) then
            #it is assumed that the <value> cannot be written there
            addErr(ErrType.SEMANTIC, "Error: index '" +str(temp) +"' is already occupied","")
            return
        array[temp] = value
    else:
        #gets the first value in idxcol
        temp = idxcol.pop(0)
        #if array is an instance of dict and the 'temp' index value 
        #does not exist in that instance then creates a dictionary
        #at that 'temp' position
        if isinstance(array,dict) and not temp in array:
            array[temp] = {}
        #the next if statement is used if there is a string stored
        # at 'temp' in 'array', the idxcol's length is equal or greater than 1, 
        # and the idxcol value is an integer
        if isinstance(array[temp], str) and len(idxcol) >= 1:
            if isinstance(idxcol[0], int):
                #this var will save a copy altered of the original string
                auxStr = ""
                #string stored in array[temp]
                aStr = array[temp]
                #length of the string in array[temp]
                lenStr =len(aStr)
                #this var will help to track the next loop
                cont = lenStr if idxcol[0] + 1 <= lenStr else idxcol[0] + 1
                for i in range(0, cont):
                    #this loop will copy the existent string
                    #and will alter it 
                    if i == idxcol[0]:
                        auxStr += str(value)
                    elif i + 1 <= lenStr:
                        auxStr += aStr[i]
                    else:
                        auxStr += " "
                array[temp] = auxStr
                if len(idxcol) > 1:
                    # this warning will let it know if there was indices that was not used
                    # and therefore those indices are not necessary
                    addErr(ErrType.SEMANTIC,"Warning: unreachable index " + str(idxcol[1]),"")
                return
            else:
                # if the index is not an integer then, an error will pop up
                # It cannot use a non-integer value to index a string 
                addErr(ErrType.SEMANTIC, "Error: illegal index, string symbols should be indexed with integers","")
                return
        setValueInArray(array[temp], idxcol, value)

def solve_assign(i):
    '''receives a pair [Assignment, OperationExpression] to create a symbol'''
    #retrieve name an assignment instance
    var_Assign = i[0]
    #get an array access for the assignment
    var_Access = None if (var_Assign.valExp == None) else createIdxCol(var_Assign.valExp)
    #solve_oper 
    var_Op = i[1] #operationexpression instance
    #solve opr, returns a Symbol
    var_Temp = None
    if isinstance(var_Op, ValExpression):
        #call solve_var, this function returns an instance of ValExpression
        var_Temp = solve_val(var_Op)
    elif isinstance(var_Op, OperationExpression):
        #call solve_opr, this function return an instance of Symbol
        var_Temp = solve_oper(var_Op) #returns Symbol
    #check if the variable name, stored in var_Assign, already exists
    #in some symbol table
    check_var = findSymbol(var_Assign.varName, var_Assign.varType)
    #create an instance of Symbol with the informatcion of varAssign
    #and the information returned by the function solve_val or solve_oper
    var_Temp = Symbol(var_Assign.varName, var_Temp.type, var_Temp.value)
    if (check_var != None):
        #The variable already exists so, it has to be updated
        #solve pointer
        check_var = solve_pointer(check_var)
        #Checks if it's an array value
        if check_var.type == ValType.ARRAY:
            #The array variable cannot be overwritten but it can be altered
            if var_Access == None:
                addErr(ErrType.SEMANTIC, "Error: indexed access to an array variable expected\n     " + 
                str(var_Assign.varType) + str(var_Assign.varName) + " was not assigned", var_Assign.row)
                return
            else:
                #if var_Access's value was not None
                setValueInArray(check_var.value, var_Access, var_Temp.value)
                updateSymbol(var_Assign.varName, var_Assign.varType, check_var)
        elif check_var.type == ValType.STRING:
            #The string value can be altered through array access
            if var_Access != None:
                #create a dictionary with one key '0' and the string as value
                dcc = {0: check_var.value} 
                #insert at the begging of the array the firt key of dcc
                var_Access.insert(0,0)
                #set the value
                setValueInArray(dcc,var_Access,var_Temp.value)
                #update the symbol
                check_var.value = dcc[0]
                updateSymbol(var_Assign.varName, var_Assign.varType, check_var)
            else:
                updateSymbol(var_Assign.varName, var_Assign.varType, var_Temp)     
        else:
            if var_Access != None:
                addErr(ErrType.SEMANTIC, "Warning: indexed access to a non array variable "+str(var_Assign.varType)+ str(var_Assign.varName), var_Assign.row)
            updateSymbol(var_Assign.varName, var_Assign.varType, var_Temp) 
            return
    else:
        if var_Access != None:
            addErr(ErrType.SEMANTIC, "Warning: indexed access to a non existent array variable "+str(var_Assign.varType)+ str(var_Assign.varName), var_Assign.row)
        updateSymbol(var_Assign.varName, var_Assign.varType, var_Temp) 

def solve_oper(i):
    if i.op == Operator.PLUS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            return Symbol(None, ValType.STRING, str(opl.value) + str(opr.value))
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value + opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value + opr.value))
        else:
            addErr(ErrType.SEMANTIC, "Error: can't add these operands " + str(typear), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.MINUS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: can't substract between string operands", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value - opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value - opr.value))
        else:
            addErr(ErrType.SEMANTIC, "Error: can't substract these operands " + str(typear), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.TIMES:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: can't multiply strings", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            return Symbol(None, ValType.FLOAT, float(opl.value * opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            return Symbol(None, ValType.INTEGER, int(opl.value * opr.value))
        else:
            addErr(ErrType.SEMANTIC, "Error: can't multiply these operands " +str(typear), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.QUOTIENT:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: can't divide strings", i.row)
            return Symbol(None, ValType.FLOAT, 0.0)
        elif any(i is ValType.INTEGER or ValType.FLOAT or ValType.CHAR for i in typear):
            if opr.value == 0:
                addErr(ErrType.SEMANTIC, "Error: division by zero", i.row)
                return Symbol(None, ValType.FLOAT, 0.0)
            else:
                return Symbol(None, ValType.FLOAT, opl.value / opr.value)
        else:
            addErr(ErrType.SEMANTIC, "Error: can't divide these operands " +str(typear), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.REMAINDER:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: can't get remainder from strings", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT for i in typear):
            if opr.value == 0:
                addErr(ErrType.SEMANTIC, "Error: division by zero", i.row)
                return Symbol(None, ValType.FLOAT, 0.0)
            else:
                return Symbol(None, ValType.FLOAT, float(opl.value % opr.value))
        elif any(i is ValType.INTEGER or ValType.CHAR for i in typear):
            if opr.value == 0:
                addErr(ErrType.SEMANTIC, "Error: division by zero", i.row)
                return Symbol(None, ValType.INTEGER, 0)
            else:
                return Symbol(None, ValType.INTEGER, int(opl.value % opr.value))
        else:
            addErr(ErrType.SEMANTIC, "Error: can't get remainder of these operands "+str(typear), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NEGATIVE:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            addErr(ErrType.SEMANTIC, "Error: can't get a negative value from string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.FLOAT:
            return Symbol(None, ValType.FLOAT, float(opl.value*-1))
        elif (opl.type == ValType.INTEGER or  opl.type == ValType.CHAR) :
            return Symbol(None, ValType.INTEGER, int(opl.value*-1))
        else:
            addErr(ErrType.SEMANTIC, "Error: can't a negative value of this operand " +str(opl.type), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.ABS:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            addErr(ErrType.SEMANTIC, "Error: can't get absolute value from string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.FLOAT:
            return Symbol(None, ValType.FLOAT, abs(opl.value))
        elif opl.type == ValType.INTEGER:
            return Symbol(None, ValType.INTEGER, abs(opl.value))
        elif opl.type == ValType.CHAR:
            return Symbol(None, ValType.CHAR, opl.value)
        else:
            addErr(ErrType.SEMANTIC, "Error: can't get absolute value from this operand "+ str(opl.type), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NOT:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            addErr(ErrType.SEMANTIC, "Error: can't negate a string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif opl.type == ValType.INTEGER or opl.type == ValType.CHAR or opl.type == ValType.FLOAT:
            temp = 0 if opl.value != 0 else 1
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot negate this operand " + str(opl.type), i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.AND:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use <and> on strings", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            return Symbol(None, ValType.INTEGER, tmpl and tmpr)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use <and> on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.XOR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use <xor> on strings", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            tmpl_n = 0 if opl.value != 0 else 1
            tmpr_n = 0 if opl.value != 0 else 1
            return Symbol(None, ValType.INTEGER, (tmpl and tmpr_n)  or (tmpl_n and tmpr))
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use <xor> on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.OR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: can't use <or> on strings", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmpl = 0 if opl.value == 0 else 1
            tmpr = 0 if opr.value == 0 else 1
            return Symbol(None, ValType.INTEGER, tmpl or tmpr)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use <or> on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.NOTBW:
        opl = solve_val(i.e1)
        if opl.type == ValType.STRING:
            addErr(ErrType.SEMANTIC, "Error: can't negate a string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        else:
            temp = ~int(opl.value)
            return Symbol(None, ValType.INTEGER, temp)
    elif i.op == Operator.ANDBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use and-bitwise on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) & int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use and-bitwise on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.ORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use or-bitwise on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) | int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use or-bitwise on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.XORBW:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use xor-bitwise on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) ^ int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use xor-bitwise on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.SHL:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use shift-left on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) << int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use shift-left on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.SHR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use shift-right on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            temp = int(opl.value) >> int(opr.value)
            return Symbol(None, ValType.INTEGER, temp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use shift-right on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.EQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        try:
            tmp = 1 if (opl.value == opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        except:
            addErr(ErrType.SEMANTIC, "Error: cannot compare these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)            
    elif i.op == Operator.NEQ:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        try:
            tmp = 1 if (opl.value != opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        except:
            addErr(ErrType.SEMANTIC, "Error: cannot compare these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.GR:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use 'greater than' on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value > opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use 'greater than' on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.GRE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use 'greater than or equal' on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value >= opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use 'greater than or equal' on  these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.LS:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use 'less than' on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value < opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use 'less than' on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.LSE:
        opl = solve_val(i.e1)
        opr = solve_val(i.e2)
        typear = [opl.type, opr.type]
        if any(i is ValType.STRING for i in typear):
            addErr(ErrType.SEMANTIC, "Error: cannot use 'less than or equal' on string", i.row)
            return Symbol(None, ValType.INTEGER, 0)
        elif any(i is ValType.FLOAT or ValType.INTEGER or ValType.CHAR for i in typear):
            tmp = 1 if (opl.value <= opr.value) else 0
            return Symbol(None, ValType.INTEGER, tmp)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use 'less than or equal' on these operands " + str(typear),  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif i.op == Operator.AMP:
        # checks if variable exist
        r = getSymbol(i.e1.value.varName, i.e1.value.varType)
        if (r != None):
            return Symbol(None, ValType.POINTER, i.e1.value)
        else:
            addErr(ErrType.SEMANTIC, "Error: cannot use & on "+ str(i.e1.value.varType) +str(i.e1.value.varName)+ ", doesn't exist",  i.row)
            return Symbol(None, ValType.INTEGER, 0)
    elif (i.op == Operator.CINT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.INTEGER, 0)
        if opr.type == ValType.CHAR:        r.value = int(opr.value)
        elif opr.type == ValType.STRING:    
            if (len(opr.value) > 0 ):
                r.value = ord(opr.value[0])
            else:
                r.value = 0
        elif opr.type == ValType.FLOAT:     r.value = trunc(opr.value)
        elif opr.type == ValType.INTEGER:   r.value = opr.value
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.value = ord(tmp[0])
            elif isinstance(tmp, float):    r.value = trunc(tmp)
            elif isinstance(tmp, int):      r.value = tmp
            else:                           addErr(ErrType.SEMANTIC, "Error: value in array "+str(opr.type)+" cannot cast to " + str(ValType.INTEGER),  i.row)
        else:
            addErr(ErrType.SEMANTIC, "Error: "+str(opr.type)+" cannot cast to " + str(ValType.INTEGER),  i.row)
        return r
    elif (i.op == Operator.CFLOAT):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.FLOAT, float(0.0))
        if opr.type == ValType.CHAR:        r.value = float(opr.value)
        elif opr.type == ValType.STRING:
            if (len(opr.value) > 0 ):
                r.value = float(ord(opr.value[0]))
            else:
                r.value = 0
        elif opr.type == ValType.FLOAT:     r.value = opr.value
        elif opr.type == ValType.INTEGER:   r.value = float(opr.value)
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.value = float(ord(tmp[0]))
            elif isinstance(tmp, float):    r.value = tmp
            elif isinstance(tmp, int):      r.value = float(tmp)
            else:                           addErr(ErrType.SEMANTIC, "Error: value in array "+str(opr.type)+" cannot cast to " + str(ValType.FLOAT),  i.row)
        else:
            addErr(ErrType.SEMANTIC, "Error: "+str(opr.type)+" cannot cast to " + str(ValType.FLOAT),  i.row)
        return r
    elif (i.op == Operator.CCHAR):
        opr = solve_val(i.e1)
        r = Symbol(None, ValType.CHAR, 0)
        if opr.type == ValType.CHAR:        r.value = abs(opr.value)
        elif opr.type == ValType.STRING:
            if (len(opr.value) > 0 ):
                r.value = abs(ord(opr.value[0]) % 256)
            else:
                r.value = 0
        elif opr.type == ValType.FLOAT:     r.value = abs(trunc(opr.value) % 256)
        elif opr.type == ValType.INTEGER:   r.value = abs(opr.value % 256)   
        elif opr.type == ValType.ARRAY:
            tmp = getFirst(opr.value) #get first value
            if isinstance(tmp, str):        r.value = abs(ord(opr.value[0]) % 256)
            elif isinstance(tmp, float):    r.value = abs(trunc(opr.value) % 256)
            elif isinstance(tmp, int):      r.value = abs(tmp)%256
            else:                           addErr(ErrType.SEMANTIC, "Error: value in array "+str(opr.type)+" cannot cast to " + str(ValType.CHAR),  i.row)
        else:
            addErr(ErrType.SEMANTIC, "Error: "+str(opr.type)+" cannot cast to " + str(ValType.CHAR),  i.row)
        return r
    elif i.op == Operator.READ:
        # shows an input box and save a string
        # creates an string symbol
        r = Symbol(None, ValType.STRING, "")
        txt, msg = QtWidgets.QInputDialog.getText(None, 'Read', 'Enter here:')
        if msg:
            r.value = txt
        return r
    elif i.op == Operator.ARRAY:
        # creates an array symbol
        r = Symbol(None,ValType.ARRAY,{})
        return r

def getFirst(arr):
    try:
        if isinstance(arr, dict):
            v_values = arr.values()
            v_it = iter(v_values)
            v_first = next(v_it)
            return getFirst(v_first)
        elif isinstance(arr, str): return arr
        elif isinstance(arr, float): return arr
        elif isinstance(arr, int): return arr
        else:
            addErr(ErrType.SEMANTIC, "Error: can't access through unknown data structure (a)","")
    except: 
        addErr(ErrType.SEMANTIC, "Error: can't access through unknown data structure (b)","")
        return 0
    return 0
