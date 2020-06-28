
class Choice:
    def __init__(self, name, child=""):
        self.name = name
        self.child = child

class Enter:
    def __init__(self, name, des, choiceNum, choiceList):
        self.name = name
        self.des = des
        self.choiceNum = choiceNum
        self.choiceList = choiceList

def makeEnter(tempS, globList):
    tempS = tempS.strip("\n")
    data = tempS.split(",")
    data[2] = int(data[2])
    tempL = []
    if data[2] != 0:
        for i in range(data[2]):
            choice = Choice(data[3 + 2*i], data[4 + 2*i])
            tempL.append(choice)
    
    globList.append(Enter(data[0], data[1], data[2], tempL))

def getData():
    localList = []
    f = open("plan", "r")

    for line in f:
        makeEnter(line, localList)

    f.close()

    return localList

def getChoice(event, eventList, eventNameList):
    print("\n+++++++++++++++++++++++++++++++++")
    print(event.des)
    if event.choiceNum != 0:
        for i in range(event.choiceNum):
            print("     %d. %s" %(i + 1, event.choiceList[i].name))
        
        choice = int(input("What do you do (number): "))

        # the problem lies in this specific code
        thing = event.choiceList[choice - 1]
        nextEvent = thing.child

        for name, evt in zip(eventNameList, eventList):
            # print(name)
            if name == nextEvent:
                print(name)
                getChoice(evt, eventList, eventNameList) 
    return

def main():
    events = getData()
    eventNames = []
    for thing in events:
        eventNames.append(thing.name)

    getChoice(events[0], events, eventNames)

main()