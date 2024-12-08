import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image, ImageFilter


# Initialize the application
app = QApplication([])


# Main window setup
main_win = QWidget()
main_win.resize(1400, 850)
main_win.setWindowTitle('Easy Editor')
main_win.setWindowIcon(QIcon('icon.png')) # only 64x64



# Widgets
imageLabel = QLabel('Image')
imageLabel.setFixedSize(1300, 800)

fileList = QListWidget()
btubaut = QPushButton('abaut')
buttonSave = QPushButton('Save')
buttonClear = QPushButton('Clear')
buttonLeft = QPushButton('Left')
buttonRight = QPushButton('Right')
buttonBlur = QPushButton('Blur')
buttonMirror = QPushButton('Mirror')
buttonSharpness = QPushButton('Sharpness')
buttonBW = QPushButton('B/W')
buttonFile = QPushButton('Folder')

# Layouts
main_layout = QHBoxLayout()      
left_layout = QVBoxLayout()    
left_layout_BU = QHBoxLayout()
right_layout = QVBoxLayout()     
buttons_layout = QHBoxLayout()   
# Add widgets to layouts
left_layout_BU.addWidget(buttonFile)
left_layout_BU.addWidget(buttonClear)
left_layout.addLayout(left_layout_BU)
left_layout.addWidget(fileList)
left_layout.addWidget(btubaut)
right_layout.addWidget(imageLabel)
buttons_layout.addWidget(buttonLeft)
buttons_layout.addWidget(buttonRight)
buttons_layout.addWidget(buttonMirror)
buttons_layout.addWidget(buttonSharpness)
buttons_layout.addWidget(buttonBW)
buttons_layout.addWidget(buttonBlur)
buttons_layout.addWidget(buttonSave)
right_layout.addLayout(buttons_layout)

# Add the layouts to the main layout
main_layout.addLayout(left_layout)  
main_layout.addLayout(right_layout)  

# Set the main layout
main_win.setLayout(main_layout)
  
#factsions
def ClearTheFileList():
   fileList.clear()

def ShooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def Filter(fileList, extensions):
    result = []
    for filename in fileList:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
        

def showFilenameList():
    global workdir
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    ShooseWorkDir()  # Let the user choose the working directory
    if workdir:  # Check if workdir is not None or empty
        filenames = Filter(os.listdir(workdir), extensions)
        fileList.clear()
        fileList.addItems(filenames)
    else:
        print("No directory selected or directory is invalid.")



def create_tray_icon():
    # Create the system tray icon
    tray_icon = QSystemTrayIcon(QIcon('icon.png'), parent=main_win)

    # Create a context menu for the tray icon
    tray_menu = QMenu()

    # Add actions to the menu
    show_action = QAction("Show", main_win)
    quit_action = QAction("Quit", main_win)

    # Connect the actions to the appropriate functions
    show_action.triggered.connect(main_win.show)
    quit_action.triggered.connect(QApplication.instance().quit)

    # Add the actions to the tray menu
    tray_menu.addAction(show_action)
    tray_menu.addAction(quit_action)

    # Set the tray icon's context menu
    tray_icon.setContextMenu(tray_menu)

    # Show the tray icon
    tray_icon.show()

    return tray_icon


# Declare the variable to hold the reference to the second window
second_window = None  # Initialize the variable here

# Class for the second window
class SecondWindow(QWidget):
    """A class for the second window."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About Easy Editor')
        self.setGeometry(300, 300, 300, 200)  # x, y, width, height
        self.setWindowIcon(QIcon('icon.png')) # only 64x64
        layout = QVBoxLayout()
        
        # Adding labels to display information
        self.creator_label = QLabel('Creator: 𝕭𝖑𝖆𝖟𝖊𝖇𝖔𝖘𝖘')
        self.version_label = QLabel('Version: 1.0')
        self.type_label = QLabel('Type: Image Editing Software')
        
        # Add labels to the layout
        layout.addWidget(self.creator_label)
        layout.addWidget(self.version_label)
        layout.addWidget(self.type_label)
        
        self.setLayout(layout)

# Define the function to open the second window
def open_second_window():
    global second_window  # Reference the global variable
    if second_window is None:  # Create only if it doesn't already exist
        second_window = SecondWindow()  # Create an instance of the second window
    second_window.show()  # Show the second window

# Connecting the button to the function
btubaut.clicked.connect(open_second_window)


#Class
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None

    def loadImage(self, dir, filename):
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)


    def showImage(self, path):
        imageLabel.hide()
        pixmapimage = QPixmap(path)
        w, h = imageLabel.width(), imageLabel.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        imageLabel.setPixmap(pixmapimage)
        imageLabel.show()

    def SaveImage(self):
        path = os.path.join(workdir, 'Modified')
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def SaveImage2(self):
        path = QFileDialog.getExistingDirectory()  
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    
        
    def do_BW(self):
        self.image = self.image.convert("L")
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)



    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)

    def do_SHARPEN(self):
        self.image = self.image.convert("RGB")
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)

    def do_blur(self):
        self.image = self.image.convert("RGB")
        self.image = self.image.filter(ImageFilter.BLUR)
        self.SaveImage()
        image_path = os.path.join(workdir, "Modified", self.filename)
        self.showImage(image_path)


workimage = ImageProcessor()

def showChosenImage():
    if fileList.currentRow() >=0:
        filename = fileList.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)

fileList.currentRowChanged.connect(showChosenImage)
buttonFile.clicked.connect(showFilenameList)
buttonClear.clicked.connect(ClearTheFileList)
tray_icon = create_tray_icon()
buttonBW.clicked.connect(workimage.do_BW)
buttonLeft.clicked.connect(workimage.do_left)
buttonRight.clicked.connect(workimage.do_right)
buttonMirror.clicked.connect(workimage.do_mirror)
buttonSharpness.clicked.connect(workimage.do_SHARPEN)
buttonSave.clicked.connect(workimage.SaveImage2)
buttonBlur.clicked.connect(workimage.do_blur)

# Show the main window
main_win.show()
sys.exit(app.exec_())
