#-*- encoding:utf-8 -*-
import random

card_prefix = []
with open(r'D:/Python3.0/header.txt','r') as f:
    for line in f:
        card_prefix.append(line.rstrip())
        
        
#print(len(card_prefix))


def make_cardID(num = 10):
        
    for i in range(num):
        prefix_part = random.choice(card_prefix)
        year = random.randint(1950,1996)
        month = random.randint(1,12)
        day = random.randint(1,31)
        if month == 2: #二月
            if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0): #闰年
                if day > 29:
                    continue
            else:
                if day > 28:
                    continue
                    
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
            
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
            
        year = str(year)
        middle_part = year + month + day
        
        #结尾随机取4位
        suffix_part = ''
        x = [ random.randint(0,9) for i in range(4) ]
        for n in x:
            suffix_part += str(n)
        
        #完整ID
        full_id = prefix_part + middle_part + suffix_part
        
        print(full_id)
        

if __name__ == '__main__':
    make_cardID(1000)
        
        
        
                    
    