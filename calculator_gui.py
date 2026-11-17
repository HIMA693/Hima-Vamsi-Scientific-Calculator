
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import math

# ==========================================
# HIMA VAMSI SCIENTIFIC CALCULATOR
# Version 2.0
# ==========================================


# 1. MAIN WINDOW

root = tk.Tk()

root.title("Hima Vamsi Scientific Calculator")
root.geometry("440x850")
root.configure(bg="#101827")
root.resizable(False, False)


# 2. HISTORY FILE LOCATION

HISTORY_FILE = Path(__file__).with_name(
    "calculator_history.txt"
)


# 3. CALCULATION STATE

state = {
    "first": None,
    "operator": None
}


# 4. HEADING

heading = tk.Label(
    root,
    text="HIMA VAMSI CALCULATOR",
    font=("Arial", 17, "bold"),
    bg="#101827",
    fg="#06B6D4"
)

heading.pack(pady=10)


# 5. DISPLAY SCREEN

display = tk.Entry(
    root,
    font=("Arial", 28, "bold"),
    justify="right",
    bg="#E2E8F0",
    fg="#101827",
    bd=0,
    relief="flat"
)

display.pack(
    padx=15,
    pady=10,
    fill="x",
    ipady=14
)


# 6. NUMBER FORMATTING

def format_number(value):

    return f"{value:g}"


# 7. NUMBER INPUT FUNCTION

def number_click(value):

    current = display.get()

    if value == ".":

        if "." in current:
            return

        if current == "":
            display.insert(tk.END, "0")

    display.insert(tk.END, value)


# 8. OPERATOR FUNCTION

def choose_operator(symbol):

    try:

        state["first"] = float(display.get())

    except ValueError:

        return

    state["operator"] = symbol

    display.delete(0, tk.END)


# 9. CLEAR FUNCTION

def clear_display():

    display.delete(0, tk.END)

    state["first"] = None
    state["operator"] = None


# 10. BACKSPACE FUNCTION

def backspace():

    current = display.get()

    display.delete(0, tk.END)

    display.insert(0, current[:-1])


# 11. SAVE HISTORY FUNCTION

