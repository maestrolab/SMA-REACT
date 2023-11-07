from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import QSize
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap


def textToLatex(text, width, height, widget, x_offset, y_offset):
    dpi = 125
    fig = Figure(figsize=(width/dpi, height/dpi), dpi=dpi)
    # fig = Figure()
    fig.tight_layout(pad=0.0)
    canvas = FigureCanvas(fig)
    ax = fig.gca()

    ax.text(x_offset, y_offset, r'{}'.format(text))
    ax.axis('off')
    ax.margins(0)
    fig.patch.set_facecolor("#f0f0f0")

    canvas.draw()

    canvas.print_figure("latex.png")

    pixmap = QPixmap('latex.png')
    # size= pixmap.size()
    # pixmap = pixmap.scaled(size * 2)
    label = QLabel(widget)
    label.setPixmap(pixmap)
    # label.setScaledContents(True)

    sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)

    label.setSizePolicy(sizePolicy)
    label.setMaximumSize(QSize(width, height))
    label.setMinimumSize(QSize(width, height))
    label.setAlignment(QtCore.Qt.AlignRight)
    label.setAlignment(QtCore.Qt.AlignVCenter)


    return label



