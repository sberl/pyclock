import Tkinter

root = Tkinter.Tk()

w = Tkinter.Label(root, text="Hello world!")

logo = Tkinter.PhotoImage(file="/usr/local/share/doc/ntp/html/pic/rabbit.gif")
explanation ="""This is a gif of some sort. 
Not sure what it looks like yet"""

#w1 =Tkinter.Label(root, image=logo).pack(side="right")

w2 = Tkinter.Label(root, justify=Tkinter.LEFT, padx=10,text=explanation,
                   fg = "red", bg = "black").pack(side="left")


root.mainloop()

