import tkinter as tk                
from tkinter import font  as tkfont 


class Engine(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

       
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):        #Welcome

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Investements using Greedy Algorithm", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button1.place(relx=.8, rely=.9)


class PageOne(tk.Frame):      #ChooseAmount

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Your Amount", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(relx=.5, rely=.9)
        button1 = tk.Button(self, text="Next",
                           command=lambda: controller.show_frame("PageTwo"))
        button1.place(relx=.8, rely=.9)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("PageOne"))
        button.place(relx=.9, rely=.10)
        button2 = tk.Button(self, text="Next",
                           command=lambda: controller.show_frame("PageOne"))
        button2.place(relx=.8, rely=.9)


if __name__ == "__main__":
    app = Engine()
    app.mainloop()
