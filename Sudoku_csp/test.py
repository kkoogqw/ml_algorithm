map1 = [
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 6, 0, 9, 0, 0, 7, 0, 4],
    [0, 8, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 9, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 1, 9, 0, 8, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 1],
    [5, 3, 0, 1, 0, 0, 9, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 8, 0]]

map2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 6, 4, 0, 0],
    [9, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 8, 0, 0],
    [7, 8, 0, 5, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 6, 3],
    [0, 0, 0, 0, 0, 0, 0, 7, 0],
    [0, 0, 2, 8, 0, 9, 0, 0, 0]]

map3 = [
    [0, 0, 0, 0, 0, 2, 0, 0, 8],
    [6, 0, 3, 0, 1, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 3, 0, 0, 5],
    [8, 6, 0, 9, 2, 0, 0, 5, 3],
    [4, 0, 0, 3, 0, 0, 0, 1, 0],
    [5, 0, 0, 0, 8, 0, 0, 4, 0],
    [0, 4, 0, 0, 0, 7, 2, 0, 0],
    [0, 2, 0, 0, 0, 9, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 5, 3, 0]]

def init_CurDom(map,index):#index表示0~81某一位置索引，将该索引位置的行，列，方块进行检查，把可走的数字的域放入CurDom[index]的容器中
    global CurDom
    able_num = []
    temp = []
    row = index//9
    col = index%9
    for i in range(10):
        able_num.append(1)#先初始为1，将行，列，方块中出现的数字的索引置为0，不为零的即为可走域
    for i in range(9):
        if(map[i][col]):
            able_num[map[i][col]] = 0
    for i in range(9):
        if(map[row][i]):
            able_num[map[row][i]] = 0
    row1 = row//3*3
    row2 = row1+3
    col1 = col//3*3
    col2 = col1+3
    for i in range(row1,row2):
        for j in range(col1,col2):
            if(map[i][j]):
                able_num[map[i][j]] = 0
    for i in range(9):
        if(able_num[i+1]):
            temp.append(i+1)
    CurDom.append(temp)

def init(map):#初始化操作，num表示空格数目
    global Assigned
    global num
    global CurDom
    for i in range(81):
        Assigned.append(0)
    for index in range(81):
        i = index//9
        j = index%9
        if(map[i][j]==0):
            num = num + 1
            init_CurDom(map,index)
        else:
            Assigned[index] = 1#已经有值的位置置为1
            CurDom.append([])

def PickAnUnassignedVariable():#//找出可走的index,即为访问过的具有最少域空间的index值
    global CurDom
    global Assigned
    min_value = 10
    min_index = 82
    for i in range(81):
        if(Assigned[i] == 0):
            if(len(CurDom[i])<min_value):
                min_value = len(CurDom[i])
                min_index = i
    return min_index

def temp_Assigned(index,d):#索引位置index中的d被选择后，行，列，方块中其他索引位置的域中有d值时将d删除掉
    global CurDom
    global Assigned
    row = index//9
    col = index%9
    temp = []
    for i in range(9):
        row_index = row*9+i
        if(Assigned[row_index]==0):
            if d in CurDom[row_index]:
                temp.append(row_index)
                CurDom[row_index].remove(d)
    for i in range(9):
        col_index = i*9 + col
        if(Assigned[col_index]==0):
            if d in CurDom[col_index]:
                temp.append(col_index)
                CurDom[col_index].remove(d)
    row1 = row//3*3
    row2 = row1+3
    col1 = col//3*3
    col2 = col1+3
    for i in range(row1,row2):
        for j in range(col1,col2):
            square_index = i*9+j
            if(Assigned[square_index]==0):
                if d in CurDom[square_index]:
                    temp.append(square_index)
                    CurDom[square_index].remove(d)
    return temp

def Restore_CurDom(store_list,d):#重新将被删除d的索引位置的域空间加回d
    global CurDom
    for i in store_list:
        CurDom[i].append(d)

def GAC_Enfore():#判断是否返回DWO
    global Assigned
    global CurDom
    for i in range(81):
        if(Assigned[i]==0):
            if(len(CurDom[i])==0):
                return False
    return True

def GAC(level):#level为空格数
    global CurDom
    global Assigned
    global answer
    global count
    if level is 0:#当空格数目减为0时，则说明全部都找了一遍
        return True
    min_index = PickAnUnassignedVariable()#每次找到未被选择的空格位置（最小域空间）
    row = min_index//9
    col = min_index%9
    for d in CurDom[min_index]:#从该位置的域空间中选择d
        answer.append([row,col,d])#先放入结果队列
        Assigned[min_index] = d
        temp_Assigned_list = temp_Assigned(min_index,d)#list，里面包含当前选择d约束时受影响的位置链表
        if(GAC_Enfore):
            if(GAC(level-1)):#空格数-1
                return True
        Restore_CurDom(temp_Assigned_list,d)#域空间重新放回d
        Assigned[min_index] = 0
        answer.remove([row,col,d])
    return False

def print_map(map):
    for i in range(9):
        temp = ""
        temp = temp + "[ "
        for j in range(9):
            temp = temp + str(map[i][j]) + " "
            if(j==2 or j==5):
                temp = temp + "]  [ "
        temp = temp + "]\n"
        if(i==2 or i==5):
            temp = temp + "\n"
        print(temp)

def print_answer():
    global answer
    step = 0
    for data in answer:
        step = step + 1
        print("step ",step,": (",data[0],",",data[1],") ---> ",data[2])

def solve(map):
    global num
    global answer
    global CurDom
    global Assigned
    global count
    count = 0
    num = 0
    answer = []
    Assigned = []
    CurDom = []
    print("原始数独矩阵:\n")
    print_map(map)
    init(map)
    GAC(num)
    print_answer()
    for data in answer:
        map[data[0]][data[1]] = data[2]
    print("GAC求解结果为:\n")
    print_map(map)
    print('='*31)

if __name__ == '__main__':
    print("求解第一个样例\n")
    solve(map1)
    print("求解第二个样例\n")
    solve(map2)
    print("求解第三个样例\n")
    solve(map3)
