import os
import math
import random

def simpleCheck(equation):
    return True


def checker(equation):
    while '(' in equation:
        first_node = -1
        second_node = 0
        part_equation = []
        count = 0
        paranthesis_count = 0
        while (paranthesis_count != 0) or (first_node == -1):
            print(paranthesis_count)
            if (equation[count] == '(') and (first_node == -1):
                first_node = count
                paranthesis_count += 1 
                print(first_node)
            elif equation[count] == '(':
                paranthesis_count += 1
            elif equation[count] == ')':
                paranthesis_count -= 1
            count += 1
        first_node += 1
        second_node = count - 2
        count = first_node
        while count != second_node:
            part_equation.append(equation[count])
            count += 1
        part_equation.append(equation[count])
        result = checker(part_equation)
        count = first_node - 1
        second_node += 1
        while count != second_node:
            equation.pop(count)
            second_node -= 1
        equation[count] = str(result)
    if '^' in equation:
        equation = exponent(equation)
    if ('*' in equation) or ('/' in equation):
        equation = multdiv(equation)
    if '+' in equation:
        equation = add(equation)
    if '-' in equation:
        equation = subtract(equation)
    return equation[0]


def exponent(equation):         
    count = 1
    while count < len(equation):
        if equation[count] == '^':
            equation[count + 1] = pow(float(equation[count -1]),float(equation[count + 1]))
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
        count+=1
    return equation

def multdiv(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '*':
            result = multiply(equation[count-1], equation[count+1])
            equation[count+1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
        elif equation[count] == '/':
            result = divide(equation[count-1], equation[count+1])
            equation[count+1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
        count+=1
    return equation


def multiply(first, second):
    return float(first) * float(second)


def divide(first, second):
    return float(first) / float(second)


def add(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '+':
            result = float(equation[count-1]) + float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
        count+=1
    return equation


def subtract(equation):
    count = 1
    while count < len(equation):
        if equation[count] == '-':
            result = float(equation[count-1]) - float(equation[count + 1])
            equation[count + 1] = result
            equation.pop(count - 1)
            equation.pop(count - 1)
            count = 0
            print(equation)
        count+=1
    return equation