import os
import math
import random

def pythagoreanCheck(a, b, c):
    c = float(c)
    result = pythagoreanHypotenuse(a, b)
    if c == result:
        return "The triangle entered is a valid right triangle"
    else: 
        return "The triangle entered is an invalid right triangle"

def pythagoreanSide(a, b):
    c = ( (float(b) * float(b)) - (float(a) * float(a)) ) ** 0.5
    return c

def pythagoreanHypotenuse(a, b):
    c = ( (float(a) * float(a)) + (float(b) * float(b)) ) ** 0.5
    return c

#the parseFraction funciton breaks the passed fraction into denominator and denomitor and then return the result in a tuple
def parseFraction(fraction):
    num = ""
    denom = ""
    count = 0
    flag = 0
    while count < len(fraction):
        if fraction[count] == '/':
            flag = 1
            count += 1
        if flag == 0:
            num += fraction[count]
        else:
            denom += fraction[count]
        count += 1
    return(int(num), int(denom))
       
def simplifyFraction(fraction):
    (a, b) = parseFraction(fraction)
    num = a
    denom = b
    while b != 0:
        a, b = b, a % b
    if a == 1:
        return fraction
    num = num / a
    denom = denom / a
    simplified = ""
    simplified += str(int(num))
    simplified += "/"
    simplified += str(int(denom)) 
    return simplified  

def gcd(fraction1, fraction2):
    (a, b) = parseFraction(fraction1)
    (c, d) = parseFraction(fraction2)
    while d != 0:
        b, d = d, b % d
    return int(b)   
     
# The LCD funciton works with fractions in order to find the least common denominator of the two given fractions
def lcd(fraction1, fraction2):
    (a, b) = parseFraction(fraction1)
    (c, d) = parseFraction(fraction2)
    greatest = gcd(fraction1, fraction2)
    least = (b * d) / greatest
    return int(least)


# This function takes two fractions and then checks is they are the same denominator
# if they are not the same denominator, then the common denomintor is found by calling the LCD funciton
def addFraction(fraction1, fraction2):
    (num1, denom1) = parseFraction(fraction1)
    (num2, denom2) = parseFraction(fraction2)
    addedFunction = ""
    if denom1 == denom2:
        addedNums = num1 + num2
        addedFunction += str(addedNums)
        addedFunction += "/"
        addedFunction += str(denom1)
    else:
        commonDenom = lcd(fraction1, fraction2)
        
        f1 = commonDenom / denom1
        num1 *= f1
        
        f2 = commonDenom / denom2
        num2 *= f2
        
        addedNums = num1 + num2
        addedFunction += str(int(addedNums))
        addedFunction += "/"
        addedFunction += str(commonDenom)
        
    return addedFunction
    
    
    
def subtractFraction(fraction1, fraction2):
    (num1, denom1) = parseFraction(fraction1)
    (num2, denom2) = parseFraction(fraction2)
    subtractedFunc = ""
    if denom1 == denom2:
        addedNums = num1 - num2
        subtractedFunc += str(addedNums)
        subtractedFunc += "/"
        subtractedFunc += str(denom1)
    else:
        commonDenom = lcd(fraction1, fraction2)
        
        f1 = commonDenom / denom1
        num1 *= f1
        
        f2 = commonDenom / denom2
        num2 *= f2
        
        subtractedNums = num1 - num2
        subtractedFunc += str(int(subtractedNums))
        subtractedFunc += "/"
        subtractedFunc += str(commonDenom)
        
    return subtractedFunc

def multiplyFraction(fraction1, fraction2):
    (num1, denom1) = parseFraction(fraction1)
    (num2, denom2) = parseFraction(fraction2)
    multiplied = ""
    nums = num1 * num2
    denoms = denom1 * denom2
    multiplied += str(nums)
    multiplied += "/"
    multiplied += str(denoms)
    multiplied = simplifyFraction(multiplied)
    return multiplied
    
def divideFraction(fraction1, fraction2):
    (num1, denom1) = parseFraction(fraction1)
    (num2, denom2) = parseFraction(fraction2)
    divided = ""
    newNum = num1 * denom2
    newDenom = denom1 * num2
    divided += str(newNum)
    divided += "/"
    divided += str(newDenom)
    divided = simplifyFraction(divided)
    return divided

    

