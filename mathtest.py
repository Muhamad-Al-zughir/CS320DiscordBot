import mathcalc.math as math

#Testing used : pytest
#all the following tests pass
 

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_simpleCheck():
    equation = "1 + 2"
    assert math.simpleCheck(list(equation.split(" "))) == True

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_simpleCheck():
    equation = "1 + 2 )"
    assert math.simpleCheck(list(equation.split(" "))) == "Incorrect parantheses count."

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_2_simpleCheck():
    equation = "( 1 + 2 )"
    assert math.simpleCheck(list(equation.split(" "))) == True

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_3_simpleCheck():
    equation = "( 1 + 2"
    assert math.simpleCheck(list(equation.split(" "))) == "Incorrect parantheses count."

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_4_simpleCheck():
    equation = "1 + 2 ) ("
    assert math.simpleCheck(list(equation.split(" "))) == "Incorrect parantheses placement"

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_slope():
    equation = "y = 12x - 2"
    assert math.slope(list(equation.split(" ")), "slope") == ('12', -2.0)

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_slope():
    equation = "y = 12x - -2"
    assert math.slope(list(equation.split(" ")), "slope") == ('12', 2.0)

# This test is a Black Box Testing 
# Equivalence Partitioning  
def test_checker():
    equation = "( 2 * 2 + 2 ) / 2"
    assert math.checker(list(equation.split(" "))) == 3.0    
    
# This is a White Box Testing
#def checker(equation):
#    while '(' in equation:
#        first_node = -1
#        second_node = 0
#        part_equation = []
#        count = 0
#        paranthesis_count = 0
#        while (paranthesis_count != 0) or (first_node == -1):
#            if (equation[count] == '(') and (first_node == -1):
#                first_node = count
#                paranthesis_count += 1
#            elif equation[count] == '(':
#                paranthesis_count += 1
#            elif equation[count] == ')':
#                paranthesis_count -= 1
#            count += 1
#        first_node += 1
#        second_node = count - 2
#        count = first_node
#        while count != second_node:
#            part_equation.append(equation[count])
#            count += 1
#        part_equation.append(equation[count])
#        result = checker(part_equation)
#        count = first_node - 1
#        second_node += 1
#        while count != second_node:
#            equation.pop(count)
#            second_node -= 1
#        equation[count] = str(result)
#    if '^' in equation:
#        equation = exponent(equation)
#    if ('*' in equation) or ('/' in equation):
#        equation = multdiv(equation)
#    if '+' in equation:
#        equation = add(equation)
#    if '-' in equation:
#        equation = subtract(equation)
#    return equation[0]

def test_1_checker():
    equation = "( 2 * 2 + 2 ) / ( ( 3 - 2 ) + 2 )"
    assert math.checker(list(equation.split(" "))) == 1       
   
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_2_checker():
    equation = "( 2 * 2 + 2 ) ^ 2"
    assert math.checker(list(equation.split(" "))) == 36.0      
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_exponent():
    equation = "2 ^ 2"
    assert math.exponent(list(equation.split(" "))) == [4.0]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_exponent():
    equation = "2 ^ 2 ^ 3"
    assert math.exponent(list(equation.split(" "))) == [64.0]

# This test is a Black Box Testing 
# Equivalence Partitioning
def test_multdiv():
    equation = "12 / 2 / 3"
    assert math.multdiv(list(equation.split(" "))) == [2.0]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_multdiv():
    equation = "12 * 2 / 3"
    assert math.multdiv(list(equation.split(" "))) == [8.0]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_add():
    equation = "23 + 12"
    assert math.add(list(equation.split(" "))) == [35]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_add():
    equation = "12.2 + 3.3"
    assert math.add(list(equation.split(" "))) == [15.5]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_subtract():
    equation = "14 - 16 - 10"
    assert math.subtract(list(equation.split(" "))) == [-12.0]
    
# This test is a Black Box Testing 
# Equivalence Partitioning
def test_1_subtract():
    equation = "14.222 - 10"
    assert math.subtract(list(equation.split(" "))) == [4.2219999999999995]
   
