import os
import math
import random

def message1():
    message = """
        Use the following commands correctly as specified below:
    
        rectangle : takes in three commands: side1, side2, operation. Side1 is one of the sides of the rectangle and side2 is the length of the adjacent side. Operation Takes two commands:
        Enter 'area': in order to get the area of the rectangle
        Enter 'perimeter': calculates the perimeter of the rectangle
    
        circle : takes in two commands : radius, operation. Radius is the length of the radius of the circle. Operation takes in two commands: 'circumference' and 'area'
        Circumference will calculate the circumference of the circle
        Area will calculate the area of the circle
    
        triangle : takes in three commands: base, height, operation. Base is the lenght of the base of the triangle. Height is the length of the triangle.
        Operation takes in one command: 'area': it calculates the area of a triangle
    
        pythagorean : takes three commands: a, b, c. A and b are the lengths of the side of the right triangle. C in the hypotenuse of the triangle.
        If you are trying to find a length for one of the side enter 'x' for that length variable.
        If you are trying to check if the triangle lengths form a proper right triangle, enter all three varaibles as numbers.

        fraction : takes 3 three commands: fraction1, fraction2, operation. Fraction1 and fraction2 are the fractions that the operation will be performed on. Operation is the type of operation.
        Enter the fractions as "numerator/denominator", where numerator is the numerator value and the denominator is the denominator value.
        Operation is going to ask the type of operation to perform. There is "LCD", "GCD", "Add", "Subtract", "Multiply", and "Divide"
        LCD - finds the Least Common Denominator
        GCD - finds the Greatest Common Denominator
        The rest solve the operations and return in simplest form.
        """
    return message


def message2():
    message = """
        equation : take in one command: simple. Simple is a string of the equation that is passed in by the user.
        Enter the equation with no variables and with spaces in between the operators and digits.
        Such as "1 + 3 + 2 * ( 2 * 3 ) ^ 2"
        It will take in the equation and correctly return the answer using proper order of operations.
    
        algebra : take in two commands : equation and answer. Equation is the equation that the user has to input in algebra. Answer is the type of algebra you want the program to perform.
        Enter the equation as such "y = 12x - 13" or "y = 12x - 12x + 13"
        answer has two types "slope" and "simplify"
        slope - will return the intercept and the slope
        simplify - will simplify the algebra equation that was entered (addition and subtraction only)
        quadratic - will take in a quadratic in the following form, Ex: '- 12x^2 + 12x - 13'
        
        polynomialtwo : takes in two commands: equation1 and equation2 are both equation that have two variables 'x' and 'y'
        Enter the equations in the following form 'ax + by = c' and Ex. '- 12x + 13y = -35'.
        """
    return message


def areaRectangle(side1, side2):
    side1 = float(side1)
    side2 = float(side2)
    result = side1 * side2
    return float(result)


def perimeterRectangle(side1, side2):
    side1 = float(side1)
    side2 = float(side2)
    result = (side1 * 2) + (side2 * 2)
    return float(result)


def areaTriangle(base, height):
    base = float(base)
    height = float(height)
    result = (base * height) / 2
    return float(result)


def areaCircle(radius):
    radius = float(radius)
    result = math.pi * (radius ** 2)
    return float(result)


def circumferenceCircle(radius):
    radius = float(radius)
    result = 2 * math.pi * radius
    return float(result)


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


def gcd_values(value1, value2):
    while value2 != 0:
        value1, value2 = value2, value1 % value2
    return int(value1) 


def lcd_values(value1, value2):
    greatest = gcd_values(value1, value2)
    least = (value1 * value2) / greatest
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

    
def quadratic(equation):
    count = 0
    a = 0
    b = 0
    c = 0
    while count < len(equation):
        if type(equation[count]) is tuple:
            print(equation[count])
            if (equation[count][1] == 'x') and (equation[count][2] == '2'):
                print(count)
                if (count == 1) and (equation[count - 1] == '-'):
                    a = (-1) * float(equation[count][0])
                else:
                    a = float(equation[count][0])
                print(a)
            elif (equation[count][1] == 'x') and (equation[count][2] == None):
                if equation[count - 1] == '-':
                    b = -1 * float(equation[count][0])
                else:
                    b = float(equation[count][0])
            elif (equation[count][1] == None) and (equation[count][2] == None):
                if equation[count - 1] == '-':
                    c = -1 * float(equation[count][0])
                else:
                    c = float(equation[count][0])
        count = count + 1
    
    answer1 = ((-1 * b) + (((b * b) - (4 * a * c)) ** 0.5)) / (2 * a)
    answer2 = ((-1 * b) - (((b * b) - (4 * a * c)) ** 0.5)) / (2 * a)
    
    print(answer1, answer2)
    
    print(a, b, c)
    return (answer1, answer2)
    

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
   
    
def multiplyPoly(x, y, number, multiple):
    x *= multiple
    y *= multiple
    number *= multiple
    return x, y, number


