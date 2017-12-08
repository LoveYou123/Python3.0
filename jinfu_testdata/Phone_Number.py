#-*-coding:utf-8-*-
import random

def make_phone_numb(num_file=r'D:\phone_numbers04.txt',n=1000):
    prefix =['187','188','189','156','131','182','155','151','136','133']
    numbers = '0123456789'
    f = open(num_file,'w')
    while n >=1:
        phone_num = random.choice(prefix)
        for i in random.sample(numbers,8):
            phone_num +=i
        f.write(phone_num+'\n')
        n -=1
    f.close()

make_phone_numb()