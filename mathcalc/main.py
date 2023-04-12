import importlib.util
#import generated as func

spec = importlib.util.spec_from_file_location("math", "./math.py")
math = importlib.util.module_from_spec(spec)
spec.loader.exec_module(math)

#spec = importlib.util.spec_from_file_location("generated", "./generated.py")
#func = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(func)


equation = "y = 12x - 12x - 31"
equation = list(equation.split(" "))
result = math.tupleList(equation)
#print(result)
print(math.algebraSimplify(result))
#eq_str = '2*x + 3*y - 4*z + 2.5*x**2 - 1.5*y**2 + 0.5*z**3 - 5 = 0'
#eq_simp_str = func.simplify_equation(eq_str)
#print(eq_simp_str)  # Output: 5.0*z**3/2 + 5.0*x**2/4 - 3.0*y**2/4 + 2*x + 3*y - 7*z + 5 = 0