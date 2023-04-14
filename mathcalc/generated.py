from sympy import simplify, Eq, symbols

def simplify_equation(eq_str):
    # Define symbols to use in the equation
    x, y, z = symbols('x y z')

    # Parse the equation string into a SymPy expression
    eq_sym = Eq(eval(eq_str))

    # Simplify the expression using SymPy
    eq_simp = simplify(eq_sym)

    # Convert the simplified expression back to a string
    eq_simp_str = str(eq_simp)

    return eq_simp_str