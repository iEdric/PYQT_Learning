# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 17:19
# @Author  : ChenLi
# @Site    : 
# @File    : APP.py
from PyQt5 import QtWidgets,QtCore,QtGui
import pyqtgraph as pg
import sys
import datetime
import traceback
import numpy as np
import os
import pandas as pd
#从bin获取数据
def get_feature(BASE_DIR,filename):
    lbl_path = os.path.join(BASE_DIR,filename)
    data = np.fromfile(lbl_path, dtype=np.float)
    # print(len(data),filename,'----->',data)
    return data

def get_AirAHid(baseurl):
    Aid = []
    Adur = []
    aurl = baseurl + '\\Air_Aid.bin'
    if os.path.exists(aurl):
        Aid = get_feature(baseurl,'Air_Aid.bin')
        Aid = np.reshape(np.array(Aid), (-1))
        Adur = get_feature(baseurl,'Air_Adur.bin')
        Adur = np.reshape(np.array(Adur), (-1))
    # print(Aid)
    # print(len(Aid), len(Adur))

    Hid = []
    Hdur = []
    hurl = baseurl + '\\Air_Hid.bin'
    if os.path.exists(hurl):
        Hid = get_feature(baseurl,'Air_Hid.bin')
        Hid = np.reshape(np.array(Hid), (-1))
        Hdur = get_feature(baseurl,'Air_Hdur.bin')
        Hdur = np.reshape(np.array(Hdur), (-1))
    # print(Hid)
    # print(len(Hid), len(Hdur))
    return {'A':dict(zip(Aid,Adur)),
            'H':dict(zip(Hid,Hdur))}
    # return {'A':{'Aid':Aid,'Adur':Adur},
    #         'H':{'Hid':Hid,'Hdur':Hdur}}

