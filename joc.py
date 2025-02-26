


def section_list(file_name):        # Creez dictionar pentru sectiuni
    f = open(file_name, "r")
    d = {}
    nr = 0
    for linie in f:
        linie = linie.strip()
        if len(linie) > 0:
            if linie[0] != "#":
                if linie in d:
                    print("Se repeta sectiunile")
                    return 0
                else:
                    if linie[0] == "[":
                        nr += 1
                        d[linie] = []
                        copy = linie
                    else:
                        if copy == "[Sigma]" or copy == "[alfabet]":
                            d[copy].append(linie)
                        else:
                            linie = linie.split(",")
                            linie = tuple(linie)
                            d[copy].append(linie)

    g.write("Numar sectiuni: ");g.write(str(nr) + "\n")
    f.close()
    return d


def exista_sigma(d):             # Verific daca exista limbaj (simboluri)
    if "[Sigma]" not in d.keys() or d["[Sigma]"] == []:
        g.write("Error: Nu exista Sigma" + '\n')
        return 0
    #else:
        #print("Exista Sigma: ", str(d["[Sigma]"]))


    return 1

def exista_deltaa(d):             # Verific daca exista delta (tranzitii)
    if "[Delta]" not in d.keys() or d["[Delta]"] == []:
        g.write("Error: Nu exista Delta" + '\n')
        return 0
    #else:
        #print("Exista Delta: ",(str(d["[Delta]"])))
    return 1


def start_final(d):              # Creez dictionar pentru starile initiale si finale
    d2={}
    d2['S']=[];d2['F']=[]
    for i in (d["[States]"]):
        if(len(i)==2):
            d2[i[1]].append(i[0])
        elif (len(i)==3):
            d2[i[1]].append(i[0])
            d2[i[2]].append(i[0])

    return d2


def start_final1(d):            # Verific daca sunt mai multe stari initiale
    d2=start_final(d)
    if (len((d2["S"]))) > 1:
        g.write("Error: Mai multe stari initiale" + '\n')
        return 0

    return 1


def exista_delta(d):            # Verific daca tranzitiile au elemente valide
    delta=d["[Delta]"]
    for element in range(len(delta)):
        #print(delta[element])
        ok1=0; ok2=0; ok3=0
        e=delta[element]
        states=d["[States]"]
        for i in range(len(states)):
            #print(states[i])
            if e[0] == states[i][0]:
                ok1=1
            if e[3] == states[i][0]:
                ok2=1

        if ok1 == 0:
            g.write("Error: Nu exista starea " + e[0] + '\n')
            return 0
        if ok2 == 0:
            g.write("Error: Nu exista starea " + e[2] + '\n')
            return 0

        sigma=d["[Sigma]"]
        for i in range(len(sigma)):
            if e[1] == sigma[i]:
                ok3=1

        if ok3 == 0:
            g.write("Error: Nu exista simbolul " + e[1] + '\n')
            return 0

        #print('\n')

    return 1


def duplicate(d):
    sigma=d["[Sigma]"]
    if len(set(sigma)) != len(sigma):        # Verific daca sunt simboluri duplicate in Sigma
        g.write("Error: Se repeta simbolurile " + '\n')
        return 0


    stari=[]                                 # Verific daca sunt stari duplicate in States
    states = d["[States]"]
    for i in states:
        stari.append(i[0])

    if len(set(stari)) != len(stari):
        g.write("Error: Se repeta starile " + '\n')
        return 0

    return 1


def isItemValid(item):      # Verific daca simbolul este in alfabetul listei
    if item in sectiuni["[alfabet]"] or item == '0':
        return True
    return False

def isItemInInventory(item):        # Verific daca itemul este in lista
    if item in inventory or item == '0':
        return True
    return False

def canMoveToRoom(new):             # Verific daca am itemul necesar sa ma mut in alta camera
    if roomReq[new] in inventory:
        return True
    return False

