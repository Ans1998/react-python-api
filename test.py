# -*- coding: utf-8 -*-
# 爬虫
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import  BeautifulSoup
driver = webdriver.PhantomJS() # js点击
import re # 正则
import datetime # 时间
import os
import csv

import pymysql.cursors

def getFundData(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find("table").tbody.find_all("tr")
    # print(rows)
    result = []
    for row in rows:
        tds = row.find_all('td')
        # print(len(tds))
        if (tds[0].get_text()):
            t = datetime.datetime.now()
            result.append({"time": t.strftime('%Y%m%d%H%M%S')
                              , "ranking": tds[0].get_text()
                              , "name": tds[1].get_text()
                              , "heat": tds[2].get_text()
                              , "marketPrice": tds[3].get_text()
                              , "legalPrice": tds[4].get_text()
                              , "amountIncrease": tds[5].get_text()
                           }
                          )
    return result
def testP():
    # 测试爬虫代码
    # driver.get('https://gz.ke.com/ershoufang/')
    # src = eval('driver.find_element_by_tag_name("body").text')
    # print(src)
    # with open("./htmls/3.txt", 'wb') as f:
    #     f.write(src.encode('utf8'))
    #     f.close()

    # 测试打开文件保存为csv文件
    datadir = "./htmls"
    allpath = os.listdir(datadir)
    allresult = []
    for p in allpath:
        if os.path.isfile(os.path.join(datadir, p)):
            with open(os.path.join(datadir, p), "rb") as f:
                fileCnt = f.read().decode('utf-8')
                f.close()
                allresult = allresult + getFundData(fileCnt)
    print(allresult)
    filesName = datetime.datetime.now()
    with open("./csvfiles/"+ filesName.strftime('%Y%m%d%H%M%S') +".csv", 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'ranking', 'name', "heat", 'marketPrice', 'legalPrice', "amountIncrease"])
        for r in allresult:
            writer.writerow([r["time"], r["ranking"], r["name"], r["heat"], r["marketPrice"], r["legalPrice"], r["amountIncrease"]])
        f.close()
# testP()

def testS(time, ranking, name, heat, marketPrice, legalPrice, amountIncrease):
    connection = pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    db='test',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `testData` (`time`, `ranking`, `name`, `heat`, `marketPrice`, `legalPrice`, `amountIncrease`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (time, ranking, name, heat, marketPrice, legalPrice, amountIncrease))
        connection.commit()
    finally:
        connection.close()
# testS()

def testA():
    datadir = "./htmls"
    allpath = os.listdir(datadir)
    dataList = []
    for p in allpath:
        if os.path.isfile(os.path.join(datadir, p)):
            with open(os.path.join(datadir, p), "rb") as f:
                fileCnt = f.read().decode('utf-8')
                f.close()
            resultSet = getFundData(fileCnt)
            for result in resultSet:
                dataList.append(result)
    # print(dataList)
    for res in dataList:
        print(res)
        testS(res['time'], res['ranking'], res['name'], res['heat'], res['marketPrice'], res['legalPrice'], res['amountIncrease'])
# testA()
def testC():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `testData`"
            cursor.execute(sql)
            # result = cursor.fetchone() # 取一行记录
            # result = cursor.fetchmany(2) # 取两行记录
            result = cursor.fetchall() # 取全部
            print(result)
    finally:
        connection.close()
testC()