import sys
import math
import ply.lex as lex

filename = sys.argv[1]

f = open(filename, "r")



#RESERVED TOKENS
reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT'
}


# TOKENS
# RENAMED 'NAME' TO STRING
tokens = (
    'QUOTATIONS', 'STRING', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LPAREN', 'RPAREN', 'RBRACKET', 'LBRACKET',
    'MOD', 'EXPONENT', 'FDIVIDE',
    'LESS', 'LESSEQUAL', 'ISEQUAL', 'NOTEQUAL', 'GREATER', 'GREATEREQUAL',
    'NOT', 'AND', 'OR', 'ID'
)

# Tokens

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_STRING = r'\".[^"]*\"'
t_MOD = r'\%'
t_EXPONENT = r'\*\*'
t_FDIVIDE = r'//'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_ISEQUAL = r'=='
t_NOTEQUAL = r'<>'
t_GREATER = r'>'
t_GREATEREQUAL = r'>='

# DICTIONARY OF NAMES
names = {}


def t_ID(t):
    r'and|or|not'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'-?\d*(\d\.|\.\d)\d* | \d+'
    try:
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
import ply.lex as lex

lex.lex()

# Parsing rules
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'LESS', 'LESSEQUAL', 'ISEQUAL', 'GREATER', 'GREATEREQUAL'),
    ('right', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'FDIVIDE'),
    ('right', 'EXPONENT'),
    ('left', 'MOD'),
    ('left', 'TIMES', 'DIVIDE')
)

# TEMPORARILY DISABLED
def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]


def p_statement_expr(t):
    '''statement : expression
                 | word
                 '''
    print(t[1])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression FDIVIDE expression
                  | expression EXPONENT expression
                  | expression LESS expression
                  | expression LESSEQUAL expression
                  | expression ISEQUAL expression
                  | expression GREATER expression
                  | expression GREATEREQUAL expression
                  | expression AND expression
                  | expression OR expression
                  | NOT expression'''

    #print("operator is ", t[2])
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        if t[3] != 0:
            t[0] = t[1] / t[3]
        else:
            t.lexer.skip(9999)
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '//':
        t[0] = math.floor(t[1] / t[3])
    elif t[2] == '**':
        t[0] = math.pow(t[1], t[3])
    elif t[2] == '<':
        t[0] = t[1] < t[3]
    elif t[2] == '<=':
        t[0] = t[1] <= t[3]
    elif t[2] == '==':
        t[0] = t[1] == t[3]
    elif t[2] == '>':
        t[0] = t[1] > t[3]
    elif t[2] == '>=':
        t[0] = t[1] >= t[3]
    elif t[2] == 'and':
        if t[1] == 0:
            t[1] = False
        else:
            t[1] = True
        if t[3] == 0:
            t[3] = False
        else:
            t[3] = True
        t[0] = t[1] and t[3]
    elif t[2] == 'or':
        if t[1] == 0:
            t[1] = False
        else:
            t[1] = True
        if t[3] == 0:
            t[3] = False
        else:
            t[3] = True
        t[0] = t[1] or t[3]
    elif t[1] == 'not':
        if t[1] == 0:
            t[1] = False
        else:
            t[1] = True
        t[0] = not t[2]
    if t[0] == True:
        t[0] = 1
    elif t[0] == False:
        t[0] = 0


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]
def p_expression_number(t):
    'expression : NUMBER'
    t[0] = t[1]


# ---WORD AND WORD EXPRESSIONS---
def p_expression_string(t):
    'word : STRING'
    t[0] = t[1].replace("\"", "\'")

def p_expression_string_op(t):
    'word : word PLUS word'
    t[0] = t[1] + t[3]
    t[0] = t[0].replace("\'", "")
    t[0] = "\'" + t[0] + "\'"

def p_expression_word_index(t):
    'word : word LBRACKET expression RBRACKET'
    t[1] = t[1].replace("\'", "")
    t[0] = t[1][t[3]]
    t[0] = "\'" + t[0] + "\'"

def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    if t != None:
        print("SYNTAX ERROR")
        t.lexer.skip(9999)
    else:
        print("SEMANTIC ERROR")

import ply.yacc as yacc

yacc.yacc()

for line in f:
    yacc.parse(line)
