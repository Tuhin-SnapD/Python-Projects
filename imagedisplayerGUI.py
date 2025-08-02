"""
Enhanced Image Display GUI

A modern PyQt5-based image viewer with advanced features including:
- Multiple image format support
- Image filters and effects
- Zoom and pan functionality
- Image information display
- Better error handling and user experience
"""

import sys
import os
from typing import Optional, Tuple
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QFileDialog, QTextEdit, 
                            QStatusBar, QSlider, QComboBox, QGroupBox, 
                            QMessageBox, QScrollArea, QFrame)


class ImageProcessor:
    """Handles image processing operations."""
    
    @staticmethod
    def apply_filter(image: QImage, filter_type: str) -> QImage:
        """Apply various filters to the image."""
        if filter_type == "None":
            return image
        
        processed = QImage(image)
        painter = QPainter(processed)
        
        if filter_type == "Grayscale":
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixel(x, y)
                    gray = int(0.299 * QColor(pixel).red() + 
                              0.587 * QColor(pixel).green() + 
                              0.114 * QColor(pixel).blue())
                    processed.setPixel(x, y, QColor(gray, gray, gray).rgb())
        
        elif filter_type == "Sepia":
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    r, g, b = color.red(), color.green(), color.blue()
                    
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    
                    tr = min(255, max(0, tr))
                    tg = min(255, max(0, tg))
                    tb = min(255, max(0, tb))
                    
                    processed.setPixel(x, y, QColor(tr, tg, tb).rgb())
        
        elif filter_type == "Invert":
            for y in range(image.height()):
                for x in range(image.width()):
                    pixel = image.pixel(x, y)
                    color = QColor(pixel)
                    processed.setPixel(x, y, QColor(255 - color.red(), 
                                                   255 - color.green(), 
                                                   255 - color.blue()).rgb())
        
        painter.end()
        return processed


