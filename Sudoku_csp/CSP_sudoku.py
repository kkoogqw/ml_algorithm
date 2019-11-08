
import sudoku as sdk
global time
time = 0

def CSP_sudoku(input):

    global time
    time += 1
    start_pos = [0, 0]
    if sdk.find_empty_position(input, start_pos) == False:
        return True

    row = start_pos[0]
    col = start_pos[1]
    for i in range(1, 10):
        if sdk.CSP_check_point(input, row, col, i) == True:
            input[row][col] = i
            if CSP_sudoku(input) == True:
                return True
            input[row][col] = 0
    return False

def get_solution(filename):
    global time
    path = "todo/" + filename
    todo = sdk.read_file(filename)
    start_time = sdk.time.clock()
    if CSP_sudoku(todo) == True:
        end_time = sdk.time.clock()
        print(todo)

        print("Time cost:", end_time - start_time)
        print("Loop count:", time)
        info = "Time cost: " + str(end_time - start_time) + "\nLoop count: " + str(time)
        sdk.output(filename, todo, "CSP", info)
    else:
        print("Cannot find solution!")
        sdk.output(filename, ["No solution!"], "CSP", "")

def main():
    filename = input("the file name:")
    get_solution(filename)
    return

if __name__ == '__main__':
    main()