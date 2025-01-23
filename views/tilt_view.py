from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform, QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

class TiltView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSceneRect(0, 0, 300, 300)

        pixmap = QPixmap("resources/assets/a.png")
        if pixmap.isNull():
            raise FileNotFoundError("Image not found at 'resources/assets/a.png'")
        scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio)

        self.image_item = QGraphicsPixmapItem(scaled_pixmap)
        self.image_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(self.image_item)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        widget_center = self.rect().center()
        delta = event.pos() - widget_center
        angle_x = delta.y() / self.height() * 30
        angle_y = delta.x() / self.width() * 30
        distance_from_center = (delta.x() ** 2 + delta.y() ** 2) ** 0.5
        scale_factor = 1 + (distance_from_center / self.width()) * 0.3

        transform = QTransform()
        transform.rotate(angle_x, Qt.Axis.XAxis)
        transform.rotate(angle_y, Qt.Axis.YAxis)
        transform.scale(scale_factor, scale_factor)

        self.image_item.setTransform(transform)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.image_item.setTransform(QTransform())
        super().leaveEvent(event)
