import importlib.util
#import generated as func

spec = importlib.util.spec_from_file_location("math", "./math.py")
math = importlib.util.module_from_spec(spec)
spec.loader.exec_module(math)

#spec = importlib.util.spec_from_file_location("generated", "./generated.py")
#func = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(func)


#equation = "y + 3 = 3 - 12x - 3"
#equation = "y + 3 = 12x"
#equation = "x - 2 = x"

#equation = list(equation.split(" "))
#result = math.tupleList(equation)
#print(result)
#print(math.algebraSimplify(result))
#eq_str = '2*x + 3*y - 4*z + 2.5*x**2 - 1.5*y**2 + 0.5*z**3 - 5 = 0'
#eq_simp_str = func.simplify_equation(eq_str)
#print(eq_simp_str)  # Output: 5.0*z**3/2 + 5.0*x**2/4 - 3.0*y**2/4 + 2*x + 3*y - 7*z + 5 = 0


#Below is the fraction testing
fraction1 = "1/8"
fraction2 = "2/12"
#math.gcd(fraction1, fraction2)
result = math.addFraction(fraction1, fraction2)
print(result)
#7/24

result = math.subtractFraction(fraction1, fraction2)
print(result)
#-1/24

result = math.multiplyFraction(fraction1, fraction2)
print(result)
#1/48

result = math.divideFraction(fraction1, fraction2)
print(result)
#3/4