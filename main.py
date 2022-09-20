import sys
from trans_star import *

from PyQt5.QtWidgets import QWidget, QTreeView, QApplication, QAbstractItemView, QTableView, QTabWidget, QTextEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QFileSystemModel


class patch_viewer(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(int(size[1] * 0.4), 0, int(size[1]*0.6), size[0])
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["path", "value", "korea"])

        self.setColumnWidth(0, int(size[1] * 0.3))
        self.setColumnWidth(1, int(size[1] * 0.1))

    def reload(self, lines):
        self.model.removeRows(0, self.model.rowCount())

        for e, i in enumerate(lines):
            self.model.insertRow(e)
            self.model.setData(self.model.index(e, 0), i.path)
            self.model.setData(self.model.index(e, 1), i.get_value())
            self.model.setData(self.model.index(e, 2), i.get_value('unicode_escape'))




class explorer(QTreeView):
    def __init__(self, parent, asset):
        super().__init__(parent)
        self.setGeometry(0, 0, int(size[1] * 0.4), size[0])

        self.model = QFileSystemModel()
        # set path
        path = os.getcwd()
        path = os.path.join(path, 'assetfile', asset)
        self.model.setRootPath(path)
        # set model
        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.model.rootPath()))
        # setting

        self.setColumnWidth(0, int(size[1] * 0.5))


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("trans_star")
        self.move(100, 100)

        self.ko_explorer = explorer(self, 'sb_korpatch_union-master')
        self.ch_explorer = explorer(self, 'chinese')
        self.ko_explorer.clicked.connect(self.cil)
        self.ch_explorer.clicked.connect(self.cil)

        self.tab = QTabWidget(self)
        self.tab.addTab(self.ko_explorer, 'Korea')
        self.tab.addTab(self.ch_explorer, 'Chinese')
        self.tab.setGeometry(0, 0, int(size[1] * 0.4), size[0])

        self.viewer = patch_viewer(self)
        self.textedit = QTextEdit(self)
        self.textedit.setGeometry(size[1], 0, int(size[1] * 0.2),int(size[0] * 0.2))

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        model = self.sender().model
        indexitem = model.index(index.row(), 0, index.parent())
        filename = model.fileName(indexitem)
        filepath = model.filePath(indexitem)

        ex = os.path.splitext(filename)[1]
        if ex == '.patch':
            a = patchfile(filepath)
            lines = [i for i in a.get_lines()]
            self.viewer.reload(lines)


if __name__ == "__main__":
    # en_dir = asset.download_original_assets('E:\SteamLibrary\steamapps\common\Starbound')
    # en = asset(en_dir)
    # ko = asset('assetfile\\sb_korpatch_union-master')
    # ch = asset('assetfile\\chinese')
    size = (800, 1000)
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
