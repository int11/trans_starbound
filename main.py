import sys
from trans_star import *
import json
from PyQt5.QtWidgets import QWidget, QTreeView, QApplication, QAbstractItemView, QTableView, QTabWidget, QPlainTextEdit, \
    QHBoxLayout, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QFileSystemModel


class patch_viewer(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setEditTriggers(QAbstractItemView.DoubleClicked)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["path", "value"])
        self.setColumnWidth(0, int(parent.size().width() * 0.2))
        self.setColumnWidth(1, int(parent.size().width() * 0.05))
        self.clicked.connect(self.cil)

        self.koreatext = QPlainTextEdit(parent)
        self.koreatext.textChanged.connect(self.textchange)
        self.originaltext = QPlainTextEdit(parent)
        self.originaltext.setReadOnly(True)

    def reload(self, lines):
        self.lines = lines
        self.model.removeRows(0, self.model.rowCount())
        for e, i in enumerate(lines):
            self.model.insertRow(e)
            self.model.setData(self.model.index(e, 0), i.path)
            self.model.setData(self.model.index(e, 1),
                               i.value if isinstance(i.value, str) else json.dumps(i.value, ensure_ascii=False))

    def textchange(self):
        value = self.koreatext.toPlainText()
        self.model.setData(self.model.index(self.selectindex, 1), value)
        typ = type(self.lines[self.selectindex].value)
        value = value if typ == str else json.loads(value, strict=False)
        print(type(value))
        print(value)

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        self.selectindex = index.row()
        indexitem = self.model.index(index.row(), 1, index.parent())
        self.koreatext.setPlainText(indexitem.data())
        op = self.lines[self.selectindex].op
        if op == 'add':
            self.originaltext.setPlainText("""This line "op" flag is "add" """)
        elif op == 'replace':
            org = self.lines[self.selectindex].original_value('english')
            self.originaltext.setPlainText(json.dumps(org if isinstance(org, str) else org, ensure_ascii=False))
        else:
            print(f"Not consider this line op flag : {op}")
            raise


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
        self.setColumnWidth(0, int(parent.size().width() * 0.35))


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("trans_star")
        rect = app.desktop().screenGeometry()
        size = (int(rect.height() * 0.8), int(rect.width() * 0.8))
        self.setGeometry(int(rect.height() * 0.1), int(rect.height() * 0.1), size[1], size[0])

        self.ko_explorer = explorer(self, 'korean')
        self.ch_explorer = explorer(self, 'chinese')
        self.ko_explorer.clicked.connect(self.cil)
        self.ch_explorer.clicked.connect(self.cil)

        self.tab = QTabWidget(self)
        self.tab.addTab(self.ko_explorer, 'korean')
        self.tab.addTab(self.ch_explorer, 'chinese')

        self.viewer = patch_viewer(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.tab)
        hbox.addWidget(self.viewer)
        vbox = QVBoxLayout()
        vbox.addWidget(self.viewer.koreatext)
        vbox.addWidget(self.viewer.originaltext)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        model = self.sender().model
        indexitem = model.index(index.row(), 0, index.parent())
        filename = model.fileName(indexitem)
        filepath = model.filePath(indexitem)

        ex = os.path.splitext(filename)[1]

        if ex == '.patch':
            a = patchfile(del_absolute_path(filepath[len(os.getcwd()) + 1:]), 'assetfile\\korean')
            lines = [i for i in a.get_lines()]
            self.viewer.reload(lines)


if __name__ == "__main__":
    # name = asset.download_original_assets('E:\SteamLibrary\steamapps\common\Starbound', 'english')
    # en = asset(name)
    # ko = asset('sb_korpatch_union-master')
    # ch = asset('chinese')

    app = QApplication(sys.argv)

    form = Form()
    form.show()
    exit(app.exec_())
