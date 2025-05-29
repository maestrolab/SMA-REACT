from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from matplotlib import rc
import io


def textToLatex(text, width, height, widget, x_offset, y_offset):
    dpi = 125
    # Configure fonts without LaTeX
    #rc["font.serif"] = "Palatino Linotype"
    #rc["font.family"] = "serif"
    rc["text.usetex"] = False  # Important: no LaTeX required

    # Create figure and axis
    fig = Figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.tight_layout(pad=0.0)
    canvas = FigureCanvas(fig)
    ax = fig.gca()

    # Render the text at the given offset
    ax.text(x_offset, y_offset, r'{}'.format(text), fontsize=10)

    # Hide axis and adjust layout
    ax.axis('off')
    ax.margins(0)
    fig.patch.set_facecolor("#f0f0f0")

    # Render figure to memory buffer
    buf = io.BytesIO()
    canvas.print_png(buf)
    pixmap = QPixmap()
    pixmap.loadFromData(buf.getvalue())

    # Create QLabel with the pixmap
    label = QLabel(widget)
    label.setPixmap(pixmap)

    # Apply size policies and alignment
    sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    label.setSizePolicy(sizePolicy)
    label.setMaximumSize(QSize(width, height))
    label.setMinimumSize(QSize(width, height))
    label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    return label


