import tkinter
from tkinter import StringVar, IntVar, DoubleVar, Text, Scrollbar
from tkinter import Entry, Button, Label
from art1 import performART1, init, string_to_clasters, clusters_to_string,customers 
from art1 import PROTOTYPES, DATABASE
from art1 import Customer, Prototype

class GraphicInterface(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.geometry("1200x500")
        self.title("ART1")
        self.beta = DoubleVar()
        self.vigilance = DoubleVar()
        self.max_items = IntVar()
        self.max_customers = IntVar()
        self.total_prototype_vectors = IntVar()
        self.entries()
        self.entries_set()
        self.labels()
        self.buttons()
    

    def buttons(self):
        self.button = Button(self, text="perform ART1", command=self.perform_art1)
        self.button.place(y=400, x=25)

    def labels(self):
        self.beta_label = Label(self, text="Beta: ").place(x=25, y=75)
        self.vigilance_label = Label(self, text="Vigilance: ").place(x=25, y=125)
        self.max_customers_label = Label(self, text="Max custormers: ").place(x=25, y=175)
        self.max_items_label = Label(self, text="Max items: ").place(x=25, y=225)
        self.total_prototype_vectors_label = Label(self, text="Total prototype vectors: ")
        self.total_prototype_vectors_label.place(x=25, y=275)

    def entries(self):
        self.beta_entry = Entry(self, textvariable=self.beta)
        self.beta_entry.place(x=25, y=100, width=25)
        
        self.vigilance_entry = Entry(self, textvariable=self.vigilance)
        self.vigilance_entry.place(x=25, y=150, width=25)

        self.max_items_entry = Entry(self, textvariable=self.max_items)
        self.max_items_entry.place(x=25, y=250, width=25)

        self.max_customers_entry = Entry(self, textvariable=self.max_customers)
        self.max_customers_entry.place(x=25, y=200, width=25)

        self.total_prototype_vectors_entry = Entry(self, textvariable=self.total_prototype_vectors)
        self.total_prototype_vectors_entry.place(x=25, y=300, width=25)
        self.clusters_entry = Text(self, font=('Consolas', 10), tabs=('3c'))
        self.clusters_entry.place(x=200, y=100, width=350, height=200)
        self.clusters_entry.insert(tkinter.END, clusters_to_string(customers=customers))
        self.scrollbar_clusters = Scrollbar(self, command=self.clusters_entry.yview)
        self.clusters_entry['yscroll'] = self.scrollbar_clusters.set
        self.scrollbar_clusters.pack(side=tkinter.RIGHT, fill=tkinter.Y, in_=self.clusters_entry)

        self.result = Text(self, font=('Consolas', 10), tabs=('3c'))
        self.result.place(x=550, y=100, width=500, height=200)
        self.scrollbar_result = Scrollbar(self, command=self.result.yview)
        self.result['yscroll']=self.scrollbar_result.set
        self.scrollbar_result.pack(side=tkinter.RIGHT, fill=tkinter.Y, in_=self.result)
        
        
    
    def entries_set(self):
        self.beta.set(1.0)
        self.vigilance.set(0.9)
        self.max_items.set(11)
        self.max_customers.set(10)
        self.total_prototype_vectors.set(5)

    def perform_art1(self):
        string = self.clusters_entry.get("1.0", "end")
        customers = string_to_clasters(string)
        init(customers=customers)
        performART1()
        grouping=""
        for prototype in PROTOTYPES:
            grouping += str(prototype) + '\n\n'

            for customer in prototype.customers:
                grouping += str(customer) + '\n'
                #  print(customer.init)
            grouping += '\n\n'
        self.result.insert(tkinter.END, grouping)
        for customer in DATABASE:
            DATABASE.remove(customer)
        for prototype in PROTOTYPES:
            PROTOTYPES.remove(prototype)
        print(DATABASE)
        print(PROTOTYPES)
        """
        Prototype.deleteinstances()
        Customer.deleteinstances()
        """


        


gui = GraphicInterface()
gui.mainloop()
