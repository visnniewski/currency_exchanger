import requests

from tkinter import *

class Exchanger_app(Tk):
    def __init__(self):
        super().__init__()

        #set title and geometry of window
        self.title(" Python exchanger ")
        self.geometry("300x270")
        # self.configure(bg='#27ae60')

        #init rates from api
        self.rates = {}
        self.load_rates()

        #create option vars
        self.option_var1 = StringVar(self, next(iter(self.rates)))
        self.option_var2 = StringVar(self, next(iter(self.rates)))

        Label(self, text="Money Exchanger", font=("Helvetica", 16)).pack()

        self.create_option_menu()

    def load_rates(self):
        #get rates json
        r = requests.get("http://api.nbp.pl/api/exchangerates/tables/A").json()[0]["rates"]
        
        #append all rates into rates dict
        for rate in r:
            self.rates[rate["currency"] + " " + rate["code"]] = rate["mid"]

        #append polish zloty into dict
        self.rates["polski złoty PLN"] = 1.00
    
    def create_option_menu(self):
        #create first option menu
        Label(self, text="Select currency", font=("Helvetica", 11)).pack()
        Label(self).pack()

        OptionMenu(self, self.option_var1, *self.rates).pack()
        self.entry = Entry(self)
        
        #setting 1 as default val for entry
        self.entry.insert(0, 1)
        self.entry.pack()

        #make space between option menus
        Label(self).pack()

        #create second option menu
        OptionMenu(self, self.option_var2, *self.rates).pack()

        #create button
        Button(self, text="Exchange", command=self.exchange).pack()

        self.result = Label(self)

    def exchange(self, *args):
        if self.option_var1.get() == "polski złoty PLN":
            #convert from pln to entered currency
            self.result["text"] = f"\n{self.entry.get()} {self.option_var1.get()} = {round((self.rates[self.option_var1.get()] * int(self.entry.get())) / self.rates[self.option_var2.get()], 3)} {self.option_var2.get()}"
        elif self.option_var2.get() == "polski złoty PLN":
            #convert from entered currency to pln
            self.result["text"] = f"\n{self.entry.get()} {self.option_var1.get()} = {self.rates[self.option_var1.get()] * int(self.entry.get())} {self.option_var2.get()}"
        else:
            #convert from entered currency to pln then to second entered currency
            calc = round(self.rates["polski złoty PLN"] * int(self.entry.get()) * self.rates[self.option_var1.get()] / self.rates[self.option_var2.get()], 3)
            self.result["text"] = f"\n{self.entry.get()} {self.option_var1.get()} = {calc} {self.option_var2.get()}"
        self.result.pack()

if __name__ == "__main__":
    app = Exchanger_app()
    app.mainloop()