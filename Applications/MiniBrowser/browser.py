# -*- coding: utf-8 -*-
"""
Applications/MiniBrowser/browser.py
Mini Browser
Web browser made by Daniel M using Python 3 for the MiniOS project: https://github.com/DanielMiao1/MiniOS
"""

import os
import sys

# Local file imports
sys.path.insert(1, "Applications/.ApplicationSupport")
import get_properties

# PyQt imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class ToolBar(QToolBar): # PyQt5 widget overrides
	def __init__(self, parent=None):
		super().__init__(parent)
		layout = self.findChild(QLayout)
		if layout is not None: layout.setExpanded(True)
		QTimer.singleShot(0, self.onTimeout)

	@pyqtSlot()
	def onTimeout(self):
		button = self.findChild(QToolButton, "qt_toolbar_ext_button")
		if button is not None: button.setFixedSize(0, 0)

	def event(self, e):
		if e.type() == QEvent.Leave: return True
		return super(ToolBar, self).event(e)

  
# PyQt5 widget overrides
class PushButton(QPushButton):
	"""Add QPushButton Animation"""
	def __init__(self) -> None:
		super().__init__()
		self._animation = QVariantAnimation()
		self._animation.setStartValue(QColor("white"))
		self._animation.setEndValue(QColor("black"))
		self._animation.setDuration(200)
		self._animation.valueChanged.connect(self.valueChanged)
		self._animation = QVariantAnimation(startValue=QColor("white"), endValue=QColor("#18082C"), valueChanged=self.valueChanged, duration=200)
		self.updateStylesheet(QColor("#18082C"), QColor("white"))
		self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

	def valueChanged(self, color: QColor) -> None:
		"""If value changed"""
		self.updateStylesheet(color, QColor("white") if self._animation.direction() == QAbstractAnimation.Forward else QColor("#18082C"))

	def updateStylesheet(self, background: QColor, foreground: QColor) -> None:
		"""Update style sheet"""
		self.setStyleSheet(f"QPushButton {{background-color: {background.name()}; color: {foreground.name()}; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}}")

	def enterEvent(self, event: QEvent) -> None:
		"""Display backward color animation on mouse hover"""
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)

	def leaveEvent(self, event: QEvent) -> None:
		"""Display forward color animation on mouse leave"""
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)


class LineEdit(QLineEdit):
	""""Add select all when pressed feature to QLineEdit"""
	def __init__(self, parent=None) -> None:
		super(LineEdit, self).__init__(parent)

	def mousePressEvent(self, _) -> None:
		"""Select all when pressed unless text is already selected"""
		self.setCursorPosition(len(self.text())) if self.hasSelectedText() else self.selectAll()


class ScrollArea(QScrollArea):
	"""Set word wrap of QScrollArea to True"""
	def __init__(self) -> None:
		QScrollArea.__init__(self)
		self.setWidgetResizable(True)
		text = QWidget(self)
		self.setWidget(text)
		template = QVBoxLayout(text)
		self.label = QLabel(text)
		self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
		self.label.setWordWrap(True)
		template.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignHCenter)

	def setText(self, text: str) -> None:
		"""Set text of button"""
		self.label.setText(text)


class WebEnginePage(QWebEnginePage):
	"""Load target='_blank' anchors in the current tab"""
	def createWindow(self, _):
		page = WebEnginePage(self)
		page.urlChanged.connect(self.onURLChanged)
		return page
	
	@pyqtSlot(QUrl)
	def onURLChanged(self, url: QUrl) -> None:
		page = self.sender()
		self.setUrl(url)
		page.deleteLater()


class TabWidget(QTabWidget):
	def __init__(self) -> None:
		super(TabWidget, self).__init__()
		self.setAcceptDrops(True)
	
	def dropEvent(self, event) -> None:
		print(event)


# Dialogs


