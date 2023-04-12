import os
import math
import random

#functions for the calculator
#(digit, varaible, degree, side)
# Simplifies the list of tuples algebra equation as much as it can

def simplifyTuples(equation, first, second):
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
        if (equation[first] == '-') or (equation[first] == '+'):
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
    print(equation)
    count = 0
    while count < len(equation):
        if type(equation[count]) is tuple:
            #print(equation[count])
            digit = equation[count][0]
            variable = equation[count][1]
            degree = equation[count][2]
            side = equation[count][3]
        
            secondCount = count + 1
            
            #print(count, secondCount)
            
            while secondCount < len(equation):
                
                #print(count, secondCount)
                #print(equation[count], equation[secondCount])
                if (type(equation[secondCount]) is tuple) and (variable == equation[secondCount][1]) and (degree == equation[secondCount][2]):
                    #print("Inside")
                    print(equation[count], equation[secondCount])
                    equation = simplifyTuples(equation, count, secondCount)
                    print("Final equation : ", equation)
                    count = 0
                    #continue
                    #do the comparrision
                secondCount += 1
        count += 1


"""def algebraSimplify(equation):
    print(equation)
    count = 0
    status = []
    while count < len(equation):
        if type(equation[count]) is tuple:
            variable = equation[count][1]
            print(variable)
            statuscount = 0
            flag = 0
            while statuscount < len(status):
                if variable in status[statuscount]:
                    flag = 1
                    status[statuscount][1] += 1
                    break
                statuscount += 1
            if flag == 0:
                status.append(list([equation[count][1], 1]))
            print(status)
        count += 1
    count = 0
    while count < len(status):
        if status[count][1] == 1:
            status.pop(count)
            count = 0
        else:
            count += 1
    print(status)           #status is a 2D list that gives us the varibles that we have to simplify in the overall equation and the amount of occurences
    # move to a new funciton
    if len(status) > 0:
        length = 0
        toSimplify = []
        while length < len(status):
            count = 0
            variable = status[length][0]
            repeats = status[length][1]
            print("Repeats : ", repeats)
            #print("Inside")
            while len(status) < (repeats):
                #print("Inside Inside")
                if type(equation[count]) is tuple:
                    print("Inside")
                    if equation[count][1] == variable:
                        if count == 0:
                            toSimplify.append(equation[count])      #DOUBLE CHECK IF YOU CAN COMBINE THE TWO CONDITIONS
                            equation.pop(count)
                        elif type(equation[count-1]) is str:
                            toSimplify.append(equation[count-1])
                            equation.pop(count-1)
                            toSimplify.append(equation[count-1])
                            equation.pop(count-1)
                        else:
                            toSimplify.append(equation[count])
                            equation.pop(count)
                        print("Equation : " + str(equation))
                        print("ToSimplify : " + str(toSimplify))
                        count = 0
                        print("COUNT : " + str(count))
                count += 1
                print("Count : ", count)
            length += 1
    else:
        return equation
"""            
            
            
    
    #while count < len(equation):
    #    if type(equation[count]) is tuple:
    #        if count != 0 and (equation[count-1] == '+' )
            
        
    

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
    count = 0
    side = 'l'
    newList = []
    while count < len(equation):
        #print(count)
        if equation[count] == '=':
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
        print(equation)
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