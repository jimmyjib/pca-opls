#!/usr/bin/env python3

from tkinter import *
import tkinter as tk
import tkinter.messagebox
from Statistics import Data
from filter import filter
from InputConvert import ColConvert, ColorConvert, GroupConvert

data = Data()
data_rec_flag = 0
data_sel_flag = 0

def Filter_Mode_Chosen():
    for widget in Filter_Widget.values():
        widget.show()

    for widget in PCA_Widget.values():
        widget.hide()

    for widget in BoxPlot_Widget.values():
        widget.hide()

    ButtonFrame1.pack(pady=5)
    ButtonFrame2.pack_forget()
    ButtonFrame3.pack_forget()
    ButtonFrame4.pack_forget()
    ButtonFrame5.pack_forget()

    screen.geometry("350x330")

def PCA_Mode_Chosen():
    for widget in Filter_Widget.values():
        widget.hide()

    for widget in PCA_Widget.values():
        widget.show()

    for widget in BoxPlot_Widget.values():
        widget.hide()

    ButtonFrame2.pack_forget()
    ButtonFrame2.pack(pady=5)
    ButtonFrame3.pack(pady=5)
    ButtonFrame4.pack_forget()
    ButtonFrame5.pack_forget()

    screen.geometry("350x455")

def BoxPlot_Mode_Chosen():
    for widget in Filter_Widget.values():
        widget.hide()

    for widget in PCA_Widget.values():
        widget.hide()

    for widget in BoxPlot_Widget.values():
        widget.show()

    ButtonFrame2.pack_forget()
    ButtonFrame2.pack_forget()
    ButtonFrame3.pack_forget()
    ButtonFrame4.pack(pady=5)
    ButtonFrame5.pack(pady=5)

    screen.geometry("350x400")

def Read_Data(name, start, end):
    global data_rec_flag
    #tkinter.messagebox.showinfo(name+start+end," Succesfully Read Data")
    data.read_data(name, int(start), int(end))
    data_rec_flag = 1

def Select_Data(groups):
    global data_sel_flag
    data.select_data(groups)
    data_sel_flag = 1

def PCA(color):
    global data_rec_flag
    if data_rec_flag==1:
        if color==['']:
            color = ["red","blue","green","magenta"]
        data.PCA(color)

def PLS(color):
    global data_sel_flag
    if data_sel_flag==1:
        if color==['']:
            color = ["red","blue"]
        data.PLS(color)

def OPLS(color):
    global data_sel_flag
    if data_sel_flag == 1:
        if color==['']:
            color = ["red","blue"]
        data.OPLS(color)

def BoxPlot_One(metabolite):
    data.BoxPlot_One(metabolite)

def BoxPlot_All():
    data.BoxPlot_All()

class Input:
    def __init__(self, name, frame):
        self.frame = Frame(frame)
        self.label = tk.Label(self.frame, text=name, bg="black", fg="white", width = 10, bd=3, padx=8, relief=SUNKEN)
        self.entry = tk.Entry(self.frame, bd=3, width = 25)
        #self.show()

    def show(self):
        self.frame.pack(pady=1)
        self.label.pack(side=LEFT)
        self.entry.pack(side=RIGHT)

    def hide(self):
        self.frame.pack_forget()
        self.label.pack_forget()
        self.entry.pack_forget()

class Label:
    def __init__(self, text, side = None):
        self.frame = Frame(screen)
        self.label = tk.Label(self.frame, text = text)
        self.side = side
        #self.show()

    def show(self):
        self.frame.pack()
        self.label.pack()

    def hide(self):
        self.frame.pack_forget()
        self.label.pack_forget()

class Button:
    def __init__(self, text, color, command, frame):
        self.frame = frame
        self.button = tk.Button(self.frame, text = text, fg = color, command=command, padx=7)
        #self.show()

    def show(self):
        self.frame.pack()
        self.button.pack(side = LEFT, padx=3)

    def hide(self):
        self.frame.pack_forget()
        self.button.pack_forget()

class labelFrame:
    def __init__(self, text):
        self.frame = LabelFrame(screen, text = text, bd=5)

    def show(self):
        self.frame.pack(fill="both", expand="yes")

    def hide(self):
        self.frame.pack_forget()

Filter_Widget = {}
PCA_Widget = {}
BoxPlot_Widget = {}

