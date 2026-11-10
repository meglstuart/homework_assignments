import tkinter as tk

root = tk.Tk()
root.title("Demo")

btn = tk.Button(root, text = "Button") # creates button and adds to root
btn.grid() # adds button to window

btn1 = tk.Button(root, text = "Other Button") # creates button and adds to root
btn1.grid(row = 1, column = 1) # adds button to window

def on_click():
 	print("testing")

btn1.config(command=on_click)

root.mainloop()