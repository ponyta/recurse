#!/usr/bin/env python3

from enum import Enum, auto

# Represents an AST Node
class Node:
    def __init__(self, key, children):
        self.key = key
        self.children = children

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
        return self.type.name + " " + self.value
    def __repr__(self):
        return self.type.name + " " + self.value

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
            while is_number(string[i]):
                i += 1
            tokens.append(Token(TokenType.NUMBER, string[num_start:i]))
            i -= 1
        elif is_letter(string[i]):
            id_start = i
            while is_letter(string[i]):
                i += 1
            tokens.append(Token(TokenType.FUNCTION, string[id_start:i]))
            i -= 1
        i += 1
    return tokens

# turns a list of tokens into an AST
def parse(tokens):
    if tokens[0].type is TokenType.OPEN_PAREN:
        if tokens[1].type is not TokenType.FUNCTION:
            raise AssertionError("Expected token with type FUNCTION, got " + str(tokens[1]) + " instead.")


test = "(first (list 1 (+ 2 34) 9))"
print(parse(tokenize(test)))
