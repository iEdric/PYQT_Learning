# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 15:10
# @Author  : ChenLi
# @Site    : 
# @File    : pyqtgraph01.py

# import pyqtgraph.examples
# pyqtgraph.examples.run()


# import pyqtgraph as pg
# import numpy as np
# x = np.random.normal(size=1000)
# y = np.random.normal(size=1000)
# pg.plot(x, y, pen=None, symbol='o')

# import pyqtgraph as pg
# import numpy as np
# x = np.arange(1000)
# y = np.random.normal(size=(3, 1000))
# plotWidget = pg.plot(title="Three plot curves")
# for i in range(3):
#     plotWidget.plot(x, y[i], pen=(i,3))
#
# pg.QtGui.QApplication.exec_()

# import initExample  ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.plot()
win.setWindowTitle('pyqtgraph example: Plot data selection')

curves = [
    pg.PlotCurveItem(y=np.sin(np.linspace(0, 20, 1000)), pen='r', clickable=True),
    pg.PlotCurveItem(y=np.sin(np.linspace(1, 21, 1000)), pen='g', clickable=True),
    pg.PlotCurveItem(y=np.sin(np.linspace(2, 22, 1000)), pen='b', clickable=True),
]


def plotClicked(curve):
    global curves
    for i, c in enumerate(curves):
        if c is curve:
            c.setPen('rgb'[i], width=3)
        else:
            c.setPen('rgb'[i], width=1)


for c in curves:
    win.addItem(c)
    c.sigClicked.connect(plotClicked)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()