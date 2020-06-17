from enum import Enum
from graphviz import Digraph
from datetime import datetime

class ErrType(Enum):
    LEXIC = 1
    SINTACTIC = 2
    SEMANTIC = 3

class ErrNode():
    def __init__(self, description, row):
        self.description = str(description)
        self.row = str(row)

lexicArgs = [] 
sintacticArgs =  [] 
semanticArgs = [] 
#this variable needs to be updtaed every time
#the parser is called
linesCount_ = 0

def addErr(type, description,row):
    '''this function adds errors to the error report'''
    #the line number needs to be fixed first
    if type == ErrType.LEXIC:
        lexicArgs.append(ErrNode(str(description), row))
    elif type == ErrType.SINTACTIC:
        sintacticArgs.append(ErrNode(str(description), row))
    elif type == ErrType.SEMANTIC:
        semanticArgs.append(ErrNode(str(description), row))

def createReport(linec):
    '''this function create the three error reports'''
    linesCount_ = linec
    addContentToDot(Digraph(name="Lexic_errors",node_attr={'shape':'plaintext', 'color':'green'}),lexicArgs,"Lexical errors")
    addContentToDot(Digraph(name="Sintactic_errors",node_attr={'shape':'plaintext','color':'blue'}),sintacticArgs,"Sintactic errors")
    addContentToDot(Digraph(name="Semantic_errors",node_attr={'shape':'plaintext','color':'orange'}),semanticArgs,"Semantic errors")

def addContentToDot(dotObj,content,reportName):
    '''add nodes to the graphviz object dotObj'''
    #string to store de html value
    lblStr = '<<table align="center" cellspacing="0" cellborder="1" border="0">'
    lblStr += "<tr><td colspan='3'>" + reportName +"</td> </tr>"
    lblStr += "<tr><td>Description</td> <td>Line</td></tr>"
    for i in content:
        if isinstance(i.row, int):
            i.row = linesCount_ - i.row
        lblStr += "<tr><td>"+i.description+"</td> <td>"+i.row+"</td></tr>"
    now = datetime.now()
    fstr = now.strftime("%d%m%y-%H%M%S")
    lblStr += "<tr><td colspan='3'>"+fstr+"</td> </tr>"
    lblStr += "</table>>"
    dotObj.node("d1",lblStr)
    dotObj.render(reportName + fstr,'report',False,True,'svg')