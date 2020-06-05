import ply.lex as lex
from ply.lex import TOKEN

# floating point regexes
dot = r'\.'
digits = r'[0-9]+'
scientific_notation = digits + dot + digits + r'[Ee]\-?' + digits  # 60.52e-2
floating_point_number = digits + dot + digits  # 60.500
fraction = dot + digits  # .500
int_part = digits + dot  # 60.

literals = "()[]{}:;,"

# lexemes
reserved_words = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

assign_operators = {
    'ASSIGN': r'=',
    'ADDASSIGN': r'\+=',
    'MINASSIGN': r'-=',
    'MULASSIGN': r'\*=',
    'DIVASSIGN': r'\/='
}

binary_operators = {
    'ADD': r'\+',
    'MIN': r'\-',
    'MUL': r'\*',
    'DIV': r'\/'
}

matrix_binary_operators = {
    'DOTADD': r'\.\+',
    'DOTMIN': r'\.\-',
    'DOTMUL': r'.\*',
    'DOTDIV': r'./',
    'TRANSPOSE': r'\''
}

relation_operators = {
    'LT': r'\<',
    'GT': r'\>',
    'LTE': r'\<\=',
    'GTE': r'\>\=',
    'NE': r'\!\=',
    'RELASSIGN': r'\=\='
}

numbers = {
    'INT': digits,
    'FLOAT': scientific_notation + r"|" + floating_point_number + r"|" + fraction + r"|" + int_part
}

strings = {
    'ID': r'[a-zA-Z_][a-zA-Z_0-9]*',
    'STR': r'\".*?\"',
    'IGN': ' \t',
    'COM': r'\#.*',
    'NL': r'\n+'
}

all_leksems = list(reserved_words.values()) + list(assign_operators) + list(binary_operators) + list(
    matrix_binary_operators) + list(relation_operators) + list(numbers) + list(strings)

# list of lexemes recognised by scanner
tokens = list([t for t in all_leksems])

# regexes
t_ADDASSIGN = assign_operators['ADDASSIGN']
t_MINASSIGN = assign_operators['MINASSIGN']
t_MULASSIGN = assign_operators['MULASSIGN']
t_DIVASSIGN = assign_operators['DIVASSIGN']
t_ASSIGN = assign_operators['ASSIGN']
t_ADD = binary_operators['ADD']
t_MIN = binary_operators['MIN']
t_MUL = binary_operators['MUL']
t_DIV = binary_operators['DIV']
t_DOTADD = matrix_binary_operators['DOTADD']
t_DOTMIN = matrix_binary_operators['DOTMIN']
t_DOTMUL = matrix_binary_operators['DOTMUL']
t_DOTDIV = matrix_binary_operators['DOTDIV']
t_TRANSPOSE = matrix_binary_operators['TRANSPOSE']
t_LT = relation_operators['LT']
t_GT = relation_operators['GT']
t_LTE = relation_operators['LTE']
t_GTE = relation_operators['GTE']
t_NE = relation_operators['NE']
t_RELASSIGN = relation_operators['RELASSIGN']
t_STR = strings['STR']
t_ignore = strings['IGN']
t_ignore_comment = strings['COM']


@TOKEN(strings['ID'])
def t_ID(t):
    t.type = reserved_words.get(t.value, 'ID')  # Check for reserved words
    return t


@TOKEN(numbers['FLOAT'])
def t_FLOAT(t):
    t.value = float(t.value)
    return t


@TOKEN(numbers['INT'])
def t_INT(t):
    t.value = int(t.value)
    return t


@TOKEN(strings['NL'])
def t_newline(t):
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print(f"Illegal character: {t.value[0]}, at line: {t.lineno}")
    t.lexer.skip(1)
    pass


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()

