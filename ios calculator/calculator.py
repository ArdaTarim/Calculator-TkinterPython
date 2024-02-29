import customtkinter as ctk
import darkdetect

# SETTINGS #

# size
APP_SIZE = (400,700)
MAIN_ROWS = 7
MAIN_COLUMNS = 4

# Text
FONT = 'Helvetica'
OUTPUT_FONT_SIZE = 70
NORMAL_FONT_SIZE = 32

STYLING = {
	'gap': 0.5,
	'corner-radius': 0}

NUM_POSITIONS = {
	'.': {'col': 2, 'row': 6, 'span': 1},
	0: {'col': 0, 'row': 6, 'span': 2},
	1: {'col': 0, 'row': 5, 'span': 1},
	2: {'col': 1, 'row': 5, 'span': 1},
	3: {'col': 2, 'row': 5, 'span': 1},
	4: {'col': 0, 'row': 4, 'span': 1},
	5: {'col': 1, 'row': 4, 'span': 1},
	6: {'col': 2, 'row': 4, 'span': 1},
	7: {'col': 0, 'row': 3, 'span': 1},
	8: {'col': 1, 'row': 3, 'span': 1},
	9: {'col': 2, 'row': 3, 'span': 1}}

MATH_POSITIONS = {
	'/': {'col': 3, 'row': 2, 'character':'÷', 'image path': {'light': 'images/divide_light.png', 'dark': 'images/divide_dark.png'}},
	'*': {'col': 3, 'row': 3, 'character':'x', 'image path': None},
	'-': {'col': 3, 'row': 4, 'character':'-', 'image path': None},
	'=': {'col': 3, 'row': 6, 'character':'=', 'image path': None},
	'+': {'col': 3, 'row': 5, 'character':'+', 'image path': None},
	}

OPERATORS = {
	'clear':   {'col': 0, 'row': 2, 'text': 'AC', 'image path': None},
	'invert':  {'col': 1, 'row': 2, 'text': '-/+', 'image path': {'light': 'images/invert_light.png', 'dark': 'images/invert_dark.png'}},
	'percent': {'col': 2, 'row': 2, 'text': '%', 'image path': None}}

COLORS = {
	'light-gray': {'fg': ('#505050','#D4D4D2'), 'hover': ('#686868','#efefed'), 'text': ('white','black')},
	'dark-gray': {'fg': ('#D4D4D2', '#505050'), 'hover': ('#efefed','#686868'), 'text': ('black','white')},
	'orange': {'fg': '#FF9500', 'hover': '#ffb143', 'text': ('black','white')},
	'orange-highlight': {'fg': 'white', 'hover': 'white', 'text': ('black','#FF9500')}}

TITLE_BAR_HEX_COLORS = {
	'dark': 0x00000000,
	'light': 0x00EEEEEE}

BLACK = '#000000'
WHITE = '#EEEEEE'

