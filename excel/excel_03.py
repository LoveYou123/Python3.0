__author__ = 'HelloWorld'
#-*- coding:utf-8 -*-
import xlrd
fname = r'D:\Python3.0\excel\1.xls'
bk = xlrd.open_workbook(fname)
datasheet = bk.sheets()[0]
outfile = open(r'D:\result.txt','w+',encoding='utf-8')
i=0
while i < datasheet.nrows:
    text = datasheet.cell(i,0).value
    print (text)
    i += 1
outfile.close()




