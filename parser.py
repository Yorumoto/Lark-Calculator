from lark import Lark

_user_defined = r"/[A-Za-z_][0-9A-Za-z_]*/x"

_grammar = rf"""
    number: /[+-]?(0|[1-9][0-9\.e]*)/x
    hex: /0x([A-Fa-f0-9]*)/x
    
    ?ans: "ans"
    ?plus: expr "+" expr
    ?minus: expr "-" expr
    ?multiply: expr "*" expr
    ?divide: expr "/" expr
    ?pow: expr "^" expr

    inf: "inf"

    ?expr: number
        | hex
        | ans
        | plus 
        | minus 
        | multiply
        | divide
        | pow
        | "(" expr ")"
        | inf

    EXIT.256: "exit"

    program : expr* | EXIT
    start : program

    %import common.WS
    %ignore WS
"""

parser = Lark(_grammar)