class Calculator(ctk.CTk):
    def __init__(self, is_dark):

        # SETUP
        super().__init__(
            fg_color= (WHITE, BLACK),
        )
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable(False, False)
        self.title("")

        # LAYOUT
        self.columnconfigure((0,1,2,3), weight= 1, uniform= "a")
        self.rowconfigure((0,1,2,3,4,5,6), weight= 1, uniform= "a")

        # DATA
        self.result_string = ctk.StringVar(value= "0")
        self.formula_string = ctk.StringVar(value= "")
        self.dispay_nums = []
        self.full_operation = []

        # WİDGETS
        self.create_widgets()

        self.mainloop()
        
    def create_widgets(self):

        # FONTS 
        main_font = ctk.CTkFont(FONT, size= NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(FONT, size= OUTPUT_FONT_SIZE)

        # OUTPUT LABELS
        OutputLabel(self, 0, "se", main_font, self.formula_string)
        OutputLabel(self, 1, "e", result_font, self.result_string)

        # AC BUTTON
        Button(self,
               text= OPERATORS["clear"]["text"], 
               func = self.clear,
               col = OPERATORS["clear"]["col"], 
               row = OPERATORS["clear"]["row"],
               font = main_font)

        # PERCENTAGE BUTTON
        Button(self,
               text= OPERATORS["percent"]["text"],
               func = self.percent,
               col = OPERATORS["percent"]["col"], 
               row = OPERATORS["percent"]["row"],
               font = main_font)

        # INVERT BUTTON
        Button(self,
               text= OPERATORS["invert"]["text"],
               func = self.invert,
               col = OPERATORS["invert"]["col"], 
               row = OPERATORS["invert"]["row"],
               font = main_font)
        
        # NUMBER BUTTONS
        for num, data in NUM_POSITIONS.items():
            NumButton(
                parent = self, 
                text = num, 
                func = self.num_press, 
                col = data["col"], 
                row = data["row"], 
                font = main_font,
                span= data["span"])
            
        # MATH BUTTONS
        for operator, data in MATH_POSITIONS.items():
            MathButton(
                parent = self, 
                text = data["character"], 
                func = self.math_press, 
                col = data["col"], 
                row = data["row"], 
                font = main_font,
                operator = operator
                )

    def clear(self):
        print("clear")
        self.result_string.set(0)
        self.formula_string.set("")
        self.dispay_nums.clear()
        self.full_operation.clear()

    def percent(self):
        print("percent")
        if self.dispay_nums:
            current_number = float("".join(self.dispay_nums))
            number = current_number/100
            
            self.dispay_nums = list(str(number))
            self.result_string.set("".join(self.dispay_nums))

    def invert(self):
        print("invert")
        current_number = "".join(self.dispay_nums)
        if current_number:
            if float(current_number) > 0:
                self.dispay_nums.insert(0, "-")
            else:
                del self.dispay_nums[0]

            self.result_string.set("".join(self.dispay_nums))

    def num_press(self, value):
        self.dispay_nums.append(str(value))
        full_number = "".join(self.dispay_nums)
        self.result_string.set(full_number)
        print(full_number)

    def math_press(self, value):
        current_number = "".join(self.dispay_nums)

        if current_number:
            self.full_operation.append(current_number)
            if value != "=":
                self.full_operation.append(value)
                self.dispay_nums.clear()
                self.result_string.set("")
                self.formula_string.set(" ".join(self.full_operation))
                print(self.full_operation)
            else:
                formula = " ".join(self.full_operation)
                try:
                    result = eval(formula)
                except:
                    self.clear()
                    self.result_string.set("ERROR")

                # formattin result
                if isinstance(result, float):

                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 4)

                self.full_operation.clear()
                self.dispay_nums = [str(result)]

                self.result_string.set(result)
                self.formula_string.set(formula)
                print(eval(formula))
    
class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(
            master= parent,
            text= "123",
            font= font,
            textvariable = string_var,
        )
        self.grid(column= 0, columnspan= 4, row= row, sticky= anchor, padx= 10)

class Button(ctk.CTkButton):
    def __init__(self, parent, text, func, col, row, font, span = 1, color = "dark-gray"):
        super().__init__(
            master = parent,
            command = func,
            text = text,
            font = font,
            corner_radius = STYLING["corner-radius"],
            fg_color = COLORS[color]["fg"],
            hover_color = COLORS[color]["hover"],
            text_color = COLORS[color]["text"]
        )
        self.grid(column= col, columnspan= span, row= row, sticky= "nsew", padx = STYLING["gap"], pady = STYLING["gap"])

class NumButton(Button):
    def __init__(self, parent, text, func, col, row, font, span, color = "light-gray"):
        super().__init__(
            parent= parent,
            text= text,
            func= lambda: func(text),
            col= col,
            row= row,
            font= font,
            color= color,
            span= span
        )

class MathButton(Button):
    def __init__(self, parent, text, func, col, row, operator, font, color = "orange"):
        super().__init__(
            parent= parent,
            text= text,
            func= lambda: func(operator),
            col= col,
            row= row,
            font= font,
            color= color
        )

if __name__ == "__main__":
    Calculator(darkdetect.isDark)