class pg_pwidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.cl_data = []
        self.cl_preIndex = 0
        self.cl_currentIndex = 0

    def mousePressEvent(self, ev):
        print('信号长度--》',len(self.cl_data))
        pos = ev.pos()
        if self.plotItem.sceneBoundingRect().contains(pos):
            vb = self.plotItem.vb
            mouseP = vb.mapSceneToView(pos)
            index = int(mouseP.x())
            pos_y = int(mouseP.y())
            if 0 < index < len(self.cl_data):
                print(index,pos_y)
                print(index,self.cl_data[index])
                self.cl_preIndex = self.cl_currentIndex
                self.cl_currentIndex = index



        return  super().mousePressEvent(ev)

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.baseUrl = '.\\hpt\\'
        self.setWindowTitle("信号标记软件by-CL")
        self.main_widget = QtWidgets.QWidget()  # 创建一个主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建一个网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置主部件的布局为网格
        self.setCentralWidget(self.main_widget)  # 设置窗口默认部件

        self.plot_widget = QtWidgets.QWidget()  # 实例化一个widget部件作为K线图部件
        self.plot_layout = QtWidgets.QGridLayout()  # 实例化一个网格布局层
        self.plot_widget.setLayout(self.plot_layout)  # 设置线图部件的布局层
        self.p1 = pg_pwidget()  # 实例化一个绘图部件
        self.p1.showGrid(x=True,y=True) # 显示图形网格
        self.plot_layout.addWidget(self.p1)  # 添加绘图部件到线图部件的网格布局层
        # 将上述部件添加到布局层中
        self.main_layout.addWidget(self.plot_widget, 1, 0, 3, 3)

        self.setCentralWidget(self.main_widget)
        # self.plot_plt.setYRange(max=8000,min=-100)
        self.data_list = get_feature(self.baseUrl,'airOrg.bin')
        self.data_diclist = dict(enumerate(self.data_list))
        self.p1.plot().setData(self.data_list, pen='g')
        self.p1.cl_data = self.data_diclist

        self.btn = QtWidgets.QPushButton('保存')
        self.btn.clicked.connect(self.btnstate)
        self.plot_layout.addWidget(self.btn)

        self.p2 = pg_pwidget()  # 实例化一个绘图部件
        self.p2.showGrid(x=True,y=True) # 显示图形网格
        self.plot_layout.addWidget(self.p2)  # 添加绘图部件到线图部件的网格布局层
        self.oxy = get_feature(self.baseUrl,'oxy.bin')
        self.p2.plot().setData(self.oxy, pen='g')
        self.lr = pg.LinearRegionItem()
        self.lr.setZValue(10)
        self.p2.addItem(self.lr)

        self.lr.sigRegionChanged.connect(lambda: self.updateRegion(1))
        self.p1.sigRangeChanged.connect(lambda: self.updateRegion(2))



    def cl_drawAHsingh(self):
        #获取AH
        AHdic = get_AirAHid(baseurl=self.baseUrl)
        print(AHdic)
        print(AHdic['A'])
        print(AHdic['A'].keys())
        print(AHdic['A'].values())
        print(AHdic['A'].items())
        #呼吸暂停
        for k,v in AHdic['A'].items():
            print(k,v)
            idArr = []
            valueArr = []
            for v1 in range(int(v)):
                id = k + v1
                value = self.data_diclist[k+v1]
                print(id,value)
                idArr.append(id)
                valueArr.append(value)
            self.p1.plot().setData(x=idArr, y=valueArr, pen='r')

        #呼吸低通气
        for k,v in AHdic['H'].items():
            print(k,v)
            idArr = []
            valueArr = []
            for v1 in range(int(v)):
                id = k + v1
                value = self.data_diclist[k+v1]
                print(id,value)
                idArr.append(id)
                valueArr.append(value)
            self.p1.plot().setData(x=idArr, y=valueArr, pen='m')



    def cl_drawOxyef(self):
        oxy = []
        oxy_ef = []
        aurl = self.baseUrl + '\\oxy.bin'
        if os.path.exists(aurl):
            oxy = get_feature(self.baseUrl, 'oxy.bin')
            oxy = np.reshape(np.array(oxy), (-1))
            oxy_ef = get_feature(self.baseUrl, 'oxyef.bin')
            oxy_ef = np.reshape(np.array(oxy_ef), (-1))
        print(oxy)
        print(len(oxy), len(oxy_ef))

        startidArr = []
        durArr = []
        j = 0
        for i, value in enumerate(oxy_ef):
            if i < len(oxy_ef) - 1:
                if value == 1 and oxy_ef[i - 1] == 0:  # 前前
                    startidArr.append(i)
                if value == 1 and oxy_ef[i + 1] == 1:  # 前后
                    j = j + 1
                if value == 1 and oxy_ef[i + 1] == 0:  # 后后
                    durArr.append(j)
                    j = 0

        print(len(startidArr), startidArr)
        print(len(durArr), durArr)
        for k,v in enumerate(startidArr):
            kid = v
            vid = durArr[k]
            print(kid,vid)
            idArr = []
            valueArr = []
            for v1 in range(int(vid)):
                need_id = kid + v1
                need_value = oxy[kid+v1]
                idArr.append(need_id)
                valueArr.append(need_value)
            self.p2.plot().setData(x=idArr, y=valueArr, pen='r')

    def btnstate(self):
        print('button released')
        print(self.p1.cl_preIndex,self.p1.cl_currentIndex)
        kid = self.p1.cl_preIndex
        kiddur = int(self.p1.cl_currentIndex)-int(kid)
        if kiddur > 0:
            idArr = []
            valueArr = []
            for v1 in range(int(kiddur)):
                need_id = kid + v1
                need_value = self.data_list[kid + v1]
                idArr.append(need_id)
                valueArr.append(need_value)
            self.p1.plot().setData(x=idArr, y=valueArr, pen=(255,50,78))
            #保存数据到csv
            savedata = np.reshape([kid,kiddur],(1,-1))
            df = pd.DataFrame(savedata)
            df.to_csv(self.baseUrl+'AddAH.csv',mode='a',index=False,header=False)


    def updateRegion(self,n):
        # print(n)
        if n == 1:
            self.p2.setXRange(*self.lr.getRegion(),padding=0)
            # self.p2.setRange(self.p1.viewRect())
        if n == 2:
            self.lr.setRegion(self.p1.getViewBox().viewRange()[0])


    def cl_getcsvAH(self):
        url = self.baseUrl+'AddAH.csv'
        if os.path.exists(url):
            data = pd.read_csv(url,header=None)
            print(data.shape)
            # print(np.array(data))
            # print(dict(np.array(data)))
            datadic = dict(np.array(data))
            for k,v in datadic.items():
                print(k,v)
                idArr = []
                valueArr = []
                for v1 in range(int(v)):
                    id = k + v1
                    value = self.data_diclist[k+v1]
                    print(id,value)
                    idArr.append(id)
                    valueArr.append(value)
                self.p1.plot().setData(x=idArr, y=valueArr, pen=(255,50,78))


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.cl_drawAHsingh()
    gui.cl_drawOxyef()
    gui.cl_getcsvAH()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



