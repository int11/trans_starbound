import glob
import json
import sys

from PyQt5 import QtCore
from PyQt5.Qt import QFileSystemModel
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QTreeView, QApplication, QAbstractItemView, QPlainTextEdit, \
    QHBoxLayout, QVBoxLayout
from PyQt5 import QtWidgets
from trans_star import *


class patch_viewer(QTreeView):
    def __init__(self, parent):
        super().__init__(parent)
        self.lines = None
        self.selectindex = None
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def reload(self, patch):
        self.lines = [i for i in patch.get_lines()]

        self.model.removeRows(0, self.model.rowCount())
        for e, i in enumerate(self.lines):
            self.model.insertRow(e)
            self.model.setData(self.model.index(e, 0), i.path)
            self.model.setData(self.model.index(e, 1),
                               i.value if isinstance(i.value, str) else json.dumps(i.value, ensure_ascii=False))

    def textchange(self):
        if not self.selectindex is None:
            value = self.koreatext.toPlainText()
            self.model.setData(self.model.index(self.selectindex, 1), value)
            typ = type(self.lines[self.selectindex].value)
            self.lines[self.selectindex].value = value if typ == str else json.loads(value, strict=False)
            self.lines[self.selectindex].target_patch.save(False)

    def clear(self):
        self.lines = None
        self.selectindex = None
        self.koreatext.clear()
        self.originaltext.clear()
        self.model.removeRows(0, self.model.rowCount())

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        self.selectindex = index.row()
        indexitem = self.model.index(index.row(), 1, index.parent())
        self.koreatext.setPlainText(indexitem.data())

        op = self.lines[self.selectindex].op
        if op == 'add':
            self.originaltext.setPlainText("""This line don't have origianl value because it "op" flag is "add" """)
        elif op == 'replace':
            try:
                org = self.lines[self.selectindex].original_value()
            except FileNotFoundError as f:
                org = f"""{f}\n\nplease check "assetfile\\original" directory or if not exist download original asset 
                with File menu """
            self.originaltext.setPlainText(org if isinstance(org, str) else json.dumps(org, ensure_ascii=False))
        else:
            print(f"Not consider this line op flag : {op}")


class explorer(QTreeView):
    def __init__(self, parent, path):
        super().__init__(parent)
        self.parent0 = parent
        self.model = QFileSystemModel()
        # set path
        self.model.setRootPath(path)
        self.asset = asset(self.model.rootPath(), load=False)
        # set model
        self.setModel(self.model)
        self.setRootIndex(self.model.index(self.model.rootPath()))
        self.setColumnWidth(0, int(parent.size().width() * 0.35))
        self.model.directoryLoaded.connect(self.load)
        self.clicked.connect(self.cil)
        self.key = None

        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        open_explorer = QtWidgets.QAction("Open in Explorer", self)
        open_explorer.triggered.connect(self.Eopen_explorer)
        self.addAction(open_explorer)

    def Eopen_explorer(self):
        os.startfile(self.model.filePath(self.currentIndex()))

    @pyqtSlot(QtCore.QModelIndex)
    def cil(self, index):
        viewer = self.parent0.tab.currentWidget().findChildren(patch_viewer)[0]
        viewer.clear()

        filepath = self.model.filePath(index)

        if self.model.type(index) == 'patch File':
            patch = patchfile(filepath[len(self.model.rootPath()) + 1:], self.asset)
            viewer.reload(patch)

    @pyqtSlot(str)
    def load(self, directory):
        parentIndex = self.model.index(directory)
        li = [parentIndex.child(row, 0) for row in range(self.model.rowCount(parentIndex)) if
              self.model.isDir(parentIndex.child(row, 0))] + \
             [parentIndex.child(row, 0) for row in range(self.model.rowCount(parentIndex)) if not
             self.model.isDir(parentIndex.child(row, 0))]

        if self.key == Qt.Key_Down:
            self.setCurrentIndex(li[0])
            if self.model.hasChildren(self.currentIndex()):
                self.expand(self.currentIndex())
            else:
                self.cil(self.currentIndex())
                self.key = None
        elif self.key == Qt.Key_Up:
            self.setCurrentIndex(li[-1])
            if self.model.hasChildren(self.currentIndex()):
                self.expand(self.currentIndex())
            else:
                self.cil(self.currentIndex())
                self.key = None

    def keyPressEvent(self, e):
        super(explorer, self).keyPressEvent(e)
        if e.key() == Qt.Key_Down:
            while True:
                if self.model.hasChildren(self.currentIndex()):
                    self.expand(self.currentIndex())
                    if self.model.rowCount(self.currentIndex()):
                        self.setCurrentIndex(self.currentIndex().child(0, 0))
                        continue
                    else:
                        self.key = Qt.Key_Down
                        break
                else:
                    self.cil(self.currentIndex())
                    break
        elif e.key() == Qt.Key_Up:
            b = True
            while True:
                if self.model.hasChildren(self.currentIndex()):
                    if self.isExpanded(self.currentIndex()) and b:
                        if self.currentIndex().parent() == self.rootIndex():
                            self.cil(self.currentIndex())
                            break
                        while True:
                            if self.currentIndex().row():
                                self.setCurrentIndex(
                                    self.currentIndex().parent().child(self.currentIndex().row() - 1, 0))
                                break
                            else:
                                self.setCurrentIndex(self.currentIndex().parent())
                                continue
                        b = False

                    self.expand(self.currentIndex())
                    row = self.model.rowCount(self.currentIndex())
                    if row:
                        self.setCurrentIndex(self.currentIndex().child(row - 1, 0))
                        continue
                    else:
                        self.key = Qt.Key_Up
                        break
                else:
                    self.cil(self.currentIndex())
                    break


