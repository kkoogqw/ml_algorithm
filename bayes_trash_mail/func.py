import sys
import numpy as np


np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)

# this class is using to record log and running data
# output : console -> *.txt
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

# this function is using to open a document in database and build an matrix
# data: *.txt -> matrix (numpy)
def importData(filename):
    a = np.loadtxt(filename)
    # print("type of a", type(a))
    return a

# this function is to build a sparse matrix by a n * 3 matrix (col 1&2 is position, col 3 is data)
# matrix (n * 3) -> sparse matrix
def buildSparse(matrix, row, col):
    result = []
    for i in range(col):
        list = []
        for j in range(row):
            list.append(0)
        result.append(list)
    for i in range(len(matrix)):
        result[(int)(matrix[i][0]) - 1][(int)(matrix[i][1]) - 1] = (int)(matrix[i][2])
    return result


# find(list:des, string:state) --> find the 0/1 in list:destination, record the index in list:result[]
def find(destination, state):
    result = []
    if state == "true":
        for i in range(len(destination)):
            if destination[i] != 0:
                result.append(i)
            else:
                continue
    if state == "false":
        for i in range(len(destination)):
            if destination[i] == 0:
                result.append(i)
            else:
                continue
    return result

# this function is to fill a list which length is “size” with 0
def zeros(size):
    result = []
    for i in range(size):
        result.append(0)
    return result

# this function is to compare 2 lists every elements and return a list with result
# input: list1, list2
# output: result -->> if : list1[i] > list[2] --> result[i] = 1
def bigger(list1, list2, result):
    for i in range(len(list1)):
        if list1[i] > list2[i]:
            result[i] = 1
        else:
            continue
    return

# this function is to get log_e() in a list
# list[i] = x --> result[i] = log_e(x)
def logList(list):
    result = []
    for i in range(len(list)):
        result.append(np.log(list[i]))
    return result

# this function is to xor every elements between 2 lists
# result[i] --> list1[i] xor list2[i]
def xorList(list1, list2):
    result = []
    if len(list1) != len(list2):
        print("The length of 2 lists is not equal!")
        return zeros(len(list1))
    else:
        for i in range(len(list1)):
            if list1[i] == list2[i]:
                result.append(0)
            elif list1[i] != list2[i]:
                result.append(1)
    return result

# this function is to get sum in a list with index in list "index"
def getSumOfElements(dest, index):
    result = 0
    for i in range(len(index)):
        result += dest[index[i]]
    return result

# this function returns a list with sun of every rows of a matrix
def getSumOfRow(matrix, rowList):
    result = []
    for i in range(len(matrix[0])):
        sum = 0
        for j in range(len(rowList)):
            sum += (matrix[rowList[j]][i])
        result.append(sum)
    return result

# this function returns a sum of every elements in a list
def sumList(list):
    result = 0;
    for i in range(len(list)):
        result += list[i]
    return (int)(result)
