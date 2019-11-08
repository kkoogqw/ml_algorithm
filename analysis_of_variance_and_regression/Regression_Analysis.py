#
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

'''
The 7 variables of database is:
x:  age*/sex/bmi*/children*/smoker/region
y:  charges

'''

# y = b0 + b1x1 + b2x2 + b3x3
# get : b0, b1, b2, b3 --> the linear regression equation

def Linear_Regression_analysis():
    data = pd.read_csv("data.txt")
    # print(data)
    train_data = data.ix[0:1332]
    # print(train_data)
    test_data = data.ix[1333:1337]
    # print(test_data)


    # data discribe
    discribe = train_data.describe()
    print("-------------------- The data discription --------------------")
    print(discribe)

    # display the 3 variable in point
    sns.pairplot(train_data, x_vars=['age', 'bmi', 'children'], y_vars='charges', size=8, aspect=1)
    plt.show()
    # display the 3 variable in point and linear
    sns.pairplot(train_data, x_vars=['age', 'bmi', 'children'], y_vars='charges', size=8, aspect=1, kind='reg')
    plt.show()

    corrCoefficient = train_data.corr()
    print("-------------------- Correlation coefficient --------------------")
    print(corrCoefficient)

    x_train = train_data[['age', 'bmi', 'children']]
    x_test = test_data[['age', 'bmi', 'children']]

    y_train = train_data[['charges']]
    y_test = test_data[['charges']]
    # print(x_test)
    # print(x_train)
    # print(y_test)
    # print(y_train)

    model = LinearRegression()
    model.fit(x_train, y_train)
    a = model.intercept_
    b = model.coef_

    # order: age bmi children
    print("\nthe linear regression equation :")
    print(a, b[0])

    k = float(a)
    x1 = float(b[0][0])
    x2 = float(b[0][1])
    x3 = float(b[0][2])

    print("y = ", k, "+", x1, "x1", "+", x2, "x2", "+", x3, "x3")

    Y_pred = model.predict(x_test)  # 对测试集数据，用predict函数预测

    plt.rcParams['figure.figsize'] = (10.0, 6.0)
    plt.plot(range(len(Y_pred)), Y_pred, 'red', linewidth=2.5, label="predict data")
    plt.plot(range(len(y_test)), y_test, 'green', label="test data")
    plt.legend(loc=2)
    plt.show()

    print("\n-------------------- the test result --------------------")
    test_data = [x_test['age'].tolist(), x_test['bmi'].tolist(), x_test['children'].tolist()]
    test_count = len(test_data[0])
    test_result = []
    for i in range(test_count):
        test_result.append(k + (x1 * test_data[0][i]) + (x2 * test_data[1][i]) + (x3 * test_data[2][i]))

    print(test_result)
    real_result = y_test['charges'].tolist()
    print("\n-------------------- The real data --------------------")
    print(real_result)

    SE = np.std(real_result) / np.sqrt(len(real_result))
    con_intervals = stats.norm.interval(0.95, loc=np.mean(real_result), scale=SE)
    print(con_intervals)

    print("\n-------------------- Confidence intervals -------------------- ")
    _SE = np.std(test_result) / np.sqrt(len(test_result))
    _con_intervals = stats.norm.interval(0.95, loc=np.mean(test_result), scale=SE)

    print(_con_intervals)
    return

def main():
    Linear_Regression_analysis()
    return

if __name__ == '__main__':
    main()
