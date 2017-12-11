__author__ = 'HelloWorld'
#-*- coding: utf-8 -*-
from selenium import webdriver
import xlrd
import time
url = "http://zldsj.com/"
userName = 'zhuxinyu'
Passwd = '111111'
#打开浏览器
ff = webdriver.Firefox()
ff.get(url)
time.sleep(2)

#获取当前浏览器窗口的handler
orignalWindow =ff.current_window_handle

userInput = ff.find_element_by_id('username')
PasswdInput = ff.find_element_by_id('password')
LoginButton = ff.find_element_by_id('submitButton')

#清空用户名、密码输入框中的内容
userInput.clear()
PasswdInput.clear()

#输入用户名及密码
userInput.send_keys(userName)
PasswdInput.send_keys(PasswdInput)

#登录DI网站
LoginButton.submit()
time.sleep(3)

#切换到专利标签表格模式下
PatentTab = ff.find_element_by_xpath('//a[@title="专利"]')
PatentTab.click()

#展开折叠内容
ff.find_elements_by_id('addPatent').click()
#点选所有国家
Countries = ff.find_element_by_class_name('span[class="floatLeft"]')
#依次点击所有国家
for ctry in Countries:
    ctry.click()

#获取输入框
inputText = ff.find_elements_by_id('expressCN')

#要读取的excel文件
excelFile = r'D:\utf8.xls'
dataIn =xlrd.open_workbook(excelFile)

#获取第一个sheet
datasheet = dataIn.sheets()[0]

#结果保存在PatentData.txt里面
outfile = open(r'D:\result.txt','w+')

#读取第二条数据，cell(m,n)m是第几行,n是第几列，从0开始
i = 2
while i < datasheet.nrows:
    try:

        text =datasheet.cell(i,1).value

        #清空
        inputText.clear()

        #输入检索内容，由于每一条都很长，因此需要等待几秒
        inputText.send_keys(text)
        time.sleep(4)

        #执行检索
        searchBt = ff.find_elements_by_id('submitExpress')
        searchBt.click()

        #由于检索后生成了新窗口，因此要切换过去
        newWindow = ff.window_handles[1]
        ff.switch_to_window(newWindow)
        time.sleep(4)

        #获取检索结果条数
        resultCount = ff.find_element_by_css_selector('span[class ^= "rightContentTipNum"]').text

        #关闭结果窗口
        ff.close()
        #切换到原来的窗口
        ff.switch_to_window(orignalWindow)
    except:
        resultCount = '0'

    outfile.write(text + '\t' +str(resultCount) +'\n')
    i += 1

#数据检索完毕，退出浏览器
ff.quit()

#关闭文件
outfile.close()

print('数据检索完毕!')


