__author__ = 'HelloWorld'
#-*- coding:utf-8 -*-
import xlrd
import xlwt
import datetime
def testXlrd(filename):
    book=xlrd.open_workbook(filename)
    sh=book.sheet_by_index(0)
    print("Worksheet name(s):",book.sheet_names()[0])
    print('book.nsheets',book.sheets())
    print ('sh.name:',sh.name,'sh.rows：','sh.nclos:',sh.ncols)
    print ('A1:',sh._cell_values(rowx=0,colx=1))
    #如国A3的内容为中文
    print('A2:',sh._cell_values(0,2).encode('gb2312'))
def testXlwt(filename):
    book=xlwt.Workbook()
    sheet1=book.add_sheet('hello')
    book.add_sheet('word')
    sheet1.write(0,0,'hello')
    sheet1.write(0,1,'world')
    row1 = sheet1.row(1)
    row1.write(0,'A2')
    row1.write(1,'B2')

    sheet1.col(0).width = 10000
    sheet2 = book.get_sheet(1)
    sheet2.row(0).write(0,'sheet 2 A1')
    sheet2.row(0).write(1,'sheet2 B1')
    sheet2.flush_row_data()
    sheet2.write(1,0,'sheet 2 A3')
    sheet2.col(0).width = 5000
    sheet2.col(0).hidden = True
    book.save(filename)
if __name__=='__main__':
    testXlrd(u'你好.xls')
    testXlwt('HelloWorld.xls')
    base=datetime.date(2015,10,31).toordinal()
    tmp=datetime.date(2013,10,31).toordinal()
    print (datetime.date.fromordinal(tmp+base-1).weekday())

