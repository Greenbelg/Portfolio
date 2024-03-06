import ast
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from syntax_tree import SyntaxTree


class TestSyntaxTree(unittest.TestCase):
    def setUp(self):
        self.syntax_tree = SyntaxTree()

    def test_build_valid_query(self):
        query = ['word', 'AND', 'NOT', 'another_word', 'OR', 'third_word']
        result = self.syntax_tree.build(query)
        self.assertIsNotNone(self.syntax_tree.tree)

    def test_build_invalid_query(self):
        query = ['word', 'NOT', 'invalid_syntax', 'OR', 'third_word']
        result = self.syntax_tree.build(query)
        self.assertEqual(result, -1)
        self.assertIsNone(self.syntax_tree.tree)

    def test_get_first_expression(self):
        query = ['word', 'AND', 'NOT', 'another_word', 'OR', 'third_word']
        self.syntax_tree.build(query)
        first_expression = self.syntax_tree.get_first_expression()
        self.assertIsNotNone(first_expression)

    def test_try_get_value(self):
        constant_node = ast.Constant(value=42)
        result = SyntaxTree.try_get_value(constant_node)
        self.assertEqual(result, 42)

        name_node = ast.Name(id='variable', ctx=ast.Load())
        result = SyntaxTree.try_get_value(name_node)
        self.assertEqual(result, 'variable')

        string_value = 'test_string'
        result = SyntaxTree.try_get_value(string_value)
        self.assertEqual(result, 'test_string')

    def test_try_get_operand_not(self):
        operand_node = ast.Constant(value=42)
        unary_op_node = ast.UnaryOp(op=ast.Not(), operand=operand_node)
        result = SyntaxTree.try_get_operand_not(unary_op_node)
        self.assertEqual(result, operand_node)

        result = SyntaxTree.try_get_operand_not(operand_node)
        self.assertIsNone(result)

    def test_try_get_operands_and(self):
        operand1 = ast.Constant(value=42)
        operand2 = ast.Constant(value=13)
        bool_op_node = ast.BoolOp(op=ast.And(), values=[operand1, operand2])
        result = SyntaxTree.try_get_operands_and(bool_op_node)
        self.assertEqual(result, (operand1, operand2))

        operand3 = ast.Constant(value=7)
        bool_op_node_or = ast.BoolOp(op=ast.Or(), values=[operand1, operand3])
        result_or = SyntaxTree.try_get_operands_and(bool_op_node_or)
        self.assertIsNone(result_or)

        result = SyntaxTree.try_get_operands_and(operand1)
        self.assertIsNone(result)

    def test_try_get_operands_or(self):
        operand1 = ast.Constant(value=42)
        operand2 = ast.Constant(value=13)
        bool_op_node = ast.BoolOp(op=ast.Or(), values=[operand1, operand2])
        result = SyntaxTree.try_get_operands_or(bool_op_node)
        self.assertEqual(result, (operand1, operand2))

        operand3 = ast.Constant(value=7)
        bool_op_node_and = ast.BoolOp(op=ast.And(),
                                      values=[operand1, operand3])
        result_and = SyntaxTree.try_get_operands_or(bool_op_node_and)
        self.assertIsNone(result_and)

        result = SyntaxTree.try_get_operands_or(operand1)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
