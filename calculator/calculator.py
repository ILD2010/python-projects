"""Python calculator is a GUI based code, that gives the user a modern appearing calculator.
   featuring:
   - unit conversions
   - basic calculations
   - memory functions
   _ user friendly design
   """


import tkinter as tk
from tkinter import ttk, messagebox
import ast
import operator


# CALCULATOR SETUP

root = tk.Tk()
root.title("Smart Calculator")
root.geometry("400x580")
root.configure(bg="#202020")

memory = 0


# CALCULATION FUNCTION

def calculate(expression):

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod
    }

    def solve(node):

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.BinOp):

            left = solve(node.left)
            right = solve(node.right)

            operation = operations.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):

            if isinstance(node.op, ast.USub):
                return -solve(node.operand)

            if isinstance(node.op, ast.UAdd):
                return solve(node.operand)

        raise ValueError("Invalid expression")

    tree = ast.parse(expression, mode="eval")

    return solve(tree.body)


# BASIC BUTTON FUNCTIONS

def button_click(value):

    entry.insert(tk.INSERT, value)


def clear():

    entry.delete(0, tk.END)


def backspace():

    position = entry.index(tk.INSERT)

    if position > 0:
        entry.delete(position - 1, position)


def get_result(event=None):

    try:

        expression = entry.get()

        result = calculate(expression)

        clear()

        entry.insert(0, str(result))

    except Exception:

        clear()

        entry.insert(0, "Error")


# MEMORY FUNCTIONS

def get_current_value():

    return calculate(entry.get())


def memory_store():

    global memory

    try:
        memory = get_current_value()
        memory_label.config(text=f"Memory: {memory}")

    except Exception:
        messagebox.showerror(
            "Memory Error",
            "Enter a valid number or calculation."
        )


def memory_recall():

    clear()
    entry.insert(0, str(memory))


def memory_clear():

    global memory

    memory = 0

    memory_label.config(text="Memory: 0")


def memory_add():

    global memory

    try:

        memory += get_current_value()

        memory_label.config(text=f"Memory: {memory}")

    except Exception:

        messagebox.showerror(
            "Memory Error",
            "Invalid calculation."
        )


def memory_subtract():

    global memory

    try:

        memory -= get_current_value()

        memory_label.config(text=f"Memory: {memory}")

    except Exception:

        messagebox.showerror(
            "Memory Error",
            "Invalid calculation."
        )


# UNIT CONVERTER WINDOW

def open_converter():

    converter = tk.Toplevel(root)

    converter.title("Unit Converter")
    converter.geometry("420x420")
    converter.configure(bg="#202020")

    # Conversion categories

    conversions = {

        "Length": {
            "Meters": 1,
            "Kilometers": 1000,
            "Centimeters": 0.01,
            "Miles": 1609.344,
            "Feet": 0.3048,
            "Inches": 0.0254
        },

        "Weight": {
            "Kilograms": 1,
            "Grams": 0.001,
            "Pounds": 0.45359237,
            "Ounces": 0.028349523125
        },

        "Volume": {
            "Liters": 1,
            "Milliliters": 0.001,
            "Gallons (US)": 3.785411784,
            "Cups (US)": 0.2365882365
        },

        "Temperature": {
            "Celsius": 1,
            "Fahrenheit": 1,
            "Kelvin": 1
        }
    }

    # Title

    tk.Label(
        converter,
        text="Unit Converter",
        font=("Arial", 22, "bold"),
        bg="#202020",
        fg="white"
    ).pack(pady=15)

    # Category selection

    category = ttk.Combobox(
        converter,
        values=list(conversions.keys()),
        state="readonly"
    )

    category.pack(pady=10)
    category.set("Length")

    # Input value

    value_entry = tk.Entry(
        converter,
        font=("Arial", 18),
        justify="center"
    )

    value_entry.pack(pady=10)

    value_entry.insert(0, "1")

    # Unit selectors

    from_unit = ttk.Combobox(
        converter,
        state="readonly"
    )

    from_unit.pack(pady=5)

    to_unit = ttk.Combobox(
        converter,
        state="readonly"
    )

    to_unit.pack(pady=5)

    # Result label

    result_label = tk.Label(
        converter,
        text="",
        font=("Arial", 18),
        bg="#202020",
        fg="#00ff88"
    )

    result_label.pack(pady=15)

    # Update available units

    def update_units(event=None):

        units = list(conversions[category.get()].keys())

        from_unit["values"] = units
        to_unit["values"] = units

        from_unit.set(units[0])
        to_unit.set(units[1])

        result_label.config(text="")

    # Temperature conversion

    def convert_temperature(value, source, target):

        if source == "Celsius":
            celsius = value

        elif source == "Fahrenheit":
            celsius = (value - 32) * 5 / 9

        else:
            celsius = value - 273.15

        if target == "Celsius":
            return celsius

        elif target == "Fahrenheit":
            return celsius * 9 / 5 + 32

        else:
            return celsius + 273.15

    # Main conversion function

    def convert():

        try:

            value = float(value_entry.get())

            selected_category = category.get()

            source = from_unit.get()
            target = to_unit.get()

            if selected_category == "Temperature":

                result = convert_temperature(
                    value,
                    source,
                    target
                )

            else:

                factors = conversions[selected_category]

                base_value = value * factors[source]

                result = base_value / factors[target]

            result_label.config(
                text=f"Result: {result:.6g}"
            )

        except ValueError:

            messagebox.showerror(
                "Conversion Error",
                "Please enter a valid number."
            )

    category.bind("<<ComboboxSelected>>", update_units)

    update_units()

    # Convert button

    tk.Button(
        converter,
        text="Convert",
        font=("Arial", 16),
        bg="#007acc",
        fg="white",
        command=convert
    ).pack(pady=10)