class AboutDialog(QDialog):
	"""About Mini Browser dialog"""
	def __init__(self, parent=None) -> None:
		super(AboutDialog, self).__init__(parent=parent)
		template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("Mini Browser") # Add title
		title_font = title.font() # Add new font
		title_font.setPointSize(50) # Set point size for font
		title_font.setBold(True) # Make font bold
		title.setFont(title_font) # Set font for title widget
		image_label = QLabel(self) # Create QLabel for image
		image = QPixmap("images/logo.png") # Load image at images/logo.png
		image_label.setPixmap(image) # Render image
		# Add widgets to layout
		template.addWidget(title, 1, 2)
		template.addWidget(QLabel("The Mini Browser is made using Python 3 and the\nPyQt Library by Daniel M"), 2, 2)
		template.addWidget(image_label, 2, 1)
		for i in range(template.count()):
			template.itemAt(i).setAlignment(Qt.AlignmentFlag.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(template) # Display the widgets


class ConfigDialog(QDialog):
	"""Browser settings dialog"""
	def __init__(self, parent=None) -> None:
		super(ConfigDialog, self).__init__(parent=parent)
		self.setWindowTitle("Settings") # Set window title
		self.template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("Settings") # Add QLabel named title
		title_font = title.font() # Create new font named title_font
		title_font.setPointSize(25) # Set point size for font
		title.setFont(title_font) # Set font for title QLabel as title_font
		# Add QLabel for history entries
		entries = open("Applications/MiniBrowser/config/history.txt", "r").read().count("\n")
		self.history_size = QLabel(f"History Size: {os.stat('Applications/MiniBrowser/config/history.txt').st_size} Bytes; {entries} Entries")
		# Add PushButton with text 'History' and call function openHistory in the current class when clicked
		self.history = PushButton()
		self.history.setText("History")
		self.history.clicked.connect(self.openHistory)
		# Add widgets to the layout
		self.template.addWidget(title, 1, 1)
		self.template.addWidget(self.history_size, 2, 1)
		self.template.addWidget(self.history, 2, 2)
		for i in range(self.template.count()):
			self.template.itemAt(i).setAlignment(Qt.AlignmentFlag.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(self.template) # Display the widgets

	@staticmethod # Set function openHistory static
	def openHistory() -> None:
		"""Open the History dialog"""
		dialog = History()
		dialog.exec_()


class History(QDialog):
	"""History dialog"""
	def __init__(self, parent=None) -> None:
		super(History, self).__init__(parent=parent)
		self.setWindowTitle("History") # Set window title to 'History'
		self.template = QVBoxLayout() # Set layout of dialog to Vertical Box Layout
		# Set fixed width and height
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("History") # Add new QLabel widget with the text 'History'
		# Add new font named 'title_font'
		title_font = title.font()
		title_font.setPointSize(25)
		title.setFont(title_font) # Set the 'title' QLabel's font to 'title_font'
		# Add QLabel for history entries
		entries = open("Applications/MiniBrowser/config/history.txt", "r").read().count("\n")
		self.history_info = QLabel(f"{os.stat('Applications/MiniBrowser/config/history.txt').st_size} Bytes with {entries} Entries")
		# Add new ScrollArea containing the text of Applications/MiniBrowser/config/history.txt
		self.history = ScrollArea()
		self.history.setText(str(open("Applications/MiniBrowser/config/history.txt", "r").read()))
		# Add new PushButton with text 'Clear History' and open the function clearHistory in the current class when clicked
		clear_history = PushButton()
		clear_history.setText("Clear History")
		clear_history.clicked.connect(self.clearHistory)
		# Add widgets to the layout
		self.template.addWidget(title, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.template.addWidget(self.history_info, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.template.addWidget(self.history, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.template.addWidget(clear_history, alignment=Qt.AlignmentFlag.AlignHCenter)
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(self.template) # Display the widgets

	def clearHistory(self) -> None:
		"""Clears the history by clearing the Applications/MiniBrowser/config/history.txt file and closes the window"""
		open("Applications/MiniBrowser/config/history.txt", "w+").write("")
		self.close()


class Browser(QMainWindow):
	"""Main Window"""
	def __init__(self) -> None:
		super(Browser, self).__init__()
		self.setMinimumWidth(QDesktopWidget().screenGeometry(-1).width() - 1000)
		self.setMinimumHeight(QDesktopWidget().screenGeometry(-1).height() - 500)
		self.tabs, self.bookmarks, self.url_bar, self.navigation, self.back, self.forward, self.reload, self.home, about_menu, about, self.config = TabWidget(), QToolBar("Bookmarks"), LineEdit(), ToolBar(self), QAction("←", self), QAction("→", self), QAction("↺", self), QAction("🏠", self), self.menuBar().addMenu("About"), QAction("About", self), QAction("⚙", self) # Define action variables
		self.navigation.setStyleSheet(f"background-color: {get_properties.returnBackgroundProperties()['background-color-2']}; font-size: 15px; font-family: {get_properties.returnProperties()['font-family']}; border: {get_properties.returnBackgroundProperties()['background-color-2']};") # Set font size of all items in the QToolBar named 'navigation' to 15px
		self.tabs.setDocumentMode(True) # Set document mode for the QTabWidget named 'tabs' to True
		self.tabs.tabBarDoubleClicked.connect(lambda: self.newTab(url=QUrl("https://home.danielmiao1.repl.co/")))
		self.tabs.currentChanged.connect(self.tabChanged) # Call the function tabChanged when tab is changed
		self.tabs.setTabsClosable(True) # Set tabs closable
		self.tabs.tabCloseRequested.connect(self.closeTab) # Call the function closeTab when user attempts to close a tab
		self.setCentralWidget(self.tabs) # Set central widget for the window as the tab widget
		# Add the tool bars 'navigation', and 'bookmarks', with a break between them
		self.addToolBar(self.navigation)
		self.addToolBarBreak()
		self.addToolBar(self.bookmarks)
		# Add back, forward, reload, and home actions to the toolbar named 'navigation', and their actions
		self.back.triggered.connect(lambda: self.tabs.currentWidget().back())
		self.navigation.addAction(self.back)
		self.forward.triggered.connect(lambda: self.tabs.currentWidget().forward())
		self.navigation.addAction(self.forward)
		self.reload.triggered.connect(lambda: self.tabs.currentWidget().reload())
		self.navigation.addAction(self.reload)
		self.home.triggered.connect(self.toHome)
		self.navigation.addAction(self.home)
		self.bookmarks.setMovable(False)
		# Add bookmark actions
		self.bookmarks_actions = [QAction("Google", self), QAction("YouTube", self), QAction("Gmail", self), QAction("Google Docs", self)]
		self.bookmarks_actions[0].triggered.connect(lambda: self.newTab(url=QUrl("https://www.google.com"), label="Google"))
		self.bookmarks_actions[1].triggered.connect(lambda: self.newTab(url=QUrl("https://www.youtube.com"), label="YouTube"))
		self.bookmarks_actions[2].triggered.connect(lambda: self.newTab(url=QUrl("https://mail.google.com"), label="Gmail"))
		self.bookmarks_actions[3].triggered.connect(lambda: self.newTab(url=QUrl("https://docs.google.com"), label="Google Docs"))
		for i in range(4):
			self.bookmarks.addAction(self.bookmarks_actions[i])
		self.bookmarks.setStyleSheet(f"border-top: 1px solid {get_properties.returnBackgroundProperties()['text-color']}; border: 2px solid {get_properties.returnBackgroundProperties()['background-color-2']}; background-color: {get_properties.returnBackgroundProperties()['background-color-2']}; font-size: {get_properties.returnProperties()['font-size']}; font-family: {get_properties.returnProperties()['font-family']}")
		self.navigation.setMovable(False) # Pin the 'navigation' toolbar
		self.url_bar.setFixedWidth(1275)
		self.url_bar.setStyleSheet(f"border: 2px solid {get_properties.returnBackgroundProperties()['background-color']}; font-size: {get_properties.returnProperties()['font-size']}; font-family: {get_properties.returnProperties()['font-family']}")
		self.url_bar.returnPressed.connect(self.toURL) # Call function toURL when 'enter' key is pressed in the 'url_bar'
		self.navigation.addWidget(self.url_bar) # Add 'url_bar' to the 'navigation' toolbar
		self.config.triggered.connect(self.openConfig) # Call function openConfig when 'config' QAction is pressed
		self.navigation.addAction(self.config) # Add 'config' QAction to 'navigation' toolbar
		about.triggered.connect(self.openAbout) # Call function openAbout when 'about' is triggered
		about_menu.addAction(about) # Add 'about' to the 'about_menu'
		self.newTab(url=QUrl("https://home.danielmiao1.repl.co/"))  # Add default tab
		self.show() # Show widgets
		
	def back(self) -> None:
		"""Go back, and record the new url in the history file"""
		self.tabs.currentWidget().back()
		open("Applications/MiniBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def forward(self) -> None:
		"""Go forward, and record the new url in the history file"""
		self.tabs.currentWidget().forward()
		open("Applications/MiniBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def reload(self) -> None:
		"""Reload, and record the new url in the history file"""
		self.tabs.currentWidget().reload()
		open("Applications/MiniBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")
		
	def newTab(self, url=QUrl("https://home.danielmiao1.repl.co/"), label="New Tab") -> None:
		"""Create a new tab"""
		engine = QWebEngineView() # Create new web engine view
		page = WebEnginePage(engine) # Create new web engine page
		engine.setPage(page) # Set page of view
		index = self.tabs.addTab(engine, label) # Add tab with the view and title
		self.tabs.setCurrentIndex(index) # Set current index of tabs
		engine.load(url) # Load URL
		engine.urlChanged.connect(lambda link, view=engine: self.updateURLBox(link, view)) # Update URL Box when the url changes
		engine.loadFinished.connect(lambda _, link=index, view=engine: self.tabs.setTabText(link, view.page().title())) # Set tab text
		
	def tabChanged(self, _) -> None:
		"""Update the URL box if tab URL changed"""
		url = self.tabs.currentWidget().url()
		self.updateURLBox(url, self.tabs.currentWidget())

	def closeTab(self, url: QUrl) -> None:
		"""Close tab"""
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(url)

	def toHome(self) -> None:
		"""Go to 'https://home.danielmiao1.repl.co/'"""
		self.tabs.currentWidget().setUrl(QUrl("https://home.danielmiao1.repl.co/"))
		open("Applications/MiniBrowser/config/history.txt", "a+").write("browser://home\n")

	def toURL(self) -> None:
		"""Go to the url given in the URL box or search google"""
		url = QUrl(self.url_bar.text())
		if url in ["browser://home", "browser:home"]:
			self.tabs.currentWidget().setUrl("https://home.danielmiao1.repl.co/")
		else:
			if list(url.toString()).count(".") == 0:
				url = QUrl(f"https://www.google.com/search?q={url.toString()}")
			elif url.scheme() == "":
				url = QUrl("http://" + url.toString())
			self.tabs.currentWidget().setUrl(url)

	def updateURLBox(self, url, engine=None) -> None:
		"""Update URL box text to the relative URL when URL changed"""
		if engine != self.tabs.currentWidget():
			return
		if not url.toString == "":
			open("Applications/MiniBrowser/config/history.txt", "a+").write(f"{url.toString()}\n")
			self.url_bar.setText(url.toString())
			self.url_bar.setCursorPosition(0)
			
	def contextMenuEvent(self, event: QEvent) -> None:
		"""Set context menu for central widget"""
		menu = QMenu(self)
		(back, forward, reload, home, action) = (menu.addAction("Back                "), menu.addAction("Forward             "), menu.addAction("Reload              "), menu.addAction("Home                "), menu.exec_(self.mapToGlobal(event.pos())))
		if action == back:
			self.tabs.currentWidget().back()
		elif action == forward:
			self.tabs.currentWidget().forward()
		elif action == reload:
			self.tabs.currentWidget().reload()
		elif action == home:
			self.toHome()

	@staticmethod # Set function openAbout static
	def openAbout() -> None:
		"""Open About dialog"""
		dialog = AboutDialog()
		dialog.exec_()

	@staticmethod # Set function openConfig static
	def openConfig() -> None:
		"""Open Config dialog"""
		dialog = ConfigDialog()
		dialog.exec_()
	
	def parentResizeEvent(self, event: QResizeEvent) -> None:
		self.url_bar.setFixedWidth(event.size().width() - 225)
