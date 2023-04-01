# -*- coding: utf-8 -*-

""" This is a Python script that creates a graphical user interface (GUI) using the PyQt5 library. The GUI allows the user to browse for an image file and display the selected image. Here is a brief overview of what the code does:

It imports necessary modules such as PyQt5 and os. It defines a main window class called MainWindow that inherits from QtWidgets.QMainWindow.
In the constructor of the MainWindow class, it sets the window title and size, creates a central widget, creates a "Browse Image" button, a QLabel 
for displaying the selected image, a QLabel for "Img-Display-GUI" text, a QLabel for displaying the selected file name, a QTextEdit for displaying 
the selected file name, and a status bar.
It defines a function called load_image which opens a file dialog to select an image file, displays the selected image in the QLabel, displays the 
selected file name in the QTextEdit, and stores the selected file name in a variable called self.file.
It runs the application by creating an instance of QApplication, an instance of MainWindow, and calling the show method to display the main window. Finally, it calls the exec_ method of the application instance to start the event loop. """

# Form implementation generated from reading ui file 'sample.ui'
# Created by: PyQt5 UI code generator 5.15.4

# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# Importing necessary modules
from PyQt5 import QtCore, QtGui, QtWidgets
import os

# Defining main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting window title and size
        self.setWindowTitle("Python Image Displayer")
        self.resize(800, 600)

        # Creating central widget
        centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralwidget)

        # Creating "Browse Image" button
        self.BrowseImage = QtWidgets.QPushButton("Browse Image", centralwidget)
        self.BrowseImage.setGeometry(QtCore.QRect(160, 390, 151, 51))
        self.BrowseImage.clicked.connect(self.load_image)

        # Creating label for displaying selected image
        self.image_lbl = QtWidgets.QLabel(centralwidget)
        self.image_lbl.setGeometry(QtCore.QRect(200, 80, 361, 261))
        self.image_lbl.setFrameShape(QtWidgets.QFrame.Box)
        self.image_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # Creating label for "Python Bootcamp" text
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(28)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_2 = QtWidgets.QLabel("Img-Display-GUI", centralwidget)
        self.label_2.setGeometry(QtCore.QRect(210, 0, 351, 61))
        self.label_2.setFont(font)

        # Creating label for displaying file name
        self.label = QtWidgets.QLabel("File Name", centralwidget)
        self.label.setGeometry(QtCore.QRect(430, 370, 111, 16))

        # Creating text edit for displaying selected file name
        self.text_edit = QtWidgets.QTextEdit(centralwidget)
        self.text_edit.setGeometry(QtCore.QRect(400, 390, 211, 51))

        # Creating status bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    # Defining function to load image
    def load_image(self):
        # Opening file dialog to select image
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp);;All Files (*)")
        if file_name:
            # Printing selected file name and storing it in variable
            print(file_name)
            self.file = file_name

            # Creating pixmap from selected image file and scaling it to fit label
            pixmap = QtGui.QPixmap(file_name)
            pixmap = pixmap.scaled(self.image_lbl.width(), self.image_lbl.height(), QtCore.Qt.KeepAspectRatio)
            self.image_lbl.setPixmap(pixmap)

            # Displaying only the file name in the text edit
            head, tail = os.path.split(file_name)
            print(tail)
            self.text_edit.setText(tail)

# Running the application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())