def emulate_dfa(d,dict_start,string):       # Functia principala care parcurge camerele
    q=dict_start["S"][0]
    i=0
    action_item = string.split(",")
    while i <= len(action_item):
        print ("Action: ", action_item[i])                  # Afisez actiunea pe care o execut
        if (action_item[i] == "look"):             # Afisez un text cu descrierea camerei in cazul in care actiunea este 'look' 
            print("You are now in", roomDisplayNames[q], "-", roomDesc[q])
            print("From here you can go to: ")
        checkedDeltas = 0                           # Folosit pentru a parcurge toate tranzitiile pentru a verifica toate camerele adiacente
        for delta in d["[Delta]"]:                  # Parcurgem toate tranzitiile  
            if " " in action_item[i]:                # Verificam daca actiunea este foramta din 2 parametrii (ex go, take, drop) sau din unul (ex look, inventory)
                action, item = action_item[i].split(" ")
                if action=="go" and delta[1]==action and delta[2]==roomReq[item] and not canMoveToRoom(delta[3]):       # Verificam daca avem itemul necesar schimbarii camerei
                    print("Nu ai item sa mergi in ", delta[3])
                    return 0        # in cazul in care nu o avem, ne oprim
                if action=="go":    
                    item = roomReq[item]        # Daca actiunea este go, stabilim de ce item avem nevoie pentru a merge in acea camera
                if delta[0]==q and delta[1]==action and delta[2]==item and isItemValid(item) and isItemValid(delta[5]):
                    q=delta[3]
                    if delta[4] in inventory and delta[4] != '0':   # eliminam itemul daca este nevoie (in cazul drop)
                        inventory.remove(delta[4])
                    if delta[5] not in inventory and delta[5] != '0':      # adaugam itemul daca este nevoie (in cazul take)
                        inventory.append(delta[5])
                    i=i+1
                    if i>=len(action_item):         # verificam daca am parcurs toate actiunile
                        if q not in dict_start["F"]:        # verificam starea in care ne aflam
                            g.write("Error: Automata nu accepta string-ul (nu ajunge intr-o stare finala)" + "\n")
                            return 0
                        else:
                            return 1
                    break
            else:
                if action_item[i]=="inventory":     # daca actiunea este inventar
                    print("Inventarul curent: ", inventory) # afisam inventarul
                    i = i + 1
                    if i>=len(action_item):         # verificam daca am parcurs toate actiunile
                        if q not in dict_start["F"]:        # verificam starea in care ne aflam
                            g.write("Error: Automata nu accepta string-ul (nu ajunge intr-o stare finala)" + "\n")
                            return 0
                        else:
                            return 1
                    break
                if action_item[i]=="look":
                    checkedDeltas = checkedDeltas + 1
                    if delta[0]==q:
                        if delta[1]=="go":
                            print("-", roomDisplayNames[delta[3]])
                    if checkedDeltas == len(d["[Delta]"]):
                        i = i + 1
                if i>=len(action_item):         # verificam daca am parcurs toate actiunile
                    if q not in dict_start["F"]:        # verificam starea in care ne aflam
                        g.write("Error: Automata nu accepta string-ul (nu ajunge intr-o stare finala)" + "\n")
                        return 0
                    else:
                        return 1

g = open("date.out", "w")
sectiuni=section_list("date.in")
print(sectiuni)
print()
print(start_final(sectiuni))

print()


inventory=[]


roomReq = { "entranceHall" : "invitation",          # Creez un dictionar cu itemele necesare pentru a intra in fiecare camera
"diningRoom" : "",
"kitchen" : "chefsHat",
"armory" : "key",
"treasury" : "sword",
"library" : "ancientCoin",
"pantry" : "spoon",
"throneRoom" : "crown",
"wizardsStudy" : "spellBook",
"secretExit" : "magicWand" }

roomDesc = {"entranceHall" : "The grand foyer of the Castle of Illusions.",         # Creez un dictionar cu descrieri pentru fiecare camera
"diningRoom": "A room with a large table filled with an everlasting feast.",
"kitchen": "A room packed with peculiar ingredients.",
"armory": "A chamber filled with antiquated weapons and armour.",
"treasury": "A glittering room overflowing with gold and gemstones.",
"library": "A vast repository of ancient and enchanted texts.",
"pantry": "A storage area for the Kitchen.",
"throneRoom": "The command center of the castle.",
"wizardsStudy": "A room teeming with mystical artifacts.",
"secretExit": "The hidden passage that leads out of the Castle of Illusions."}

roomDisplayNames = {"entranceHall" : "Entrance Hall",    # Creez un dictionar de nume lizibile
"diningRoom" : "Dining Room",
"kitchen" : "Kitchen",
"armory" : "Armory",
"treasury" : "Treasury",
"library" : "Library",
"pantry" : "Pantry",
"throneRoom" : "Throne Room",
"wizardsStudy" : "Wizard's Study",
"secretExit" : "Secret Exit"}


dict_start=start_final(sectiuni)  
emulator=emulate_dfa(sectiuni,dict_start,"take invitation,go entranceHall,take key,go armory,take sword,inventory,go treasury,take ancientCoin,go library,take spellBook,inventory,go treasury,go wizardsStudy,take magicWand,look,inventory,drop invitation,inventory,go secretExit,look")

if exista_sigma(sectiuni) == exista_deltaa(sectiuni) == start_final1(sectiuni) == exista_delta(sectiuni) == \
        duplicate(sectiuni) == emulator == 1:

    g.write('\n' + "LA-ul a fost acceptat !!" + '\n')
    print('\n', "LA-ul a fost acceptat !!")
else:
    g.write('\n' + "LA-ul nu a fost acceptat." + '\n')
    print('\n', "LA-ul nu a fost acceptat.")


g.close()