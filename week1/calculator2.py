#!/usr/bin/env python3

import sys

threshold = 3500

def getwages():
    try:
        if len(sys.argv) < 2:
            raise
        else:
            for arg in sys.argv[1:]:
                list1 = arg.split(':')
                nums.append(int(list1[0]))
                wage.append(int(list1[1]))
    except:
        print("Parameter Error")
        exit(1)

def calculation(wages):
    fee = wages * 0.165
    income = wages - fee - threshold
    if wages <= threshold:
        return count(wages,fee,income,0,0)
    elif income <= 1500:
        return count(wages,fee,income,0.03,0)
    elif 1500 < income <= 4500: 
        return count(wages,fee,income,0.1,105)
    elif 4500 < income <= 9000: 
        return count(wages,fee,income,0.2,555)
    elif 9000 < income <= 35000: 
        return count(wages,fee,income,0.25,1005)
    elif 35000 < income <= 55000: 
        return count(wages,fee,income,0.3,2755)
    elif 55000 < income <= 80000: 
        return count(wages,fee,income,0.35,5505)
    elif 80000 < income: 
        return count(wages,fee,income,0.45,13505)

def count(wages,fee,income,rate,quicknum):
    tax = income * rate - quicknum
    after_wages = wages - fee - tax
    return after_wages

if __name__ == '__main__':
    nums = []
    wage = []
    getwages()
    for i in range(len(nums)):
        b = format(calculation(wage[i]),".2f")  
        print(str(nums[i]) + ":" + str(b))