def save_history(expression):

    try:

        with open(
            HISTORY_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(expression + "\n")

    except OSError as error:

        messagebox.showerror(
            "Save Error",
            str(error)
        )


# 12. LOAD HISTORY FUNCTION

def load_history():

    try:

        if HISTORY_FILE.exists():

            with open(
                HISTORY_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:

                    history_list.insert(
                        tk.END,
                        line.rstrip("\r\n")
                    )

    except OSError as error:

        messagebox.showerror(
            "History Error",
            str(error)
        )


# 13. CLEAR HISTORY FUNCTION

def clear_history():

    answer = messagebox.askyesno(
        "Clear History",
        "Delete all calculation history?"
    )

    if answer:

        try:

            HISTORY_FILE.write_text(
                "",
                encoding="utf-8"
            )

            history_list.delete(
                0,
                tk.END
            )

        except OSError as error:

            messagebox.showerror(
                "Delete Error",
                str(error)
            )


# 14. SHOW RESULT FUNCTION

def show_result(expression, result):

    result = round(result, 10)

    record = (
        f"{expression} = {format_number(result)}"
    )

    save_history(record)

    history_list.insert(
        tk.END,
        record
    )

    history_list.see(tk.END)

    display.delete(0, tk.END)

    display.insert(
        tk.END,
        format_number(result)
    )


# 15. BASIC CALCULATION FUNCTION

def calculate():

    try:

        second = float(display.get())

        first = state["first"]
        operator = state["operator"]

        if first is None or operator is None:
            return

        if operator == "+":

            result = first + second

        elif operator == "-":

            result = first - second

        elif operator == "*":

            result = first * second

        elif operator == "/":

            if second == 0:
                raise ZeroDivisionError

            result = first / second

        elif operator == "%":

            if second == 0:
                raise ZeroDivisionError

            result = first % second

        elif operator == "**":

            result = first ** second

            if isinstance(result, complex):
                raise ValueError

        expression = (
            f"{format_number(first)} "
            f"{operator} "
            f"{format_number(second)}"
        )

        show_result(expression, result)

        state["first"] = None
        state["operator"] = None

    except ZeroDivisionError:

        clear_display()

        display.insert(
            tk.END,
            "Cannot divide by zero"
        )

    except (ValueError, TypeError, OverflowError):

        clear_display()

        display.insert(
            tk.END,
            "Invalid Input"
        )


# 16. SCIENTIFIC RESULT FUNCTION

def scientific_calculation(name, function):

    try:

        number = float(display.get())

        result = function(number)

        show_result(
            f"{name}({format_number(number)})",
            result
        )

    except ValueError:

        clear_display()

        display.insert(
            tk.END,
            "Invalid Input"
        )

    except (OverflowError, TypeError):

        clear_display()

        display.insert(
            tk.END,
            "Calculation Error"
        )


# 17. SQUARE ROOT FUNCTION

def square_root():

    scientific_calculation(
        "√",
        math.sqrt
    )


# 18. SQUARE FUNCTION

def square():

    scientific_calculation(
        "Square",
        lambda number: number ** 2
    )


# 19. FACTORIAL FUNCTION

def factorial():

    def calculate_factorial(number):

        if number < 0 or not number.is_integer():

            raise ValueError

        return math.factorial(int(number))

    scientific_calculation(
        "Factorial",
        calculate_factorial
    )


# 20. HISTORY HEADING

history_label = tk.Label(
    root,
    text="CALCULATION HISTORY",
    font=("Arial", 11, "bold"),
    bg="#101827",
    fg="#06B6D4"
)

history_label.pack(pady=5)


# 21. HISTORY LIST

history_list = tk.Listbox(
    root,
    height=4,
    font=("Arial", 11),
    bg="#263449",
    fg="#FFFFFF",
    bd=0,
    relief="flat"
)

history_list.pack(
    padx=15,
    pady=5,
    fill="x"
)


# 22. CLEAR HISTORY BUTTON

clear_history_button = tk.Button(
    root,
    text="CLEAR HISTORY",
    font=("Arial", 9, "bold"),
    bg="#DC2626",
    fg="#FFFFFF",
    relief="flat",
    cursor="hand2",
    command=clear_history
)

clear_history_button.pack(pady=5)


# 23. LOAD OLD HISTORY

load_history()


# 24. BUTTON FRAME

button_frame = tk.Frame(
    root,
    bg="#101827"
)

button_frame.pack(
    padx=10,
    pady=10,
    fill="both",
    expand=True
)


# 25. BUTTON LAYOUT

buttons = [

    ("√", 0, 0),
    ("x²", 0, 1),
    ("n!", 0, 2),
    ("C", 0, 3),

    ("⌫", 1, 0),
    ("%", 1, 1),
    ("÷", 1, 2),
    ("×", 1, 3),

    ("7", 2, 0),
    ("8", 2, 1),
    ("9", 2, 2),
    ("-", 2, 3),

    ("4", 3, 0),
    ("5", 3, 1),
    ("6", 3, 2),
    ("+", 3, 3),

    ("1", 4, 0),
    ("2", 4, 1),
    ("3", 4, 2),
    ("xʸ", 4, 3),

    ("0", 5, 0),
    (".", 5, 1),
    ("=", 5, 2)

]


# 26. CREATE BUTTONS

for (text, row, column) in buttons:

    if text in "0123456789.":

        command = lambda value=text: number_click(value)

        bg_color = "#263449"
        fg_color = "#FFFFFF"

    elif text == "√":

        command = square_root

        bg_color = "#0891B2"
        fg_color = "#FFFFFF"

    elif text == "x²":

        command = square

        bg_color = "#0891B2"
        fg_color = "#FFFFFF"

    elif text == "n!":

        command = factorial

        bg_color = "#0891B2"
        fg_color = "#FFFFFF"

    elif text in ["+", "-", "×", "÷", "%", "xʸ"]:

        symbol = {
            "×": "*",
            "÷": "/",
            "xʸ": "**"
        }.get(text, text)

        command = lambda value=symbol: choose_operator(value)

        bg_color = "#06B6D4"
        fg_color = "#FFFFFF"

    elif text == "=":

        command = calculate

        bg_color = "#16A34A"
        fg_color = "#FFFFFF"

    elif text == "C":

        command = clear_display

        bg_color = "#DC2626"
        fg_color = "#FFFFFF"

    else:

        command = backspace

        bg_color = "#475569"
        fg_color = "#FFFFFF"

    tk.Button(

        button_frame,

        text=text,

        font=("Arial", 16, "bold"),

        width=5,
        height=2,

        bg=bg_color,
        fg=fg_color,

        activebackground="#0891B2",
        activeforeground="#FFFFFF",

        relief="flat",
        bd=0,

        cursor="hand2",

        command=command

    ).grid(

        row=row,
        column=column,

        padx=4,
        pady=4,

        sticky="nsew"

    )


# 27. GRID SETTINGS

for column in range(4):

    button_frame.grid_columnconfigure(
        column,
        weight=1
    )

for row in range(6):

    button_frame.grid_rowconfigure(
        row,
        weight=1
    )


# 28. KEYBOARD SUPPORT

def keyboard_input(event):

    key = event.keysym
    char = event.char

    if char and char in "0123456789.":

        number_click(char)

        return "break"

    elif char and char in ["+", "-", "*", "/", "%"]:

        choose_operator(char)

        return "break"

    elif char == "^":

        choose_operator("**")

        return "break"

    elif key in ["Return", "KP_Enter"]:

        calculate()

        return "break"

    elif key == "BackSpace":

        backspace()

        return "break"

    elif key == "Escape":

        clear_display()

        return "break"


# 29. CONNECT KEYBOARD

root.bind_all(
    "<Key>",
    keyboard_input
)


# 30. RUN APPLICATION

root.mainloop()
