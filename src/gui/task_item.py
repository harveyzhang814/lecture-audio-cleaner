"""
Task item widget implementation.
"""
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QVBoxLayout, QStyle
)
from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath

class TaskItem(QWidget):
    """Widget for displaying a single task in the task list."""
    
    # Custom signals
    start_clicked = pyqtSignal()
    delete_clicked = pyqtSignal()
    
    def __init__(self, task_name: str, parent=None):
        super().__init__(parent)
        self.is_running = False
        
        # Create main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Create top row with filename and buttons
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)
        
        # Filename label
        self.filename_label = QLabel(task_name)
        self.filename_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
            }
        """)
        top_layout.addWidget(self.filename_label)
        
        # Status label
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 2px 6px;
                border-radius: 4px;
            }
            QLabel[status="success"] {
                background: #e6f4ea;
                color: #1e7e34;
            }
            QLabel[status="error"] {
                background: #fce8e8;
                color: #dc3545;
            }
        """)
        self.status_label.hide()
        top_layout.addWidget(self.status_label)
        
        # Add stretch to push buttons to the right
        top_layout.addStretch()
        
        # Start button
        self.start_button = QPushButton()
        self.start_button.setFixedSize(24, 24)
        self.start_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        self.start_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.start_button.clicked.connect(self._on_start_clicked)
        top_layout.addWidget(self.start_button)
        
        # Delete button
        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(24, 24)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 0.1);
            }
        """)
        self.delete_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_button.clicked.connect(self.delete_clicked.emit)
        top_layout.addWidget(self.delete_button)
        
        layout.addLayout(top_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(6)
        layout.addWidget(self.progress_bar)
        
        # Set the layout
        self.setLayout(layout)
        
        # Set widget style
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            TaskItem {
                background: palette(base);
                border: 1px solid palette(mid);
                border-radius: 6px;
            }
        """)
        
    def paintEvent(self, event):
        """Custom paint event to draw shadow and border."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRectF(self.rect())
        
        # Draw shadow
        shadow_path = QPainterPath()
        shadow_path.addRoundedRect(rect.adjusted(2, 2, -2, -2), 6, 6)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 15))
        painter.drawPath(shadow_path.translated(0, 1))
        
        # Draw border
        border_path = QPainterPath()
        border_path.addRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 6, 6)
        painter.setPen(QPen(self.palette().mid(), 1))
        painter.setBrush(self.palette().base())
        painter.drawPath(border_path)
        
    def set_progress(self, value: int):
        """Set the progress bar value."""
        self.progress_bar.setValue(value)
        
    def set_filename(self, name: str):
        """Set the filename label."""
        self.filename_label.setText(name)
        
    def set_running(self, running: bool):
        """Update the UI based on task running state."""
        self.is_running = running
        self.start_button.setIcon(
            self.style().standardIcon(
                QStyle.SP_MediaPause if running else QStyle.SP_MediaPlay
            )
        )
        if running:
            self.status_label.hide()
            self.progress_bar.setValue(0)
        
    def set_status(self, success: bool, message: str):
        """Update the status display."""
        self.status_label.setText(message)
        self.status_label.setProperty("status", "success" if success else "error")
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.show()
        
    def _on_start_clicked(self):
        """Handle start button click."""
        self.start_clicked.emit() 