def subtractPoly(x_eq1, x_eq2, y_eq1, y_eq2, number_eq1, number_eq2):
    x_result = x_eq1 - x_eq2
    y_result = y_eq1 - y_eq2
    number_result = number_eq1 - number_eq2
    print(x_result, y_result, number_result)
    return x_result, y_result, number_result
 
    
def addPoly(x_eq1, x_eq2, y_eq1, y_eq2, number_eq1, number_eq2):
    x_result = x_eq1 + x_eq2
    y_result = y_eq1 + y_eq2
    number_result = number_eq1 + number_eq2
    print(x_result, y_result, number_result)
    return x_result, y_result, number_result        

    
def polynomialTwo(equation1, equation2):
    print(equation1)
    print(equation2)
    count = 0
    x_eq1 = 0
    x_eq2 = 0
    y_eq1 = 0
    y_eq2 = 0
    number_eq1 = 0
    number_eq2 = 0
    while count < len(equation1):
        if type(equation1[count]) is tuple:
            if equation1[count][1] == 'x':
                if (count >= 1) and (equation1[count - 1] == '-'):
                    x_eq1 = (-1) * float(equation1[count][0])
                else:
                    x_eq1 = float(equation1[count][0])
            elif equation1[count][1] == 'y':
                if (count >= 1) and (equation1[count - 1] == '-'):
                    y_eq1 = (-1) * float(equation1[count][0])
                else:
                    y_eq1 = float(equation1[count][0])
            else:
                if (count >= 1) and (equation1[count - 1] == '-'):
                    number_eq1 = (-1) * float(equation1[count][0])
                else:
                    number_eq1 = float(equation1[count][0])
        count += 1
    count = 0
    print(x_eq1, y_eq1, number_eq1)
    while count < len(equation2):
        if type(equation2[count]) is tuple:
            if equation2[count][1] == 'x':
                if (count >= 1) and (equation2[count - 1] == '-'):
                    x_eq2 = (-1) * float(equation2[count][0])
                else:
                    x_eq2 = float(equation2[count][0])
            elif equation2[count][1] == 'y':
                if (count >= 1) and (equation2[count - 1] == '-'):
                    y_eq2 = (-1) * float(equation2[count][0])
                else:
                    y_eq2 = float(equation2[count][0])
            else:
                if (count >= 1) and (equation2[count - 1] == '-'):
                    number_eq2 = (-1) * float(equation2[count][1])
                else:
                    number_eq2 = float(equation2[count][0])
        count += 1
    print(x_eq2, y_eq2, number_eq2) 
    
          
    x_lcd = lcd_values(abs(x_eq1), abs(x_eq2))
    if (x_lcd / abs(x_eq1)) != 1:
        x_eq1, y_eq1, number_eq1 = multiplyPoly(x_eq1, y_eq1, number_eq1, x_lcd / abs(x_eq1))
    if (x_lcd / abs(x_eq2)) != 1:
        x_eq2, y_eq2, number_eq2 = multiplyPoly(x_eq2, y_eq2, number_eq2, x_lcd / abs(x_eq2))
        
    if ((x_eq1 < 0) and (x_eq2 < 0)) or ((x_eq1 > 0) and (x_eq2 > 0)):
        x_result, y_result, number_result =  subtractPoly(x_eq1, x_eq2, y_eq1, y_eq2, number_eq1, number_eq2)
    else:
        x_result, y_result, number_result = addPoly(x_eq1, x_eq2, y_eq1, y_eq2, number_eq1, number_eq2)
    
    if(x_result == 0) and (y_result == 0):
        return(0, 0)
    
    y = number_result / y_result
    if y_eq1 < 0:
        result = number_eq1 - (y * y_eq1)
    else:
        result = number_eq1 + (y * y_eq1)
    x = result / x_eq1
    
    
    print("Y : ", y)
    print("X : ", x)
    
    return (x, y)
    

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