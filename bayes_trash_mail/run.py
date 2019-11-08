
import Train
import Test
import func

def main():


    trainDataPack_0 = ["Data/train/train-features.txt", "Data/train/train-labels.txt"]
    trainDataPack_1 = ["Data/train/train-features-50.txt", "Data/train/train-labels-50.txt"]
    trainDataPack_2 = ["Data/train/train-features-100.txt", "Data/train/train-labels-100.txt"]
    trainDataPack_3 = ["Data/train/train-features-400.txt", "Data/train/train-labels-400.txt"]

    dataBase = [trainDataPack_0, trainDataPack_1, trainDataPack_2, trainDataPack_3]

    report = ""
    for i in range(len(dataBase)):
        trainResult = Train.train(dataBase[i])
        testResult = Test.test(trainResult[0], trainResult[1])
        string = "Train database:\t" + dataBase[i][0] + "\t" + dataBase[i][1]
        string += "\nTrain result:\n\t" + "prob_spam:\t" + str(trainResult[1])
        string +=  "\nTest result:\n\t" + testResult[0] + "\n\t" + testResult[1] + "\n"
        string += "Train time using:\t" + trainResult[2] + "\nTest time using:\t" + testResult[2] + "\n"
        string += "------------------------------------------------------------\n"
        report += string

    func.sys.stdout = func.Logger("Report.log")
    print("--------------------------------> Running Report <--------------------------------")
    print(report)
    return

if __name__ == '__main__':
    main()