#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import requests
from bs4 import BeautifulSoup
import os
import time
import random
import threading

all_url = 'https://www.meitulu.com/item/'
img_url='https://www.meitulu.com/img.html?img=https://mtl.ttsqgs.com/images/img/'
img_ture='https://mtl.ttsqgs.com/images/img/'
#http请求头
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'https://www.meitulu.com'
               }
path = 'E:/meitulu/'
flag=2
prT=0
threads = []

class xa_AI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # QAction是菜单栏、工具栏或者快捷键的动作的组合。
        # 我们创建了一个图标、一个exit的标签和一个快捷键组合，都执行了一个动作
        exitAct = QAction(QIcon('exit.png'), '退出', self) #
        exitAct.setShortcut('Ctrl+Q') # 设置快捷键
        # 创建了一个状态栏
        exitAct.setStatusTip('退出本程序')
        # 当执行这个指定的动作时，就触发了一个事件
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()


        qF=QFrame(self)
        qF.setFrameShape(QFrame.StyledPanel)
        qF.setGeometry(2,28,200,310)
        self.setStatusTip("就绪")
        self.statusBar()
        lblA=QLabel("输入编号:",qF)
        lblA.setGeometry(5,13,140,20)
        lblAA=QLabel("结束编号:",qF)
        lblAA.setGeometry(5,33,140,20)
        self.txtA=QLineEdit(qF)
        self.txtA.setGeometry(65,10,100,20)
        self.txtAA=QLineEdit(qF)
        self.txtAA.setGeometry(65,32,100,20)
        btnA = QPushButton('提  取',qF)
        btnA.clicked.connect(self.on_click)
        btnA.setGeometry(5,68,140,24)

        qS=QFrame(self)
        qS.setFrameShape(QFrame.StyledPanel)
        qS.setGeometry(210,28,336,310)
        lblB=QLabel("输出信息:",qS)
        lblB.setGeometry(5,13,140,20)
        self.txtB=QTextEdit('',qS)
        self.txtB.setGeometry(5,38,325,265)
        # menuBar()创建菜单栏。这里创建了一个菜单栏，并在上面添加了一个file菜单，
        # 并关联了点击退出应用的事件。
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('文件')
        fileMenu.addAction(exitAct)
        self.setFixedSize(550, 360)
        self.setGeometry(100, 100, 550, 360)
        self.setWindowTitle('慧聚社-AI项目')
        self.show()

    def on_click(self):
        sItem=self.txtA.text()
        pItem=self.txtAA.text()
        for i in range(int(sItem),int(pItem),-1):
            sUrl=all_url+str(i)+'.html'
            #self.txtB.append("提取开始！")
            self.start_t(sUrl, i)

    def start_t(self,sUrl,sItem):
        t = threading.Thread(target=self.get_Meitulu, args=(sUrl, sItem))
        t.start()

    def get_Meitulu(self,sUrl, sItem):
        start_html = requests.get(sUrl, headers=Hostreferer)
        start_html.encoding = 'utf-8'
        soup = BeautifulSoup(start_html.text, "html.parser")
        iName = soup.find("div", class_="weizhi").find("h1").text.strip()
        #print("模特名称:" + iName)
        self.txtB.append(iName)

        iTemPage = soup.find("div", class_="c_l").find_all("p")
        #print("itemCount=" + str(len(iTemPage)))
        if len(iTemPage) == 6:
            pageItem = iTemPage[2].text
            pageItem = pageItem.replace("张", "").replace("图片数量：", "").strip()
            #print("图片数量:" + pageItem)
            if not iTemPage[4].find("a"):
                mName = iTemPage[4].text.replace("模特姓名：", "").strip()
            else:
                mName = iTemPage[4].find("a").text.strip()
            #print("目录名称:" + mName)
            self.txtB.append(mName + "图片数量:" + pageItem)
        else:
            pageItem = iTemPage[1].text
            pageItem = pageItem.replace("张", "").replace("图片数量：", "").strip()
            #print("图片数量:" + pageItem)
            if not iTemPage[3].find("a"):
                mName = iTemPage[3].text.replace("模特姓名：", "").strip()
            else:
                mName = iTemPage[3].find("a").text.strip()
            #print("目录名称:" + mName)
            self.txtB.append(mName + "图片数量:" + pageItem)
        flag = self.checkFloder_mName(mName, iName)
        if (flag == 1 and len(os.listdir(path + mName.replace('?', '') + "/" + iName.replace('/', ''))) >= int(
                pageItem)):
            print('已经保存完毕，跳过')
        else:
            ipath = path + mName.replace('?', '') + "/" + iName.replace('/', '') + "/"
            for num in range(1, int(pageItem) + 1):
                try:
                    time.sleep(random.random())
                    iPic = img_url + str(sItem) + '/' + str(num) + '.jpg'
                    iMgture = img_ture + str(sItem) + '/' + str(num) + '.jpg'
                    file_name = iPic.split(r'/')[-1]
                    html = requests.get(iPic, headers=Hostreferer)
                    html.encoding = 'utf-8'
                    mess = BeautifulSoup(html.text, "html.parser")
                    Picreferer = {
                        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
                        'Referer': iPic
                    }
                    html = requests.get(iMgture, headers=Picreferer)
                    #print(iMgture)
                    self.txtB.append(iMgture)
                    f = open(ipath + file_name, 'wb')
                    f.write(html.content)
                    f.close()
                except Exception as e:
                    print(e)
                    pass
            time.sleep(1)
        self.txtB.append(iName+" 图片提取完毕！")
    def checkFloder_mName(self,mName, iName):
        # win不能创建带？的目录
        if (os.path.exists(path + mName.replace('?', ''))):
            print('目录已存在')
        else:
            os.makedirs(path + mName.replace('?', ''))
        if (os.path.exists(path + mName.replace('?', '') + "/" + iName.replace('/', ''))):
            # print('目录已存在')
            flag = 1
        else:
            os.makedirs(path + mName.replace('?', '') + "/" + iName.replace('/', ''))
            flag = 0
        return flag


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = xa_AI()
    ex.show
    sys.exit(app.exec_())