class ModernImageDisplayGUI(QMainWindow):
    """Enhanced image display application with modern UI."""
    
    def __init__(self):
        super().__init__()
        self.original_pixmap: Optional[QPixmap] = None
        self.current_pixmap: Optional[QPixmap] = None
        self.zoom_factor = 1.0
        self.file_path = ""
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("🎨 Modern Image Display GUI")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ffffff;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #5c6bc0;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left panel for controls
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Create right panel for image display
        right_panel = self.create_image_panel()
        main_layout.addWidget(right_panel, 4)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - No image loaded")
        
    def create_control_panel(self) -> QWidget:
        """Create the control panel with buttons and options."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Title
        title_label = QLabel("🎨 Image Display GUI")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #333333;
                padding: 10px;
                background-color: #e8f5e8;
                border-radius: 5px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        # File operations group
        file_group = QGroupBox("📁 File Operations")
        file_layout = QVBoxLayout(file_group)
        
        self.browse_btn = QPushButton("📂 Browse Image")
        self.browse_btn.clicked.connect(self.load_image)
        file_layout.addWidget(self.browse_btn)
        
        self.clear_btn = QPushButton("🗑️ Clear Image")
        self.clear_btn.clicked.connect(self.clear_image)
        self.clear_btn.setEnabled(False)
        file_layout.addWidget(self.clear_btn)
        
        layout.addWidget(file_group)
        
        # Image information group
        self.info_group = QGroupBox("ℹ️ Image Information")
        self.info_layout = QVBoxLayout(self.info_group)
        
        self.file_name_label = QLabel("File: None")
        self.file_name_label.setWordWrap(True)
        self.info_layout.addWidget(self.file_name_label)
        
        self.image_info_label = QLabel("Size: N/A")
        self.info_layout.addWidget(self.image_info_label)
        
        self.file_size_label = QLabel("File size: N/A")
        self.info_layout.addWidget(self.file_size_label)
        
        layout.addWidget(self.info_group)
        
        # Image filters group
        filter_group = QGroupBox("🎭 Image Filters")
        filter_layout = QVBoxLayout(filter_group)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["None", "Grayscale", "Sepia", "Invert"])
        self.filter_combo.currentTextChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_combo)
        
        layout.addWidget(filter_group)
        
        # Zoom controls group
        zoom_group = QGroupBox("🔍 Zoom Controls")
        zoom_layout = QVBoxLayout(zoom_group)
        
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        self.zoom_slider.valueChanged.connect(self.zoom_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("Zoom: 100%")
        self.zoom_label.setAlignment(Qt.AlignCenter)
        zoom_layout.addWidget(self.zoom_label)
        
        # Zoom buttons
        zoom_btn_layout = QHBoxLayout()
        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_btn_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_btn_layout.addWidget(self.zoom_out_btn)
        
        self.fit_btn = QPushButton("📐 Fit")
        self.fit_btn.clicked.connect(self.fit_to_window)
        zoom_btn_layout.addWidget(self.fit_btn)
        
        zoom_layout.addLayout(zoom_btn_layout)
        layout.addWidget(zoom_group)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return panel
    
    def create_image_panel(self) -> QWidget:
        """Create the image display panel."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Create scroll area for image
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameStyle(QFrame.Box)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #ffffff;
                border: 2px solid #cccccc;
                border-radius: 5px;
            }
        """)
        
        # Create image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f8f8;
                border: 1px solid #dddddd;
                border-radius: 3px;
            }
        """)
        self.image_label.setText("No image loaded\nClick 'Browse Image' to select an image")
        
        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)
        
        return panel
    
    def load_image(self):
        """Load an image file."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Image",
                "",
                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
            )
            
            if file_path:
                self.load_image_from_path(file_path)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    def load_image_from_path(self, file_path: str):
        """Load image from a specific file path."""
        try:
            self.file_path = file_path
            self.original_pixmap = QPixmap(file_path)
            
            if self.original_pixmap.isNull():
                raise ValueError("Invalid image file")
            
            self.current_pixmap = self.original_pixmap.copy()
            self.update_image_display()
            self.update_image_info()
            
            # Enable controls
            self.clear_btn.setEnabled(True)
            self.zoom_slider.setEnabled(True)
            self.zoom_in_btn.setEnabled(True)
            self.zoom_out_btn.setEnabled(True)
            self.fit_btn.setEnabled(True)
            self.filter_combo.setEnabled(True)
            
            self.status_bar.showMessage(f"Image loaded: {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
            self.status_bar.showMessage("Error loading image")
    
    def clear_image(self):
        """Clear the currently loaded image."""
        self.original_pixmap = None
        self.current_pixmap = None
        self.file_path = ""
        self.zoom_factor = 1.0
        
        self.image_label.clear()
        self.image_label.setText("No image loaded\nClick 'Browse Image' to select an image")
        
        # Disable controls
        self.clear_btn.setEnabled(False)
        self.zoom_slider.setEnabled(False)
        self.zoom_in_btn.setEnabled(False)
        self.zoom_out_btn.setEnabled(False)
        self.fit_btn.setEnabled(False)
        self.filter_combo.setEnabled(False)
        
        # Reset info
        self.file_name_label.setText("File: None")
        self.image_info_label.setText("Size: N/A")
        self.file_size_label.setText("File size: N/A")
        
        self.status_bar.showMessage("Ready - No image loaded")
    
    def update_image_display(self):
        """Update the image display with current settings."""
        if self.current_pixmap:
            # Apply zoom
            new_width = int(self.current_pixmap.width() * self.zoom_factor)
            new_height = int(self.current_pixmap.height() * self.zoom_factor)
            scaled_pixmap = self.current_pixmap.scaled(
                new_width,
                new_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
    
    def update_image_info(self):
        """Update the image information display."""
        if self.original_pixmap and self.file_path:
            # File name
            file_name = os.path.basename(self.file_path)
            self.file_name_label.setText(f"File: {file_name}")
            
            # Image size
            width = self.original_pixmap.width()
            height = self.original_pixmap.height()
            self.image_info_label.setText(f"Size: {width} × {height} pixels")
            
            # File size
            try:
                file_size = os.path.getsize(self.file_path)
                if file_size < 1024:
                    size_str = f"{file_size} B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size / 1024:.1f} KB"
                else:
                    size_str = f"{file_size / (1024 * 1024):.1f} MB"
                self.file_size_label.setText(f"File size: {size_str}")
            except OSError:
                self.file_size_label.setText("File size: Unknown")
    
    def apply_filter(self, filter_type: str):
        """Apply a filter to the image."""
        if self.original_pixmap:
            try:
                # Convert pixmap to image for processing
                image = self.original_pixmap.toImage()
                
                # Apply filter
                processed_image = ImageProcessor.apply_filter(image, filter_type)
                
                # Convert back to pixmap
                self.current_pixmap = QPixmap.fromImage(processed_image)
                self.update_image_display()
                
                self.status_bar.showMessage(f"Applied filter: {filter_type}")
                
            except Exception as e:
                QMessageBox.warning(self, "Filter Error", f"Failed to apply filter: {str(e)}")
    
    def zoom_changed(self, value: int):
        """Handle zoom slider changes."""
        self.zoom_factor = value / 100.0
        self.zoom_label.setText(f"Zoom: {value}%")
        self.update_image_display()
    
    def zoom_in(self):
        """Zoom in on the image."""
        current_value = self.zoom_slider.value()
        new_value = min(300, current_value + 25)
        self.zoom_slider.setValue(new_value)
    
    def zoom_out(self):
        """Zoom out from the image."""
        current_value = self.zoom_slider.value()
        new_value = max(10, current_value - 25)
        self.zoom_slider.setValue(new_value)
    
    def fit_to_window(self):
        """Fit the image to the current window size."""
        if self.current_pixmap:
            # Calculate the zoom factor to fit the image in the scroll area
            scroll_size = self.scroll_area.size()
            image_size = self.current_pixmap.size()
            
            scale_x = scroll_size.width() / image_size.width()
            scale_y = scroll_size.height() / image_size.height()
            scale = min(scale_x, scale_y, 1.0)  # Don't scale up beyond 100%
            
            zoom_percentage = int(scale * 100)
            self.zoom_slider.setValue(zoom_percentage)
    
    def resizeEvent(self, event):
        """Handle window resize events."""
        super().resizeEvent(event)
        # Optionally auto-fit image when window is resized
        # self.fit_to_window()


def main():
    """Main function to start the application."""
    try:
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')  # Use Fusion style for modern look
        
        # Set application properties
        app.setApplicationName("Modern Image Display GUI")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Python Projects")
        
        # Create and show the main window
        window = ModernImageDisplayGUI()
        window.show()
        
        # Start the event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()