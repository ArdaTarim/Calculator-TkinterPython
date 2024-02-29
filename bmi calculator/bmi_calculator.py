import tkinter as tk
import customtkinter as ctk
from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = GREEN)
        self.title("")
        self.geometry("400x400")
        self.resizable(False, False)
        self.change_title_bar_color()

        # layout
        self.columnconfigure(0, weight= 1, uniform= "a")
        self.rowconfigure((0,1,2,3), weight= 2, uniform= "a")

        # data
        self.metric_bool = ctk.BooleanVar(value= True)
        self.user_height = ctk.IntVar(value= 177)
        self.user_weight = ctk.DoubleVar(value= 77)
        self.user_result = ctk.DoubleVar()
        self.update_bmi()

        # trace
        self.user_height.trace("w", self.update_bmi)
        self.user_weight.trace("w", self.update_bmi)
        self.metric_bool.trace("w", self.change_units)

        #widgets
        ResultText(self, self.user_result)
        self.weight_input = WeightInput(self, self.user_weight, self.metric_bool)
        self.height_input = HeightInput(self, self.user_height, self.metric_bool)
        UnitSwitcher(self, self.metric_bool)

        self.mainloop()

    def update_bmi(self, *args):
        height_meter = self.user_height.get() / 100
        weight_kg = self.user_weight.get()
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        self.user_result.set(bmi_result)

    def change_units(self, *args):
        self.height_input.update_text(self.user_height.get())
        self.weight_input.update_weight()

    def change_title_bar_color(self):
        pass

class ResultText(ctk.CTkLabel):
    def __init__(self, parent, user_result):
        font = ctk.CTkFont(FONT, MAIN_TEXT_SIZE, weight= "bold")
        super().__init__(
            master= parent, 
            text= 20,
            font= font,
            text_color= WHITE,
            textvariable= user_result)
        self.grid(column= 0, row= 0, rowspan = 2, sticky = "nsew")

class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, user_weight, metric_bool):
        super().__init__(master= parent, fg_color= WHITE)
        self.grid(column= 0, row= 2, sticky= "nsew", padx= 10, pady= 10)

        self.user_weight = user_weight
        self.metric_bool = metric_bool

        self.columnconfigure(0, weight= 2, uniform= "b")
        self.columnconfigure(1, weight= 1, uniform= "b")
        self.columnconfigure(2, weight= 3, uniform= "b")
        self.columnconfigure(3, weight= 1, uniform= "b")
        self.columnconfigure(4, weight= 2, uniform= "b")
        self.rowconfigure(0, weight= 1, uniform= "b")

        self.output_string = ctk.StringVar()
        self.update_weight()

        font = ctk.CTkFont(FONT, INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, 
                             text_color= BLACK,
                             font= font,
                             textvariable = self.output_string
                             )
        label.grid(row = 0, column= 2)

        minus_button = ctk.CTkButton(self, text= "-", 
                                     font= font,
                                     text_color= BLACK,
                                     fg_color= LIGHT_GRAY,
                                     hover_color= GRAY,
                                     corner_radius= BUTTON_CORNER_RADIUS,
                                     command= lambda: self.update_weight(("minus", "large")))
        minus_button.grid(row = 0, column = 0, sticky= "ns", padx= 8, pady= 8)

        plus_button = ctk.CTkButton(self, text= "+", 
                                     font= font,
                                     text_color= BLACK,
                                     fg_color= LIGHT_GRAY,
                                     hover_color= GRAY,
                                     corner_radius= BUTTON_CORNER_RADIUS,
                                     command= lambda: self.update_weight(("plus", "large")))
        plus_button.grid(row = 0, column = 4, sticky= "ns", padx= 8, pady= 8)

        small_plus_button = ctk.CTkButton(self, text= "+", 
                                     font= font,
                                     text_color= BLACK,
                                     fg_color= LIGHT_GRAY,
                                     hover_color= GRAY,
                                     corner_radius= BUTTON_CORNER_RADIUS,
                                     command= lambda: self.update_weight(("plus", "small")))
        small_plus_button.grid(row = 0, column = 3, padx= 4, pady= 4)

        small_minus_button = ctk.CTkButton(self, text= "-", 
                                     font= font,
                                     text_color= BLACK,
                                     fg_color= LIGHT_GRAY,
                                     hover_color= GRAY,
                                     corner_radius= BUTTON_CORNER_RADIUS,
                                     command= lambda: self.update_weight(("minus", "small")))
        small_minus_button.grid(row = 0, column = 1, padx= 4, pady= 4)

    def update_weight(self, info= None):
        if info:

            if self.metric_bool.get():
                amount = 1 if info[1] == "large" else 0.1
            else:
                amount = 0.453592 if info[1] == "large" else 0.453592 / 16
            
            if info[0] == "plus":
                self.user_weight.set(self.user_weight.get() + amount)
            else :
                self.user_weight.set(self.user_weight.get() - amount)

        if self.metric_bool.get():
            self.output_string.set(f"{round(self.user_weight.get(), 1)}kg")
        else:
            raw_ounces = self.user_weight.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f"{int(pounds)}lb {int(ounces)}oz")

class HeightInput(ctk.CTkFrame): 
    def __init__(self, parent, user_height, metric_bool):
        super().__init__(master= parent, fg_color= WHITE)
        self.grid(column= 0, row= 3, sticky= "nsew", padx= 10, pady= 10)

        self.metric_bool = metric_bool

        slider = ctk.CTkSlider(self,
                               command= self.update_text,
                               button_color= GREEN,
                               button_hover_color= GRAY,
                               progress_color= GREEN,
                               fg_color= LIGHT_GRAY,
                               variable= user_height,
                               from_=130,
                               to= 230)
        slider.pack(side= "left", fill= "x", expand= True, pady= 10, padx= 10)

        self.output_string = ctk.StringVar()
        self.update_text(user_height.get())

        output_text = ctk.CTkLabel(self, 
                                   text= "1.77",
                                   text_color = BLACK,
                                   font = ctk.CTkFont(FONT, INPUT_FONT_SIZE),
                                   textvariable = self.output_string)
        output_text.pack(side= "left")

    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f"{meter}.{cm}")
        else:
            feet, inches = divmod(amount/ 2.54, 12)
            self.output_string.set(f"{int(feet)}\'{int(inches)}\"")
        
class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        super().__init__(master= parent, text= "metric",
                         text_color= DARK_GREEN,
                         font = ctk.CTkFont(family= FONT, size= SWITCH_FONT_SIZE, weight= "bold"))
        self.place(relx=0.98, rely=0.02, anchor= "ne")

        self.metric_bool = metric_bool
        self.bind("<Button>", self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text = "metric")
        else:
            self.configure(text = "imperial")






if __name__ == "__main__":
    App()