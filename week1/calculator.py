#!/usr/bin/env python3

import sys

threshold = 3500
fee = 0

try:
    if len(sys.argv) != 2:
        raise
    else:
        wages = int(sys.argv[1])
except:
    print("Parameter Error")
    exit(1)

if wages <= threshold:
    tax = 0
    print(format(tax,".2f"))
else:
    income = wages - fee - threshold
    if income <= 1500:
        tax = income * 0.03 - 0
        print(format(tax,".2f"))
    elif 1500 < income <= 4500: 
        tax = income * 0.1 - 105
        print(format(tax,".2f"))
    elif 4500 < income <= 9000: 
        tax = income * 0.2 - 555
        print(format(tax,".2f"))
    elif 9000 < income <= 35000: 
        tax = income * 0.25 - 1005
        print(format(tax,".2f"))
    elif 35000 < income <= 55000: 
        tax = income * 0.3 - 2755
        print(format(tax,".2f"))
    elif 55000 < income <= 80000: 
        tax = income * 0.35 - 5505
        print(format(tax,".2f"))
    elif 80000 < income: 
        tax = income * 0.45 - 13505
        print(format(tax,".2f"))