#functions for the calculator
#(digit, varaible, degree, side)
# Simplifies the list of tuples algebra equation as much as it can

def simplifyTuples(equation, first, second):
    print("First :", first, "Second :", second)
    copy = equation
    variable = equation[first][1]
    degree = equation[first][2]
    side = equation[first][3]
    if equation[first][3] == 'l':
        if first == 0 or (equation[first - 1] == '+'):
            if (equation[second - 1] == '+') and (equation[second][3] == 'l'):
                print("1")
                digit = float(equation[first][0]) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
                #side = equation[first][3]
            elif (equation[second - 1] == '-') and (equation[second][3] == 'l'):
                print("2")
                digit = float(equation[first][0]) - float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
                #side = equation[first][3]
            elif ((equation[second - 1] == '+') or (type(equation[second - 1]) is tuple)) and (equation[second][3] == 'r'):
                print("3")
                digit = float(equation[first][0]) - float(equation[second][0])
                if equation[second - 1] == '+':
                    equation.pop(second - 1)
                    equation.pop(second - 1)
                else:
                    equation.pop(second)
            elif (equation[second - 1] == '-') and (equation[second][3] == 'r'):
                print("4")
                digit = float(equation[first][0]) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
        elif equation[first - 1] == '-':
            if equation[second - 1] == '+' and (equation[second][3] == 'l'):
                print("5")
                digit = ((-1) * (float(equation[first][0]))) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
            elif equation[second - 1] == '-' and (equation[second][3] == 'l'):
                print("6")
                digit = ((-1) * (float(equation[first][0]))) - float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
            elif ((equation[second - 1] == '+') or (type(equation[second - 1]) is tuple)) and (equation[second][3] == 'r'):
                print("7")
                digit = ((-1) * (float(equation[first][0]))) - float(equation[second][0])
                if equation[second - 1] == '+':
                    equation.pop(second - 1)
                    equation.pop(second - 1)
                else:
                    equation.pop(second)
            elif equation[second - 1] == '-' and (equation[second][3] == 'r'):
                print("8")
                digit = ((-1) * (float(equation[first][0]))) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
    elif equation[first][3] == 'r':
        if (type(equation[first - 1]) is tuple) or (equation[first - 1] == '+'):
            if equation[second - 1] == '+':
                print("9")
                digit = float(equation[first][0]) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
            elif equation[second - 1] == '-':
                print("10")
                digit = float(equation[first][0]) - float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
        elif equation[first - 1] == '-':
            if equation[second - 1] == '+':
                print("11")
                digit = ((-1) * float(equation[first][0])) + float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
            elif equation[second - 1] == '-':
                print("12")
                digit = ((-1) * float(equation[first][0])) - float(equation[second][0])
                equation.pop(second - 1)
                equation.pop(second - 1)
    if digit == 0:
        if (equation[first - 1] == '-') or (equation[first - 1] == '+'):
            equation.pop(first - 1)
            equation.pop(first - 1)
        else:
            equation.pop(first)
        return equation
    else:
        newTuple = (str(digit), variable, degree, side)
        #print(equation[first], equation[second], newTuple)
        equation[first] = newTuple
        if (equation[first] == '-') or (equation[first] == '+'):
            equation.pop(first - 1)
        return equation
                 

def algebraSimplify(equation):
    print("AlgrebraSimplify: ", equation)
    count = 0
    modifyflag = 0
    while count < len(equation):
        if modifyflag == 1:
            count = 0
            print("Inside of flag reset: ", equation)
        modifyflag = 0
        if type(equation[count]) is tuple:
            #print(equation[count])
            digit = equation[count][0]
            variable = equation[count][1]
            degree = equation[count][2]
            side = equation[count][3]
        
            secondCount = count + 1
            
            #print(count, secondCount)
            
            while secondCount < len(equation):
                
                print(equation[count], equation[secondCount])
                #print(equation[count], equation[secondCount])
                if (type(equation[secondCount]) is tuple) and (variable == equation[secondCount][1]) and (degree == equation[secondCount][2]):
                    #print("Inside")
                    #print(equation[count], equation[secondCount])
                    print("Before modification:", equation)
                    equation = simplifyTuples(equation, count, secondCount)
                    print("Modified: ", equation)
                    #print("Final equation : ", equation, turnBackToString(equation))
                    modifyflag = 1
                    break
                    #continue
                    #do the comparrision
                secondCount += 1
        count += 1
    return turnBackToString(equation)

