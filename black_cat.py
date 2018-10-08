from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QMovie
from pics import pics_rc
import json
import sys


class BlackCat(QLabel):

    def __init__(self):
        super(BlackCat, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.FramelessWindowHint|Qt.Tool)
        self.setMouseTracking(True)
        self.data = json.loads(open('data.dat', 'rb').read().decode())
        self.setup()

    def setup(self):
        normal = self.data.get('normal', '')
        move = self.data.get('move', '')
        hover = self.data.get('hover', '')
        press = self.data.get('press', '')
        movie = QMovie(normal)
        image = QPixmap(hover)
        self.resize(image.size())
        self.setMinimumSize(image.size())
        self.setMaximumSize(image.size())

        self.movie = {
            'normal': movie,
            'move': QPixmap(move),
            'hover': image,
            'press': QPixmap(press)
        }

        self._currentImage = movie
        self.change_image('normal')
        self.update()

    def change_image(self, name):
        self._currentImage = self.movie.get(name)
        if name == 'normal':
            self.setMovie(self._currentImage)
            self.movie.get('normal').start()
            print('movie start')
            print(self.size())
            print(self.pos())
        else:
            self.movie.get('normal').stop()
            print('movie stop')

    def paintEvent(self, event):
        if isinstance(self._currentImage, QMovie):
            return super(BlackCat, self).paintEvent(event)
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._currentImage)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_image('press')
            self.update()
            self.mpos = event.globalPos() - self.pos()
        super(BlackCat, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.change_image('normal')
            self.update()
        super(BlackCat, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos()-self.mpos)
            self.change_image('move')
            self.update()
        super(BlackCat, self).mouseMoveEvent(event)

    def enterEvent(self, event):
        self.change_image('hover')
        print("enter")
        self.update()
        super(BlackCat, self).enterEvent(event)
    
    def leaveEvent(self, event):
        self.change_image('normal')
        self.update()
        print("leave")
        super(BlackCat, self).leaveEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    black_cat = BlackCat()
    black_cat.show()
    sys.exit(app.exec_())