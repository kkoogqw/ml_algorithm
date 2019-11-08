import copy as cp

distanceToB = {
        'A' : 366,
        'B' : 0,
        'C' : 160,
        'D' : 242,
        'E' : 161,
        'F' : 178,
        'G' : 77,
        'H' : 151,
        'I' : 226,
        'L' : 244,
        'M' : 241,
        'N' : 234,
        'O' : 380,
        'P' : 98,
        'R' : 193,
        'S' : 253,
        'T' : 329,
        'U' : 80,
        'V' : 199,
        'Z' : 374
    }

class city:
    name = ''
    linkedCity = []

    def __init__(self, name, linked):
        self.name = name
        self.linkedCity = cp.deepcopy(linked)

    def getF_x(self, length):
        f_x = []
        for i in range(len(self.linkedCity)):
            f_x.append(self.linkedCity[i][1] + length + distanceToB[self.linkedCity[i][0]])
        return f_x

    def getLinkedName(self, index):
        return self.linkedCity[index][0]

    def getLinkedNDis(self, index):
        return self.linkedCity[index][1]

def nameFind(n, m):
    for i in range(len(m)):
        if m[i].name == n:
            return m[i]
def findIndex(value, list):
    for i in range(len(list)):
        if list[i] == value:
            return i

def checkPath(city, list, f_x):
    for i in range(len(list)):
        for j in range(len(city)):
            if  city[j][0] == list[i]:
                f_x[j] == 99999
    return

def buildMap():
    A = city('A', [['Z', 75], ['T', 118], ['S', 140]])
    B = city('B', [['U', 85], ['G', 90], ['P', 101], ['F', 211]])
    C = city("C", [['D', 120], ['P', 138], ['R', 146]])
    D = city("D", [['M', 70], ['C', 120]])
    E = city("E", [['H', 86]])
    F = city("F", [['S', 99], ['B', 211]])
    G = city("G", [['B', 90]])
    H = city("H", [['E', 86], ['U', 98]])
    I = city("I", [['N', 87], ['V', 92]])
    L = city("L", [['M', 70], ['T', 111]])
    M = city("M", [['L', 70], ['D', 75]])
    N = city("N", [['I', 87]])
    O = city("O", [['Z', 71], ['S', 151]])
    P = city("P", [['R', 97], ['B', 101], ['C', 138]])
    R = city("R", [['S', 80], ['P', 97], ['C', 146]])
    S = city("S", [['R', 80], ['F', 99], ['A', 140], ['O', 151]])
    T = city("T", [['L', 111], ['A', 118]])
    U = city("U", [['B', 85], ['H', 98], ['V', 142]])
    V = city("V", [['I', 92], ['U', 142]])
    Z = city("Z", [['O', 71], ['A', 75]])

    return [A, B, C, D, E, F, G, H, I, L, M, N, O, P, R, S, T, U, V, Z]

def findPath():
    map = buildMap()
    length = 0
    path = []
    lengthCount = []
    start = city('', [])
    dest = city('', [])

    s = input("start city:")
    d = input("destination city:")

    for i in range(len(map)):
        if map[i].name == s:
            start = map[i]
        if map[i].name == d:
            dest = map[i]

    next = start
    path.append(start.name)
    lengthCount.append(length)
    while(next != dest):
        f_x = next.getF_x(length)
        checkPath(next.linkedCity, path, f_x)
        minF = findIndex(min(f_x), f_x)
        next_city_Name = next.getLinkedName(minF)
        temp = next.getLinkedNDis(minF)
        path.append(next_city_Name)
        length += temp
        lengthCount.append(length)
        next = nameFind(next_city_Name, map)

    print("The path is:")
    string = ''
    for i in range(len(path)):
        string += path[i]
        string += '//using:'
        string += str(lengthCount[i])
        if i != len(path) - 1:
            string += " -> "
    print(string)

def main():
    findPath()

if __name__ == '__main__':
    main()