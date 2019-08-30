#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
import json

import datetime # 时间
import os

from bs4 import  BeautifulSoup
import csv

import pymysql


app = Flask(__name__)
# 解决跨域
CORS(app)

# 爬虫
from selenium import webdriver
driver = webdriver.PhantomJS() # js点击
import re # 正则

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# 爬取指定页面(保存html)
@app.route('/api/get', methods=['POST', 'GET'])
def get():
    # if not request.json or not 'website' in request.json:
    #     return make_response(jsonify({'code': '405', 'error': '请求参数不正确'}), 200)
    try:
        # arr = str(json.loads(request.get_data())[0]['website'])

        # 获取post过来的数据
        arr = json.loads(request.get_data())
        # test = str(arr)
        # with open("./htmls/1.txt", 'wb') as f:
        #     f.write(test.encode('utf8'))
        #     f.close()

        link = ''
        for val in arr:
            if 'key' in val:
                if val['key'] == 'class':
                    # class
                    link = link + 'find_element_by_class_name("'+val['val'] +'").'
                elif val['key'] == 'id':
                    # id
                    link = link + 'find_element_by_id("'+val['val'] +'").'
                else:
                    # tag
                    link = link + 'find_element_by_tag_name("'+val['val'] +'").'

        # 拼接xpath
        linkXpath = str('driver.' + link + 'get_attribute("innerHTML")')
        # with open("./htmls/2.txt", 'wb') as f:
        #     f.write(linkXpath.encode('utf8'))
        #     f.close()

        # 测试爬虫代码
        # driver.get('https://gz.ke.com/ershoufang/')
        # src = eval(linkXpath)
        # with open("./htmls/3.txt", 'wb') as f:
        #     f.write(src.encode('utf8'))
        #     f.close()

        driver.get(arr[0]['website'])
        res = eval(linkXpath)
        filesName = datetime.datetime.now()
        with open("./htmls/" + filesName.strftime('%Y%m%d%H%M%S')+".txt", 'wb') as f:
            f.write(res.encode('utf8'))
            f.close()
        return jsonify({'code': '200', 'msg': '爬取成功', 'data': ''}), 200
    except:
        return jsonify({'code': '200', 'msg': '爬取异常', 'data': ''}), 200

#读取爬到的文件 (http://127.0.0.1:5000/getFile/20190601145109.txt)
@app.route('/getFile/<path>')
def getFile(path):
    pathFile = os.path.dirname(__file__)
    base_dir = pathFile + '\htmls'
    f = open(os.path.join(base_dir, path), 'rb')
    resp = f.read()
    f.close()
    return resp

# 爬到的文件列表
@app.route('/api/getFile/list',  methods=['POST', 'GET'])
def getFileList():
    try:
        datadir = "./htmls"
        allpath = os.listdir(datadir)
        list = []
        for i in range(0, len(allpath)):
            l = {
                'name': allpath[i],
                'key': i
            }
            list.append(l)
        data = {
            'list': list,
            'total': len(allpath)
        }
        return jsonify({'code': '200', 'msg': '查询成功', 'data': data}), 200
    except:
        return jsonify({'code': '200', 'msg': '查询异常'}), 200

#删除文件
@app.route('/api/getFile/del', methods=['POST', 'GET'])
def getFileDel():
    if not request.json or not 'fileName' in request.json:
        return make_response(jsonify({'code': '405', 'msg': '请求参数不正确', 'data': ''}), 200)
    try:
        fileName = request.json['fileName']
        pathFile = os.path.dirname(__file__)
        base_dir = pathFile + '\htmls'
        os.remove(os.path.join(base_dir, fileName))
        return jsonify({'code': '200', 'msg': '删除成功', 'data': fileName}), 200
    except:
        return jsonify({'code': '405', 'msg': '删除异常', 'data': ''}), 200

# csv文件列表
@app.route('/api/getCsvFile/list',  methods=['POST', 'GET'])
def getCsvFile():
    try:
        datadir = "./csvfiles"
        allpath = os.listdir(datadir)
        list = []
        for i in range(0, len(allpath)):
            l = {
                'name': allpath[i],
                'key': i
            }
            list.append(l)
        data = {
            'list': list,
            'total': len(allpath)
        }
        return jsonify({'code': '200', 'msg': '查询成功', 'data': data}), 200
    except:
        return jsonify({'code': '200', 'msg': '查询异常'}), 200
#读取csv文件 (http://127.0.0.1:5000/getCsvFile/20190601145109.txt)
@app.route('/getCsvFile/<path>')
def getLookCsvFile(path):
    pathFile = os.path.dirname(__file__)
    base_dir = pathFile + '\csvfiles'
    f = open(os.path.join(base_dir, path), 'rb')
    resp = f.read()
    f.close()
    return resp
#删除csv文件
@app.route('/api/getCsvFile/del', methods=['POST', 'GET'])
def getCsvFileDel():
    if not request.json or not 'fileName' in request.json:
        return make_response(jsonify({'code': '405', 'msg': '请求参数不正确', 'data': ''}), 200)
    try:
        fileName = request.json['fileName']
        pathFile = os.path.dirname(__file__)
        base_dir = pathFile + '\csvfiles'
        os.remove(os.path.join(base_dir, fileName))
        return jsonify({'code': '200', 'msg': '删除成功', 'data': fileName}), 200
    except:
        return jsonify({'code': '405', 'msg': '删除异常', 'data': ''}), 200