class Form(QtWidgets.QMainWindow):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("Asset Editer")
        rect = app.desktop().screenGeometry()
        size = (int(rect.height() * 0.8), int(rect.width() * 0.8))
        self.setGeometry(int(rect.height() * 0.1), int(rect.height() * 0.1), size[1], size[0])

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        action0 = QtWidgets.QAction("Open Assset", self)
        action0.triggered.connect(self.action0f)
        action1 = QtWidgets.QAction("Original asset download", self)
        action1.triggered.connect(self.action1f)

        file_menu = menubar.addMenu("File")
        file_menu.addAction(action0)
        file_menu.addAction(action1)

        self.tab = QtWidgets.QTabWidget(self)
        astli = [i for i in glob('assetfile/*') if os.path.isdir(i) and i != 'assetfile\\original']
        try:
            self.addtap(astli.pop(astli.index('assetfile\\korean')))
        except ValueError:
            pass
        finally:
            for i in astli: self.addtap(i)
        self.setCentralWidget(self.tab)

    def addtap(self, path):
        widget = QWidget()
        new_explorer = explorer(self, os.path.abspath(path))
        viewer = patch_viewer(self)

        hbox = QHBoxLayout(widget)
        hbox.addWidget(new_explorer)
        hbox.addWidget(viewer)
        vbox = QVBoxLayout(widget)
        vbox.addWidget(viewer.koreatext)
        vbox.addWidget(viewer.originaltext)
        hbox.addLayout(vbox)

        self.tab.addTab(widget, path[path.rfind('\\') + 1:])

    def action0f(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Asset Folder", './assetfile')
        if not path == '':
            self.addtap(path)

    def action1f(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Starbound Folder")
        if not path == '':
            option = QtWidgets.QMessageBox.question(self, 'Download',
                                                    'Download the Original asset?\n다운로드 중에는 프로그램이 멈추거나 응답없음이 뜰수있습니다. 기다려주세요.',
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if option == QtWidgets.QMessageBox.Yes:
                result = asset.download_original_assets(path)
                if result:
                    QtWidgets.QMessageBox.information(self, 'Success', 'Unpacking success')
                else:
                    QtWidgets.QMessageBox.critical(self, 'Fail', 'Unpacking Fail')
            elif option == QtWidgets.QMessageBox.No:
                pass


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
