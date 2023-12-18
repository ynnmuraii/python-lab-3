import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from script_1 import create_annotation
from script_2 import create_dataset2, create_annotation2
from script_3 import create_dataset3, create_annotation3
from script_5 import Iterator


class Window(QMainWindow):
    def __init__(self) -> None:

        super().__init__()

        self.initUI()
        self.initIterators()
        self.createActions()
        self.createMenuBar()
        self.createToolBar()

    def initUI(self) -> None:

        self.center()
        self.setWindowTitle('Leopard and Tiger')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        leop_btn = QPushButton('Next Leopard', self)
        tig_btn = QPushButton('Next Tiger', self)

        pixmap = QPixmap('img/main_photo.jpg')
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        hbox.addWidget(leop_btn)
        hbox.addWidget(tig_btn)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)

        leop_btn.clicked.connect(self.nextLeop)
        tig_btn.clicked.connect(self.nextTig)

        self.folderpath = ' '

        self.showMaximized()

    def initIterators(self) -> None:

        self.leopards = Iterator('leopard', 'dataset')
        self.tigers = Iterator('tiger', 'dataset')

    def nextLeop(self) -> None:

        lbl_size = self.lbl.size()
        next_image = next(self.leopards)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextLeop()

    def nextTig(self) -> None:

        lbl_size = self.lbl.size()
        next_image = next(self.tigers)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextTig()

    def center(self) -> None:

        widget_rect = self.frameGeometry()
        pc_rect = QDesktopWidget().availableGeometry().center()
        widget_rect.moveCenter(pc_rect)
        self.move(widget_rect.center())

    def createMenuBar(self) -> None:

        menuBar = self.menuBar()

        self.fileMenu = menuBar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)

        self.annotMenu = menuBar.addMenu('&Annotation')
        self.annotMenu.addAction(self.createAnnotAction)

        self.dataMenu = menuBar.addMenu('&Dataset')
        self.dataMenu.addAction(self.createData2Action)

    def createToolBar(self) -> None:

        fileToolBar = self.addToolBar('File')
        fileToolBar.addAction(self.exitAction)

        annotToolBar = self.addToolBar('Annotation')
        annotToolBar.addAction(self.createAnnotAction)

    def createActions(self) -> None:

        self.exitAction = QAction(QIcon('img/log_out.png'), '&Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction(QIcon('img/change.png'), '&Change dataset')
        self.changeAction.triggered.connect(self.changeDataset)

        self.createAnnotAction = QAction(
            QIcon('img/csv.png'), '&Create annotation for current dataset')
        self.createAnnotAction.triggered.connect(self.createAnnotation)

        self.createData2Action = QAction(
            QIcon('img/dataset.png'), '&Create dataset2')
        self.createData2Action.triggered.connect(self.createDataset2)

        self.createData3Action = QAction(
            QIcon('img/dataset.png'), '&Create dataset3')
        self.createData3Action.triggered.connect(self.createDataset3)

    def createAnnotation(self) -> None:

        if 'dataset2' in str(self.folderpath):
            create_annotation2()
        elif 'dataset3' in str(self.folderpath):
            create_annotation3()
        elif 'dataset' in str(self.folderpath):
            create_annotation()

    def createDataset2(self) -> None:

        create_dataset2()
        self.dataMenu.addAction(self.createData3Action)

    def createDataset3(self) -> None:

        create_dataset3()

    def changeDataset(self) -> None:

        reply = QMessageBox.question(self, 'Warning', f'Are you sure you want to change current dataset?\nCurrent dataset: {str(self.folderpath)}',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.folderpath = self.folderpath = QFileDialog.getExistingDirectory(
                self, 'Select Folder')
        else:
            pass

    def closeEvent(self, event: QEvent) -> None:

        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main() -> None:
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()