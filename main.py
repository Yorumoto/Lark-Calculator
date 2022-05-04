#!/usr/bin/python3
import logging

from lark.lexer import Token
from parser import parser
from lark import Transformer, logger, exceptions, Tree

logger.setLevel(logging.DEBUG)

ans = 0.0

class SelfTransformer(Transformer):
    def inf(self, _):
        return float('inf')

    def ans(self, _):
        global ans
        return ans

    def hex(self, n):
        try:
            return float(int(n[0].value, 0))
        except ValueError:
            raise exceptions.UnexpectedInput("Malformed hex number")

    def number(self, n):
        try:
            return float(n[0].value)
        except ValueError:
            raise exceptions.UnexpectedInput("Malformed number")
    
    def _arithemetic(self, t, operator=None):
        n = None

        for item in t:
            if item is None:
                continue

            if isinstance(item, Tree):
                print(item)
                continue
            
            if n is None:
                n = item
            elif operator and n is not None:
                n = operator(n, item)

        return n

    def EXIT(self, _):
        exit()

    plus = lambda self, n: self._arithemetic(n, operator=(lambda a, b: a + b))
    minus = lambda self, n: self._arithemetic(n, operator=(lambda a, b: a - b))
    multiply = lambda self, n: self._arithemetic(n, operator=(lambda a, b: a * b))
    divide = lambda self, n: self._arithemetic(n, operator=(lambda a, b: a / (b if b != 0 else 1)))
    pow = lambda self, n: self._arithemetic(n, operator=(lambda a, b: a ** b))

def main():
    global ans

    while True:
        try:
            tree = parser.parse(input("\033[31m>\033[0m "))
            results = SelfTransformer().transform(tree)

            for token in results.scan_values(lambda _: True):
                ans = token
                print(token)
                break
        except (exceptions.ParseError, exceptions.UnexpectedCharacters, exceptions.UnexpectedInput) as e:
            print(e)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
