


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy import stats



'''
The 7 variables of database is:
x:  age*/sex/bmi*/children*/smoker/region
y:  charges

'''

def ANOVA_1():
    print("----------------------- Charges <-> sex -----------------------")
    data = pd.read_csv("data.txt")
    # print(data)

    analysis_data = data[['sex','charges']]
    # print(analysis_data)

    # female -> 0 / male -> 1
    # analysis_data['sex'] = analysis_data['sex'].replace(['male', 'female'],[1, 0])
    # print(analysis_data)

    # group = analysis_data['sex'].unique()
    # print(group)

    male_group = analysis_data[analysis_data['sex'] == 1]['charges']
    female_group = analysis_data[analysis_data['sex'] == 0]['charges']
    # print(male_group)
    # print(female_group)

    model = ols('charges ~ sex', analysis_data).fit()
    anovat = anova_lm(model)
    print(anovat)

    # model = ols('charges ~ children', data).fit()
    # anovat = anova_lm(model)
    # print(anovat)

    # args = [[male_group, female_group]]
    # print(args)
    # # levene test
    # w, p = stats.levene(*args)
    # print(w, p)

    # a, b = stats.f_oneway(*args)
    # print(a, b)

    return

def ANOVA_2():
    print("----------------------- Charges <-> sex & smoker -----------------------")
    data = pd.read_csv("data.txt")
    # print(data)

    analysis_data = data[['sex', 'smoker', 'charges']]
    # print(analysis_data)

    # female -> 0 / male -> 1
    # analysis_data['sex'] = analysis_data['sex'].replace(['male', 'female'],[1, 0])
    # print(analysis_data)

    # group = analysis_data['sex'].unique()
    # print(group)

    male_group = analysis_data[analysis_data['sex'] == 1]['charges']
    female_group = analysis_data[analysis_data['sex'] == 0]['charges']
    # print(male_group)
    # print(female_group)

    model = ols('\ncharges ~ sex + smoker', analysis_data).fit()
    anovat = anova_lm(model)
    print(anovat)
    return

def main():
    ANOVA_1()
    ANOVA_2()
    return

if __name__ == '__main__':
    main()