# TOP MENU

menu_bar = tk.Menu(root)

tools_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

tools_menu.add_command(
    label="Unit Converter",
    command=open_converter
)

tools_menu.add_separator()

tools_menu.add_command(
    label="Exit",
    command=root.destroy
)

menu_bar.add_cascade(
    label="Tools",
    menu=tools_menu
)

root.config(menu=menu_bar)


# CALCULATOR DISPLAY

title = tk.Label(
    root,
    text="SMART CALCULATOR",
    font=("Arial", 20, "bold"),
    bg="#202020",
    fg="white"
)

title.pack(pady=10)


entry = tk.Entry(
    root,
    font=("Arial", 26),
    bg="#303030",
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)

entry.pack(
    fill="x",
    padx=15,
    pady=10,
    ipady=15
)


# Memory display

memory_label = tk.Label(
    root,
    text="Memory: 0",
    font=("Arial", 12),
    bg="#202020",
    fg="#00ff88"
)

memory_label.pack()


# BUTTON FRAME

frame = tk.Frame(
    root,
    bg="#202020"
)

frame.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


# MEMORY BUTTONS

memory_buttons = [
    ("MC", memory_clear),
    ("MR", memory_recall),
    ("MS", memory_store),
    ("M+", memory_add),
    ("M-", memory_subtract)
]

for index, (text, command) in enumerate(memory_buttons):

    button = tk.Button(
        frame,
        text=text,
        font=("Arial", 12),
        bg="#505050",
        fg="white",
        command=command
    )

    button.grid(
        row=0,
        column=index,
        sticky="nsew",
        padx=2,
        pady=3
    )

# CALCULATOR BUTTONS

buttons = [

    ["7", "8", "9", "/", "⌫"],

    ["4", "5", "6", "*", "C"],

    ["1", "2", "3", "-", "("],

    ["0", ".", "=", "+", ")"],

    ["**", "%", "00", "", ""]

]


for row_index, row in enumerate(buttons):

    for col_index, value in enumerate(row):

        if value == "":
            continue

        if value == "=":
            command = get_result

        elif value == "C":
            command = clear

        elif value == "⌫":
            command = backspace

        else:
            command = lambda v=value: button_click(v)

        button = tk.Button(
            frame,
            text=value,
            font=("Arial", 18),
            bg="#404040",
            fg="white",
            activebackground="#606060",
            command=command
        )

        button.grid(
            row=row_index + 1,
            column=col_index,
            sticky="nsew",
            padx=3,
            pady=3
        )


for row in range(6):
    frame.rowconfigure(row, weight=1)

for col in range(5):
    frame.columnconfigure(col, weight=1)


# KEYBOARD SHORTCUTS

root.bind("<Return>", get_result)


# START APPLICATION

entry.focus_set()

root.mainloop()
