#"-*-coding:utf-8 -*-"
#'''
#@File    :   weibo_like_scrap
#@Time    :   2021-12-21
#@Author  :   test 
#@Version :   1.0
#@License :   (C)Copyright 2021, Moonvee
#@Desc    :   A weibo spider.

import requests
import re
import time
import csv

#如果想将文件输出成gbk格式，使用ucsv库
#import ucsv

#爬取函数
def get_zpz_num(link):
    headers = {
        "user-Agent" : "Mozilla/5.0 (...此处替换为自己账号信息...",
        "Cookie": "...此处替换为自己账号信息..."
    }
    r = requests.get(link, headers= headers)
    html = r.text

    title_list = re.findall('<./em><em>(.*?)<./em><./span>',html)
    #results = '转发'+title_list[1] + '评论'+title_list[2] + '点赞'+title_list[3]

    return title_list

#读取输入文件
def get_urls(file):
    rowlist = []
    reader = csv.DictReader(file)
    for row in reader:
        rowlist.append(row['url'])
    return rowlist

#输出首行标题
def out_data_title(path):
    csv_writer = csv.writer(open(path, "a+", newline=''))
    csv_writer.writerow(['links','zhuanfa','pinglun','dianzan'])
    #csv_writer = ucsv.writer(open(path, "wb", newline='',coding='gbk))
    #csv_writer.writerow(['链接','转发','评论','点赞'])

#输出爬取数据     
def out_data(path,row):
    with open(path, "a+", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(row)


if __name__ == '__main__':
    mylist = []
    count = 0   #累计爬取条数
    countok = 0 #累计爬取成功的条数
    countfalse = 0  #累计爬取失败的条数
    
    filein = open("weibo_like_scrap\\data.csv", "r")    #输入数据文件
    fileout ="weibo_like_scrap\\out.csv"    #输出文件
    
    urls = get_urls(filein)
    out_data_title(fileout)
    
    for links in urls:
        try:
            result = get_zpz_num(links)
            mylist.append((links,result[1],result[2],result[3]))    #爬取的单条结果存储在list中，部分微博没有转发、评论或点赞数值，则存储在微博上的对应文字
            time.sleep(2)   #自主调节每个链接间的访问间隔，以免访问过快被系统屏蔽
            countok += 1
            count += 1
            print('第',count,'条成功')
            
            if isinstance(count/200,int) :  #每隔200条，暂停60s，也可以根据情况调节
              time.sleep(60)
            
        except:
            mylist.append((links,'fail','fail','fail')) #失败的爬取会在链接后生成fail
            countfalse += 1
            count += 1
            print('第',count,'条失败')
        
        out_data(fileout,mylist)
        mylist = []

    print('本次共处理', countok+countfalse , '条数据，成功 ',countok, ' 条，失败 ',countfalse,' 条')
    