def Init():
    global ButtonFrame1, ButtonFrame2, ButtonFrame3, ButtonFrame4, ButtonFrame5
    Filter_Widget['Label']= labelFrame("File Input")
    PCA_Widget['File_Input_Label'] = labelFrame("File Input")
    BoxPlot_Widget['File_Input_Label'] = labelFrame("File Input")

    Filter_Widget['File_Name'] = Input("File Name", frame = Filter_Widget['Label'].frame)
    PCA_Widget['File_Name'] = Input("File Name", frame = PCA_Widget['File_Input_Label'].frame)
    BoxPlot_Widget['File_Name'] = Input("File Name", frame = BoxPlot_Widget['File_Input_Label'].frame)

    Filter_Widget['Sheet_Name'] = Input("Sheet Name", frame = Filter_Widget['Label'].frame)
    Filter_Widget['Metadata'] = Input("Metadata", frame = Filter_Widget['Label'].frame)
    Filter_Widget['Control_Name'] = Input("Control Name", frame = Filter_Widget['Label'].frame)

    ButtonFrame1 = Frame(Filter_Widget['Label'].frame, height= 100)

    Filter_Widget['Filter_Button'] = Button(
        "Filter","blue", lambda: filter(
            Filter_Widget['File_Name'].entry.get(),
            Filter_Widget['Sheet_Name'].entry.get(),
            Filter_Widget['Metadata'].entry.get(),
            Filter_Widget['Control_Name'].entry.get()
        ),
        frame=ButtonFrame1
    )

    PCA_Widget['Start_Column'] = Input("Start Column", frame = PCA_Widget['File_Input_Label'].frame)
    PCA_Widget['End_Column'] = Input("End Column", frame = PCA_Widget['File_Input_Label'].frame)
    PCA_Widget['Color'] = Input("Color", frame=PCA_Widget['File_Input_Label'].frame)

    BoxPlot_Widget['Start_Column'] = Input("Start Column", frame=BoxPlot_Widget['File_Input_Label'].frame)
    BoxPlot_Widget['End_Column'] = Input("End Column", frame=BoxPlot_Widget['File_Input_Label'].frame)

    ButtonFrame2 = Frame(PCA_Widget['File_Input_Label'].frame)

    PCA_Widget['Read_Data_Button'] = Button(
        "Read Data", "blue", lambda: Read_Data(
            PCA_Widget['File_Name'].entry.get(),
            ColConvert(PCA_Widget['Start_Column'].entry.get()),
            ColConvert(PCA_Widget['End_Column'].entry.get())
        ),
        frame = ButtonFrame2
    )

    ButtonFrame4 = Frame(BoxPlot_Widget['File_Input_Label'].frame)

    BoxPlot_Widget['Read_Data_Button'] = Button(
        "Read Data", "blue", lambda: Read_Data(
            BoxPlot_Widget['File_Name'].entry.get(),
            ColConvert(BoxPlot_Widget['Start_Column'].entry.get()),
            ColConvert(BoxPlot_Widget['End_Column'].entry.get())
        ),
        frame=ButtonFrame4
    )

    PCA_Widget['PCA_Button'] = Button("PCA", "red", lambda: PCA(ColorConvert(PCA_Widget['Color'].entry.get())), frame=ButtonFrame2)

    PCA_Widget['PLS_Label'] = labelFrame("PLS/OPLS-DA")
    PCA_Widget['Groups'] = Input("Groups", frame = PCA_Widget['PLS_Label'].frame)
    PCA_Widget['PLS_Color'] = Input("Color", frame=PCA_Widget['PLS_Label'].frame)

    ButtonFrame3 = Frame(PCA_Widget['PLS_Label'].frame)

    PCA_Widget['Select_Groups_Button'] = Button(
        "Select Groups", "blue", lambda: Select_Data(
            PCA_Widget['Groups'].entry.get(),
        ),
        frame = ButtonFrame3
    )
    PCA_Widget['PLS_Button'] = Button("PLS", "red", lambda: PLS(ColorConvert(PCA_Widget['PLS_Color'].entry.get())), frame = ButtonFrame3)
    PCA_Widget['OPLS_Button'] = Button("OPLS", "red", lambda: OPLS(ColorConvert(PCA_Widget['PLS_Color'].entry.get())), frame = ButtonFrame3)

    BoxPlot_Widget['Plot_Label'] = labelFrame("Plot")
    BoxPlot_Widget['Metabolite'] = Input("Metabolite", frame = BoxPlot_Widget['Plot_Label'].frame)

    ButtonFrame5 = Frame(BoxPlot_Widget['Plot_Label'].frame)

    BoxPlot_Widget['Plot_One'] = Button("Plot One", "red", lambda: BoxPlot_One(BoxPlot_Widget['Metabolite'].entry.get()), frame = ButtonFrame5)
    BoxPlot_Widget['Plot_All'] = Button("Plot All", "red", BoxPlot_All, frame = ButtonFrame5)

#start
global screen
screen = tk.Tk()
screen.geometry("350x130")
screen.title("test")
screen.iconbitmap('icon.ico')

Init()

var = IntVar()
Menu_Frame = LabelFrame(screen, text = "Menu", bd=5)
Menu_Frame.pack(fill="both", expand="yes")
Mode_Button_Frame = Frame(Menu_Frame)
Mode_Button_Frame.pack()
Filter_Mode_Button = Radiobutton(
    Mode_Button_Frame, text = "Filter", variable = var, value = 1, command = Filter_Mode_Chosen
)
Filter_Mode_Button.pack(side=LEFT)
PCA_Mode_Button = Radiobutton(
    Mode_Button_Frame, text = "PCA", variable = var, value = 2, command = PCA_Mode_Chosen
)
PCA_Mode_Button.pack(side=LEFT)
BoxPlot_Mode_Button = Radiobutton(
    Mode_Button_Frame, text = "Box Plot", variable = var, value = 3, command = BoxPlot_Mode_Chosen
)
BoxPlot_Mode_Button.pack(side=LEFT)

Dev_Frame = LabelFrame(screen, text = "Developer", bd=5)
Dev_Frame.pack(side = BOTTOM, fill="both", expand="yes")
Dev = tk.Label(Dev_Frame, text="Jihwan Kim")
Dev.pack(side = RIGHT)

screen.mainloop()
#end


