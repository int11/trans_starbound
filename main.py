import sys
from trans_star import *

from PyQt5.QtWidgets import QWidget, QTreeView, QApplication, QAbstractItemView, QTableView, QTabWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QFileSystemModel


class patch_viewer(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.setGeometry(600, 0, 1500, 1500)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["path", "value", "korea"])

        self.setColumnWidth(0, 600)
        self.setColumnWidth(1, 500)

    def reload(self, path):
        self.model.removeRows(0, self.model.rowCount())
        a = patchfile(path)
        lines = [i for i in a.get_lines()]
        for e, i in enumerate(lines):
            self.model.insertRow(e)
            self.model.setData(self.model.index(e, 0), i.path)
            self.model.setData(self.model.index(e, 1), i.get_value())
            self.model.setData(self.model.index(e, 2), i.get_value('unicode_escape'))


class explorer(QTreeView):
    def __init__(self, parent, asset):
        super().__init__(parent)
        self.model = QFileSystemModel()
        # set path
        path = os.getcwd()
        path = os.path.join(path, 'assetfile', asset)
        self.model.setRootPath(path)
        # set model
        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.model.rootPath()))
        # setting
        self.setGeometry(0, 0, 600, 1500)
        self.setColumnWidth(0, 800)


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("ItemView QTreeView")
        self.move(100, 100)
        self.ko_explorer = explorer(self, 'sb_korpatch_union-master')
        self.ch_explorer = explorer(self, 'chinese')
        self.ko_explorer.clicked.connect(self.cil)
        self.ch_explorer.clicked.connect(self.cil)

        self.tab = QTabWidget(self)
        self.tab.addTab(self.ko_explorer, 'Korea')
        self.tab.addTab(self.ch_explorer, 'Chinese')
        self.tab.setGeometry(0, 0, 600, 1500)

        self.viewer = patch_viewer(self)

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        indexitem = self.ko_explorer.model.index(index.row(), 0, index.parent())
        filename = self.ko_explorer.model.fileName(indexitem)
        filepath = self.ko_explorer.model.filePath(indexitem)

        ex = os.path.splitext(filename)[1]
        if ex == '.patch':
            self.viewer.reload(filepath)


if __name__ == "__main__":
    # en_dir = asset.download_original_assets('E:\SteamLibrary\steamapps\common\Starbound')
    # en = asset(en_dir)
    # ko = asset('assetfile\\sb_korpatch_union-master')
    # ch = asset('assetfile\\chinese')

    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
