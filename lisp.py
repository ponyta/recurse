#!/usr/bin/env python3

from enum import Enum, auto

# Represents an AST Node
class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.children = children

    def __str__(self):
        if self.children is None:
            return str(self.key) + "[]"
        return str(self.key) + "[ " + ",".join(map(str, self.children)) + " ]"

class TokenType(Enum):
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    NUMBER = auto()
    FUNCTION = auto()

class Token:
    def __init__(self, token_type, value=None):
        self.type = token_type
        if token_type is TokenType.OPEN_PAREN:
            self.value = '('
        elif token_type is TokenType.CLOSE_PAREN:
            self.value = ')'
        else:
            if value is None:
                raise AssertionError('NUMBER or FUNCTION tokens must supply a value')
            self.value = value

    def __str__(self):
        return self.type.name + " " + str(self.value)
    def __repr__(self):
        return self.type.name + " " + str(self.value)

def is_whitespace(char):
    if char is '\t' or char is '\n' or char is ' ':
        return True
    return False

# For now, we are only parsing natural numbers. Also we allow arbitrary leading
# zeros.
# TODO: implement ^[+|-]?[1-9][0-9]*\.?[0-9]*$ for arbitrary numbers
def is_number(char):
    if char <= '9' and char >= '0':
        return True
    return False

# Valid letters for an identifier (for a function, since there are no variables yet)
def is_letter(char):
    if ('a' <= char <= 'z' or 'A' <= char <= 'Z'
            or char is '+' or char is '-' or char is '*' or char is '/'):
        return True
    return False

# Turns the input string into an array of tokens
def tokenize(string):
    tokens = []
    i = 0
    while i < len(string):
        if is_whitespace(string[i]): # just ignore any whitespace
            while is_whitespace(string[i]):
                i += 1
            i -= 1
        elif string[i] == '(':
            tokens.append(Token(TokenType.OPEN_PAREN))
        elif string[i] == ')':
            tokens.append(Token(TokenType.CLOSE_PAREN))
        elif is_number(string[i]):
            num_start = i
            while i < len(string) and is_number(string[i]):
                i += 1
            tokens.append(Token(TokenType.NUMBER, int(string[num_start:i])))
            i -= 1
        elif is_letter(string[i]):
            id_start = i
            while is_letter(string[i]):
                i += 1
            tokens.append(Token(TokenType.FUNCTION, string[id_start:i]))
            i -= 1
        i += 1
    return tokens

"""
My basic LISP language

s-expr  ->  atom
        |   OPEN_PAREN FUNCTION {s-expr} CLOSE_PAREN
atom    ->  NUMBER

"""
def parse_sexpr(tokens):
    # print("parsing sexp for: ", tokens)
    if len(tokens) == 0:
        raise AssertionError("Expected tokens, not nothing")
    if tokens[0].type is TokenType.OPEN_PAREN:
        if len(tokens) < 3:
            raise AssertionError("Failed to parse s-expr rule for tokens: " + str(tokens))
        if tokens[1].type is not TokenType.FUNCTION:
            raise AssertionError("Expected token with type FUNCTION, got " + str(tokens[1]) + " instead.")
        tokens.pop(0) # pop the open paren
        parent = Node(tokens.pop(0))
        children = []
        while tokens[0].type is not TokenType.CLOSE_PAREN:
            children.append(parse_sexpr(tokens))
        parent.children = children
        tokens.pop(0) # pop off the close paren
        return parent
    elif tokens[0].type is TokenType.NUMBER:
        return Node(tokens.pop(0))
    else:
        raise AssertionError("Could not parse tokens: " + str(tokens))

def evaluate_ast(node):
    token = node.key
    print("evaluating", token)
    if token.type is TokenType.NUMBER:
        return token.value
    elif token.type is TokenType.FUNCTION:
        if token.value == "+":
            acc = 0
            for child in node.children:
                print(child)
                acc += evaluate_ast(child)
            return acc
        else:
            raise AssertionError("Unknown function name " + node.key)

test = "(+ (+ 1 (+ 2 34) 9))"
test = "(+ 1 2 3 4 5)"
# print(tokenize(test))
ast = parse_sexpr(tokenize(test))
print(ast)
print(evaluate_ast(ast))
