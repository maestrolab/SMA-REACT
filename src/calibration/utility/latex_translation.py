from matplotlib.figure import Figure
from matplotlib import rcParams as rc
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import QSize
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import io


def textToLatex(text, width, height, widget):
    #rc["font.serif"] = "Palatino Linotype"
    #rc["font.family"] = "serif"
    rc["text.usetex"] = False  # Don't use external LaTeX

    dpi = 125
    fig = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    canvas = FigureCanvas(fig)
    ax = fig.gca()

    # Place text in the center like original
    ax.text(0.0, 0.0, text,
            va='center', ha='center',
            fontsize=10)

    ax.axis('off')
    ax.margins(0)
    ax.patch.set_facecolor('none')
    fig.patch.set_facecolor('none')

    # Render to memory (no file I/O)
    buf = io.BytesIO()
    canvas.print_png(buf, facecolor=fig.get_facecolor())
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())

    # Set up QLabel
    label = QLabel(widget)
    label.setPixmap(pixmap)
    label.setMinimumSize(QSize(width, height))

    return label