def turnBackToString(equation):
    print("This is the turnBackToString function", equation)
    stringEquation = ""
    count = 0
    flag = 1
    while count < len(equation):
        #print(stringEquation)
        print(equation[count])
        if type(equation[count]) is tuple:
            if equation[count][3] == 'r' and flag == 1:
                stringEquation += '='
                stringEquation += ' '
                flag = 0
            if equation[count][0] != '1':
                stringEquation += equation[count][0] 
            if equation[count][1] != None:
                stringEquation += equation[count][1]
            if equation[count][2] != None:
                stringEquation += '^'
                stringEquation += equation[count][3]
        else:
            if equation[count + 1][3] == 'r' and flag == 1:
                stringEquation += '='
                flag = 0
                stringEquation += ' '
            stringEquation += equation[count]
        stringEquation += ' '
        count += 1
    return(stringEquation)
    

#makes a list of tuples with (digit, varaible, degree, side) if operator then just an operator sign
def makeTuples(element, side):
    digit = ""
    variable = None
    exponentFlag = 0
    degree = ""
    for char in element:
        if exponentFlag == 1:
            degree = degree + char
        elif char.isnumeric():
            digit = digit + char
        elif char == '^':
            exponentFlag = 1
        elif char.isalpha:
            variable = char
    if exponentFlag == 0:
        degree = None
    if digit == "":
        digit = "1"
    return (digit, variable, degree, side)
            
def isOperator(operator):
    if operator == '+' or operator == '-' or operator == '*' or operator == '/' or operator == '^' or operator == '(' or operator == ')':
        return True  

def tupleList(equation):
    print("tupleList :", equation)
    count = 0
    side = 'l'
    newList = []
    while count < len(equation):
        #print(count)
        if equation[count] == '=':
            #result
            side = 'r'
            count += 1
            continue
        if isOperator(equation[count]):
            result = equation[count]
        else:
            result = makeTuples(equation[count], side)
        count += 1
        newList.append(result)
    #print(newList)
    count = 0
    while count < len(newList):
        #if (type(newList[count])) is str:
        #    print("It is a string")
        #elif type(newList[count]) is tuple:
        #    print("It is a tuple")
            
        count += 1
    return newList
        
        

def simpleCheck(equation):
    length = len(equation)
    count = 0
    last = ''
    parantheses_check = 0
    while count < length:
        if equation[count] == '(':
            parantheses_check += 1
            last = '('
        elif equation[count] == ')':
            parantheses_check -= 1
            last = ')'
        count += 1
    if parantheses_check != 0:
        return "Incorrect parantheses count."
    elif last == '(':
        return "Incorrect parantheses placement"
    return True


def slope(equation, answer):
    newList = tupleList(equation)
    #algebraSimplify(newList)
    if answer == "slope":
        if (equation[0] == 'y') and (equation[1]) == '=':
            equation.pop(0)
            equation.pop(0)
        mx = list(equation[0])
        if 'x' in mx:
            mx.remove('x')
        slope = ""
        for ele in mx:
            slope += ele
        if equation[1] == '-':
            value = -1
            intercept = float(equation[2]) * float(value)
        else:
            intercept = equation[2]
    return(slope, intercept)


def checker(equation):
    while '(' in equation:
        #print(equation)
        first_node = -1
        second_node = 0
        part_equation = []
        count = 0
        paranthesis_count = 0
        while (paranthesis_count != 0) or (first_node == -1):
            if (equation[count] == '(') and (first_node == -1):
                first_node = count
                paranthesis_count += 1
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
            #print(equation)
        count+=1
    return equation

#helpuse function