#进库
@app.route('/api/createSvcSaveData', methods=['POST', 'GET'])
def createSvcSaveData():
    if not request.json or not 'fileName' in request.json:
        return make_response(jsonify({'code': '405', 'msg': '请求参数不正确', 'data': ''}), 200)
    try:
        fileName = request.json['fileName']
        pathFile = os.path.dirname(__file__)
        base_dir = pathFile + '\htmls'
        allresult = []
        with open(os.path.join(base_dir, fileName), "rb") as f:
            fileCnt = f.read().decode('utf-8')
            f.close()
            allresult = getFundData(fileCnt)
        # print(allresult)
        for res in allresult:
            # print(res)
            saveToDB(res['time'], res['ranking'], res['name'], res['heat'], res['marketPrice'], res['legalPrice'],
                  res['amountIncrease'])
        return jsonify({'code': '200', 'msg': '保存成功', 'data': ''}), 200
    except:
        return jsonify({'code': '405', 'msg': '保存异常', 'data': ''}), 200
# 生成csv文件
@app.route('/api/createCsv', methods=['POST', 'GET'])
def createCsv():
    if not request.json or not 'fileName' in request.json:
        return make_response(jsonify({'code': '405', 'msg': '请求参数不正确', 'data': ''}), 200)
    try:
        fileName = request.json['fileName']
        pathFile = os.path.dirname(__file__)
        base_dir = pathFile + '\htmls'
        allresult = []
        with open(os.path.join(base_dir, fileName), "rb") as f:
            fileCnt = f.read().decode('utf-8')
            f.close()
            allresult = getFundData(fileCnt)
        print(allresult)
        filesName = datetime.datetime.now()
        with open("./csvfiles/" + filesName.strftime('%Y%m%d%H%M%S') + ".csv", 'w', encoding="utf-8",
                  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'ranking', 'name', "heat", 'marketPrice', 'legalPrice', "amountIncrease"])
            for r in allresult:
                writer.writerow([r["time"], r["ranking"], r["name"], r["heat"], r["marketPrice"], r["legalPrice"],
                                 r["amountIncrease"]])
            f.close()

        return jsonify({'code': '200', 'msg': '生成成功', 'data': ''}), 200
    except:
        return jsonify({'code': '405', 'msg': '生成异常', 'data': ''}), 200
#进库
def saveToDB(time, ranking, name, heat, marketPrice, legalPrice, amountIncrease):
    print(name)
    connection = pymysql.connect(host='localhost',
                    user='root',
                    password='',
                    db='test',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `testData` (`time`, `ranking`, `name`, `heat`, `marketPrice`, `legalPrice`, `amountIncrease`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (time, ranking, name, heat, marketPrice, legalPrice, amountIncrease))
        connection.commit()
    finally:
        connection.close()
# 处理文件
def getFundData(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find("table").tbody.find_all("tr")
    # print(rows)
    result = []
    for row in rows:
        tds = row.find_all('td')
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

# 查库
@app.route('/api/getToDB', methods=['POST', 'GET'])
def getToDB():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='test',
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `testData`"
        cursor.execute(sql)
        result = cursor.fetchall()  # 取全部
        print(result)
        list = {
            'res': result
        }
    return jsonify({'code': '200', 'msg': '查询成功', 'data': list}), 200
    # try:
    #     with connection.cursor() as cursor:
    #         sql = "SELECT * FROM `testData`"
    #         cursor.execute(sql)
    #         result = cursor.fetchall() # 取全部
    #         print(result)
    #         # list = {
    #         #     'res': result
    #         # }
    #     return jsonify({'code': '200', 'msg': '查询成功', 'data': 'aasssa' }), 200
    # finally:
    #     connection.close()
    #     return jsonify({'code': '405', 'msg': '查询异常', 'data': ''}), 200

# 测试代码
@app.route('/api/post', methods=['POST'])
def post():
    if not request.json or not 'title' in request.json:
        return make_response(jsonify({'code':'405','msg': '请求参数不正确', 'data': ''}), 400)
    task = {
        'id': request.json['id'],
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': request.json['done']
    }
    return jsonify({'task': task}), 200

@app.route('/api/getWebMsg', methods=['POST', 'GET'])
def getWebMsg():
    # if not request.json or not 'website' in request.json:
    #     return make_response(jsonify({'code': '405', 'error': '请求参数不正确'}), 200)
    try:
        if not request.json or not 'fileName' in request.json:
            return make_response(jsonify({'code': '405', 'msg': '请求参数不正确', 'data': ''}), 200)
        return jsonify({'code': '200', 'msg': '爬取成功', 'data': ''}), 200
    except:
        return jsonify({'code': '405', 'msg': '爬取异常', 'data': ''}), 200

if __name__ == '__main__':
    app.run(debug=True)