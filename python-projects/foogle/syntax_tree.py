import ast
from ast import Constant, UnaryOp, Name, BoolOp, And, Or


class SyntaxTree:
    def __init__(self):
        self.__query_string = ''
        self.tree = None

    def build(self, query):
        self.__build_query_string(query)
        try:
            self.tree = ast.parse(self.__query_string)
        except SyntaxError:
            return -1
        return self

    def __build_query_string(self, query_tokens):
        operators = ['AND', 'OR', 'NOT']
        for token in query_tokens:
            if token in operators:
                self.__query_string += token.lower()
            else:
                self.__query_string += f'"{token}"'
            self.__query_string += ' '

    def get_first_expression(self):
        if self.tree:
            return self.tree.body[0].value

    @staticmethod
    def try_get_value(node):
        if isinstance(node, str):
            return node

        if isinstance(node, Constant):
            return node.value

        if isinstance(node, Name):
            return node.id

    @staticmethod
    def try_get_operand_not(node):
        if isinstance(node, UnaryOp):
            return node.operand

    @staticmethod
    def try_get_operands_and(node):
        if isinstance(node, BoolOp) and isinstance(node.op, And):
            return node.values[0], node.values[1]

    @staticmethod
    def try_get_operands_or(node):
        if isinstance(node, BoolOp) and isinstance(node.op, Or):
            return node.values[0], node.values[1]
