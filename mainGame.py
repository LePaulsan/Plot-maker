import tkinter as tk


# Classes ------------------
class Choice:
    def __init__(self, name, child=""):
        self.name = name
        self.child = ""

class Enter:
    def __init__(self, name, des, choiceNum, choiceList):
        self.name = name
        self.des = des
        self.choiceNum = choiceNum
        self.choiceList = choiceList

# Creat an entry point with a name: follow by an entry box that can be typed in
class EntryBox:
    def __init__(self, surface, text, row):
        self.name = tk.Label(surface, text=text)
        self.content = tk.Entry(surface)
        self.row = row 

    def display(self):
        self.name.grid(row=self.row, column=0, sticky=tk.W)
        self.content.grid(row=self.row, column=1, padx=10, pady=5, sticky=tk.W)

    def requestContent(self):
        temp = self.content.get()
        self.content.delete(0, tk.END)
        return temp

# I need a delete button next to it to delete it
class ChoiceBox(EntryBox):
    def __init__(self, surface, text, row, globList):
        super().__init__(surface, text, row)
        self.delete = tk.Button(surface, text="-", command=lambda: self.deleteButt(globList))

    def display(self):
        self.name.grid(row=self.row, column=0, sticky=tk.W)
        self.content.grid(row=self.row, column=1, padx=10, pady=5, sticky=tk.W) 
        self.delete.grid(row=self.row, column=2, sticky=tk.W)

    def deleteButt(self, tempList): 
        self.name.destroy()
        self.content.destroy()
        self.delete.destroy()
        for item in tempList[:]:
            if item == self:
                tempList.remove(item)

# drop box need the surface, the list, and would just pack it up there
class DropBox:
    def __init__(self, surface, tempL):
        self.nameList = []
        self.tempL = tempL
        self.surface = surface

        for item in self.tempL:
            self.nameList.append(item.name) 

        self.var = tk.StringVar()
        self.var.set(self.nameList[0])

        self.output = None

    def createDropBox(self, row):
        self.drop = tk.OptionMenu(self.surface, self.var, *self.nameList)
        self.drop.grid(row=row, column=0, padx=5, pady=5)

        self.button = tk.Button(self.surface, text="ok", command=self.getObject)
        self.button.grid(row=row, column=1, padx=5, pady=5)
    def makeDropBox(self, box):
        if box.output != None:
            choiceDropBox = DropBox(self.surface, box.output.choiceList)
            choiceDropBox.createDropBox(1)

    def getObject(self):
        for item, thing in zip(self.nameList, self.tempL):
            if self.var.get() == item:
                self.output = thing
                break

        self.makeDropBox(self)


# Variables----------------
eventList = []
# eventList = [Enter("Start", "Empty here", 1, [Choice("Eat")]), Enter("Ate", "Ful", 1, [Choice("Stop", "Start")])]
choiceBoxList = []


# Function ------------------
#  This is a function of the add choice frame
def addChoice(surface, tempList, row):
    tempList.append(ChoiceBox(surface, "Choice", len(tempList) + row, tempList))
    tempList[len(tempList)-1].display()

def changeName(obj, var, button):
    for choice in obj.choiceList:
        if choice.name == var:
            choice.child = obj.name
            print(choice.child)
    
    button.configure(state="normal")

def chooseChoice(surface, var, evnList, button):
    obj = ""

    for thing in evnList:
        if var == thing.name:
            obj = thing
    
    nameList = []
    for choice in obj.choiceList:
        nameList.append(choice.name)
        
    var = tk.StringVar()
    var.set(nameList[0])

    event = tk.OptionMenu(surface, var, *nameList, command=lambda var: changeName(obj, var, button))
    event.pack()

# this is a veryyyyyyy important functin
def chooseEvent(surface, evnList, button):
    _list = surface.winfo_children()

    for item in _list:
        item.destroy()

    nameList = []
    for obj in evnList:
        nameList.append(obj.name)
    
    var = tk.StringVar()
    var.set(nameList[0])

    event = tk.OptionMenu(surface, var, *nameList, command=lambda var: chooseChoice(surface, var, evnList, button))
    event.pack()

# Function for summiting data
def submit(surface, name, des, tempList, globList, button):
    tempChoiceList = []
    tempName = name.requestContent()
    tempDes = des.requestContent()
    tempChoiceNum = len(tempList)

    for item in tempList:
        tempChoiceList.append(Choice(item.requestContent()))

    globList.append(Enter(tempName, tempDes, tempChoiceNum, tempChoiceList))

    chooseEvent(surface, globList, button)

    button.configure(state="disabled")

def saving(aList):
    f = open("plan", "a")

    for thing in aList:
        data = "%s,%s,%d" %(thing.name, thing.des, thing.choiceNum)
        for choice in thing.choiceList:
            data.join(",%s,%s" %(choice.name, choice.child))
        
        f.write(data + "\n")

    f.close()

def main(root, choiceBoxList, eventList):
    # Identity frame
    firstFrame = tk.LabelFrame(root, text="Event", padx=5, pady=5)
    firstFrame.pack(anchor=tk.W, padx=10, pady=10)

    name = EntryBox(firstFrame, "Name:", 1)
    des = EntryBox(firstFrame, "Plot:", 2)
    name.display()
    des.display()

    # Choices input frame
    secondFrame = tk.LabelFrame(root, text="Choice", padx=5, pady=5)
    secondFrame.pack(anchor=tk.W, padx=10, pady=10)

    l3 = tk.Label(secondFrame, text="Choices")
    b3 = tk.Button(secondFrame, text="+", command=lambda: addChoice(secondFrame, choiceBoxList, 1)) 
    l3.grid(row=0, column=0, sticky=tk.W)
    b3.grid(row=0, column=1, sticky=tk.W)

   # Child of frame
    thirdFrame = tk.LabelFrame(root, text="Child of", padx=5, pady=5)
    thirdFrame.pack(anchor=tk.W, padx=10, pady=10)

    b = tk.Button(root, text="Submit", command=lambda: submit(thirdFrame, name, des, choiceBoxList, eventList, b))

    if len(eventList) > 0:
        chooseEvent(thirdFrame, eventList, b)

    # submition
    b.pack(padx=5, pady=5)

    save = tk.Button(root, text="Save", command=lambda: saving(eventList))
    save.pack()

# The main function
root = tk.Tk()
root.title("Event maker")
main(root, choiceBoxList, eventList)
tk.mainloop()