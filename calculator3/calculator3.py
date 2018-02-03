#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import csv
import os

# 处理命令行参数类
class Args(object):

    def __init__(self):
        self.args = sys.argv[1:]

    # 获得参数路径
    def getfile(self,index):
        self.index = index
        result = self.args.index(self.index)
        configfile = self.args[result+1]
        return configfile

    # 判断命令行参数
    def isfile(self):
        try:
            if len(sys.argv) == 7:
                fileexists1 = os.path.exists(self.getfile('-c'))
                fileexists2 = os.path.exists(self.getfile('-d'))
                if fileexists1 and fileexists2:
                    fileformat1 = os.path.basename(self.getfile('-c')).split('.')
                    fileformat2 = os.path.basename(self.getfile('-d')).split('.')
                    fileformat3 = os.path.basename(self.getfile('-o')).split('.')
                    if fileformat1[1] != 'cfg':
                        raise ValueError
                    elif fileformat2[1] != 'csv':
                        raise ValueError
                    elif fileformat3[1] != 'csv':
                        raise ValueError
                    else:
                        pass
                else:
                    raise IOError
            else:
                raise
        except IOError:
            print("File is not exists")
            exit(1)
        except ValueError:
            print("File error")
            exit(1)
        except:
            print("Parameter Error")
            exit(1)

# 配置文件类
class Config(object):

    def __init__(self):
        self.config = self._read_config()
    # 配置文件读取内部函数
    def _read_config(self):
        config = {}
        arg = Args()
        with open(arg.getfile('-c'),'r') as f:
            cfglist1 = f.readlines()
            for cfg in cfglist1:
                cfglist2 = cfg.split('=')
                config[cfglist2[0].strip()] = float(cfglist2[1].strip().strip('/n'))
        return config

# 用户数据类
class UserData(object):

    def __init__(self):
        self.userdata = self._read_userdata()
    # 用户数据读取内部函数
    def _read_userdata(self):
        userdata = {}
        arg = Args()
        with open(arg.getfile('-d'),'r') as f:
            datalist1 = f.readlines()
            for data in datalist1:
                datalist2 = data.split(',')
                userdata[int(datalist2[0].strip())] = float(datalist2[1].strip().strip('/n'))
        return userdata

# 税后工资计算类
class IncomeTaxCalculator(object):
    
    result = [0,0,0,0,0]
    gongzi = []
    gonghao = []
    fees = []
    taxs = []
    after_wages = []
    threshold = 3500
    ud = UserData().userdata
    cfg = Config().config

    # 处理结果函数
    def calc_for_all_userdata(self,key,value):
            self.key = key
            self.value = value
            self.result[0] = self.key
            self.result[1] = int(self.value)
            self.calculation(self.key,self.value)
 
    # 判断工资基数函数       
    def calculation(self,key, wage):
        self.jishu = wage
        self.wage = wage
        self.key = key
        if self.jishu < self.cfg['JiShuL']:
            self.jishu = self.cfg['JiShuL']
            num = format(self.abc(self.jishu,self.wage),".2f")
        elif self.jishu > self.cfg['JiShuH']:
            self.jishu = self.cfg['JiShuH']
            num = format(self.abc(self.jishu,self.wage),".2f")
        else:
            num = format(self.abc(self.jishu,self.wage),".2f")

    # 输出CSV文件函数
    def export(self):
        arg = Args()
        with open(arg.getfile('-o'),'w',newline=None) as f:
            for key,value in self.ud.items():
                self.calc_for_all_userdata(key,value)
                writer = csv.writer(f)
                writer.writerows([self.result])

    # 税率判断函数
    def abc(self,jishu, wage):
        self.jishu = jishu
        self.wage = wage
        fee = self.jishu * (self.cfg['YangLao'] + self.cfg['YiLiao'] + self.cfg['ShiYe'] + self.cfg['GongShang'] + self.cfg['ShengYu'] + self.cfg['GongJiJin'])
        self.result[2] = format(fee,".2f")
        income = self.wage - fee - self.threshold
        if self.wage <= self.threshold:
            return self.count(self.wage,fee,income,0,0)
        elif income <= 1500:
            return self.count(self.wage,fee,income,0.03,0)
        elif 1500 < income <= 4500: 
            return self.count(self.wage,fee,income,0.1,105)
        elif 4500 < income <= 9000: 
            return self.count(self.wage,fee,income,0.2,555)
        elif 9000 < income <= 35000: 
            return self.count(self.wage,fee,income,0.25,1005)
        elif 35000 < income <= 55000: 
            return self.count(self.wage,fee,income,0.3,2755)
        elif 55000 < income <= 80000: 
            return self.count(self.wage,fee,income,0.35,5505)
        elif 80000 < income: 
            return self.count(self.wage,fee,income,0.45,13505)
    
    # 工资计算函数
    def count(self,wage,fee,income,rate,quicknum):
        tax = income * rate - quicknum
        self.result[3] = format(abs(tax),".2f")
        after_wage = wage - fee - tax
        self.result[4] = format(after_wage,".2f")
        return after_wage

# 执行
if __name__ == '__main__':
    arg = Args()
    arg.isfile()
    jisuan = IncomeTaxCalculator()  
    jisuan.export()
