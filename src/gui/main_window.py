"""
Main window GUI implementation.
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QProgressBar, QFileDialog,
    QMessageBox, QLabel, QComboBox, QDialog, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from audio.processor import AudioProcessor
from audio.task import AudioTask
from .task_dialog import TaskDialog
from .task_item import TaskItem

class ProcessingThread(QThread):
    """Thread for processing audio tasks."""
    progress_updated = pyqtSignal(str, int)  # task_name, progress
    task_completed = pyqtSignal(str, bool, str)  # task_name, success, message
    
    def __init__(self, processor, task):
        super().__init__()
        self.processor = processor
        self.task = task
        self.is_running = False
        
    def run(self):
        """Run the processing task."""
        self.is_running = True
        try:
            # Process the audio file
            success = self.processor.process_audio(
                self.task,
                progress_callback=lambda p: self.progress_updated.emit(self.task.name, p)
            )
            
            if not self.is_running:
                self.task_completed.emit(self.task.name, False, "Task cancelled")
                return
                
            if success:
                self.task_completed.emit(self.task.name, True, "Processing completed successfully")
            else:
                self.task_completed.emit(self.task.name, False, "Processing failed")
                
        except Exception as e:
            self.task_completed.emit(self.task.name, False, f"Error: {str(e)}")
        finally:
            self.is_running = False
            
    def stop(self):
        """Stop the processing."""
        self.is_running = False

class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lecture Audio Cleaner")
        self.setMinimumSize(800, 600)
        
        # Initialize audio processor
        self.processor = AudioProcessor()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # Create toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)
        self.add_button = QPushButton("Add Task")
        self.start_all_button = QPushButton("Start All")
        self.stop_all_button = QPushButton("Stop All")
        
        toolbar.addWidget(self.add_button)
        toolbar.addWidget(self.start_all_button)
        toolbar.addWidget(self.stop_all_button)
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Create scroll area for task list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        # Create task list container
        self.task_container = QWidget()
        self.task_container.setObjectName("task_container")
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setSpacing(12)
        self.task_layout.setContentsMargins(5, 5, 5, 5)
        self.task_layout.addStretch()
        
        scroll.setWidget(self.task_container)
        layout.addWidget(scroll)
        
        # Connect signals
        self.add_button.clicked.connect(self.add_task)
        self.start_all_button.clicked.connect(self.start_all_tasks)
        self.stop_all_button.clicked.connect(self.stop_all_tasks)
        
        # Initialize task list and processing threads
        self.tasks = {}  # Dictionary of task_name -> (task, task_item)
        self.processing_threads = {}  # Dictionary of task_name -> processing_thread
        
    def add_task(self):
        """Add a new audio processing task."""
        # Show task configuration dialog
        dialog = TaskDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get configuration
            config = dialog.get_configuration()
            
            if config["input_path"]:
                # Create task with configuration
                task = AudioTask(
                    input_path=config["input_path"],
                    noise_reduction_level=config["noise_reduction_level"],
                    enable_speech_enhancement=config["enable_speech_enhancement"],
                    speech_enhancement_level=config["speech_enhancement_level"],
                    voice_clarity_boost=config["voice_clarity_boost"],
                    background_noise_level=config["background_noise_level"]
                )
                
                # Create task item
                task_item = TaskItem(task.name)
                task_item.start_clicked.connect(lambda: self.start_task(task.name))
                task_item.delete_clicked.connect(lambda: self.remove_task(task.name))
                
                # Add to layouts
                self.tasks[task.name] = (task, task_item)
                self.task_layout.insertWidget(self.task_layout.count() - 1, task_item)
                
    def remove_task(self, task_name: str):
        """Remove a specific task."""
        if task_name in self.tasks:
            # Stop processing if running
            self.stop_task(task_name)
            
            # Remove task
            task, task_item = self.tasks.pop(task_name)
            task_item.deleteLater()
            
    def start_task(self, task_name: str):
        """Start processing a specific task."""
        if task_name in self.tasks and task_name not in self.processing_threads:
            task, task_item = self.tasks[task_name]
            
            # Create and start processing thread
            thread = ProcessingThread(self.processor, task)
            thread.progress_updated.connect(self.update_task_progress)
            thread.task_completed.connect(self.on_task_completed)
            
            self.processing_threads[task_name] = thread
            thread.start()
            
            # Update UI
            task_item.set_running(True)
            
    def stop_task(self, task_name: str):
        """Stop processing a specific task."""
        if task_name in self.processing_threads:
            thread = self.processing_threads.pop(task_name)
            thread.stop()
            thread.wait()
            
            # Update UI
            _, task_item = self.tasks[task_name]
            task_item.set_running(False)
            
    def start_all_tasks(self):
        """Start processing all tasks."""
        if not self.tasks:
            QMessageBox.warning(self, "Warning", "No tasks to process!")
            return
            
        for task_name in self.tasks:
            if task_name not in self.processing_threads:
                self.start_task(task_name)
                
    def stop_all_tasks(self):
        """Stop processing all tasks."""
        for task_name in list(self.processing_threads.keys()):
            self.stop_task(task_name)
            
    def update_task_progress(self, task_name: str, progress: int):
        """Update progress for a specific task."""
        if task_name in self.tasks:
            _, task_item = self.tasks[task_name]
            task_item.set_progress(progress)
            
    def on_task_completed(self, task_name: str, success: bool, message: str):
        """Handle task completion."""
        if task_name in self.processing_threads:
            self.stop_task(task_name)
            
            # Update task item status
            if task_name in self.tasks:
                _, task_item = self.tasks[task_name]
                task_item.set_status(success, message)
                
            # Show notification for failed tasks
            if not success:
                QMessageBox.warning(self, "Task Failed", f"Task '{task_name}' failed: {message}")
            
    def closeEvent(self, event):
        """Handle window close event."""
        self.stop_all_tasks()
        super().closeEvent(event) 