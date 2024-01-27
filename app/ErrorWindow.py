from tkinter import Toplevel, Label

class ErrorWindow():
  def __init__(self, root, label):
    self.top = Toplevel(root)
    self.top.geometry('200x50')
    self.label = Label(self.top, text=label).pack()
    self.top.grab_set()
    self.top.focus_set()
    self.top.wait_window()