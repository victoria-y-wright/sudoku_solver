import tkinter as tk

def set_up(self):
    err_flags_text = ["Only digits 1-9 are valid inputs", 
                      "Enter starting digits in the grid", 
                      "Numbers can't repeat in the same row, column or box", 
                      "Paste a list of 81 digits 1-9 (blank space= 0)",
                      "Try adding another strategy to solve", 
                      "Add faces to create the shape of the 3D sudoku board",
                      "Invalid 3D Sudoku board- faces must be form lines of 3"]
    self.err_flags = [False for i in range(len(err_flags_text))]
    self.lbl_err_flags = []
    for i in range(len(err_flags_text)):
        self.lbl_err_flags.append(tk.Label(master=self.frm_top, text=err_flags_text[i], bg = 'pink', font=('TkDefaultFont', 12), width=60, justify = "center"))

def reset(self):
    for i in range(len(self.err_flags)):
        if self.err_flags[i] == True:
            self.lbl_err_flags[i].pack_forget()

def flag(self,index):
    self.lbl_err_flags[index].pack()
    self.err_flags[index] = True 