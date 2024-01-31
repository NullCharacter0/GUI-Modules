from GUI_modules import * 
import tkinter as tk 
import sys

root = tk.Tk()

def productlist_test():
    FinancialModules.ProductList(root,products=Products().list_products()).pack()



def pieFrameTest():
    FinancialModules.PiePerformanceFrame(root).pack()


root.mainloop()