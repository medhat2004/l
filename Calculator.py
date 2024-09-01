from tkinter import *
import math

# Define additional mathematical functions
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Error: Division by zero."

def modulus(x, y):
    if y != 0:
        return x % y
    else:
        return "Error: Division by zero."

def square_root(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return "Error: Negative value for square root."

def absolute(x):
    return abs(x)

def average(x, y):
    return (x + y) / 2

def calculate(expression):
    """
    Evaluate a mathematical expression using custom functions.
    """
    def tokenize(expression):
        tokens = []
        number = ''
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or char == '.':
                number += char
            else:
                if number:
                    tokens.append(float(number))
                    number = ''
                if char in '+-*/%()':
                    tokens.append(char)
                elif char == 's' and expression[i:i+4] == 'sqrt':
                    tokens.append('sqrt')
                    i += 3
                elif char == 'a' and expression[i:i+3] == 'abs':
                    tokens.append('abs')
                    i += 2
                elif char == 'm' and expression[i:i+7] == 'average':
                    tokens.append('average')
                    i += 6
            i += 1
        if number:
            tokens.append(float(number))
        return tokens
    
    def evaluate(tokens):
        def operate(op, a, b=None):
            if op == '+':
                return add(a, b)
            elif op == '-':
                return subtract(a, b)
            elif op == '*':
                return multiply(a, b)
            elif op == '/':
                return divide(a, b)
            elif op == '%':
                return modulus(a, b)
            elif op == 'sqrt':
                return square_root(a)
            elif op == 'abs':
                return absolute(a)
            elif op == 'average':
                return average(a, b)
            else:
                raise ValueError("Invalid operator: " + op)

        def parse_expression():
            result = parse_term()
            while tokens and tokens[0] in ('+', '-'):
                op = tokens.pop(0)
                result = operate(op, result, parse_term())
            return result

        def parse_term():
            result = parse_factor()
            while tokens and tokens[0] in ('*', '/', '%'):
                op = tokens.pop(0)
                result = operate(op, result, parse_factor())
            return result

        def parse_factor():
            if tokens[0] == '(':
                tokens.pop(0)
                result = parse_expression()
                if tokens.pop(0) != ')':
                    raise ValueError("Mismatched parentheses.")
                return result
            elif tokens[0] in ('sqrt', 'abs', 'average'):
                func = tokens.pop(0)
                if func == 'average':
                    return operate(func, parse_factor(), parse_factor())
                return operate(func, parse_factor())
            elif tokens[0] in ('+', '-'):
                op = tokens.pop(0)
                return operate(op, 0, parse_factor())
            return tokens.pop(0)

        return parse_expression()
    
    try:
        tokens = tokenize(expression)
        result = evaluate(tokens)
        if isinstance(result, float) and result.is_integer():
            result = int(result)  # Convert to int if result is a whole number
        return result
    except Exception as e:
        return f"Error: {e}"

def click_button(value):
    current_text = e.get()
    if value == "c":
        e.delete(0, END)
    elif value == "=":
        result = calculate(current_text)
        e.delete(0, END)
        e.insert(0, result)
    else:
        e.insert(END, value)

# Create the main application window
root = Tk()
root.title("Advanced Calculator")
root.geometry("400x600")  # Increased height for better layout
root.resizable(width=0, height=0)
root.configure(bg="#333333")  # Dark background color

# Entry field
e = Entry(root, bd=10, width=28, font=("Arial", 24), bg="#FFFFFF", fg="#000000", justify='right')
e.grid(row=0, column=0, columnspan=5, pady=10, padx=10)

# Define button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
    ('0', 4, 0),
    ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3),
    ('%', 1, 4), ('sqrt', 2, 4), ('abs', 3, 4), ('average', 4, 4),
    ('c', 4, 1, 2), ('=', 4, 3, 2)
]

# Create buttons and add them to the grid
for item in buttons:
    if len(item) == 4:
        text, row, column, colspan = item
    else:
        text, row, column = item
        colspan = 1
    Button(root, text=text, font=("Arial", 18), bg="#555555", fg="#FFFFFF", bd=2, padx=20, pady=20,
           command=lambda t=text: click_button(t)).grid(row=row, column=column, columnspan=colspan, padx=5, pady=5, sticky='nsew')

# Configure grid weights to make buttons resizeable
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for j in range(5):
    root.grid_columnconfigure(j, weight=1)

# Run the application
root.mainloop()
