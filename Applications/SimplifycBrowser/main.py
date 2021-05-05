# -*- coding: utf-8 -*-
# Simplifyc Browser
# Web browser made by Daniel M using Python 3 for the SimplifycOS project: https://github.com/DanielMiao1/SimplifycOS

# Imports
import os
import sys

# import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

# PyQt5 widget overrides
# noinspection PyArgumentList
class PushButton(QPushButton):
	# noinspection PyUnresolvedReferences
	"""Add QPushButton Animation"""
	def __init__(self):
		super().__init__()
		self._animation = QVariantAnimation(startValue = QColor("white"), endValue = QColor("#18082C"), valueChanged = self.valueChanged, duration = 200)
		self.updateStylesheet(QColor("#18082C"), QColor("white"))
		self.setCursor(QCursor(Qt.PointingHandCursor))

	def valueChanged(self, color): self.updateStylesheet(color, QColor("white") if self._animation.direction() == QAbstractAnimation.Forward else QColor("#18082C"))

	def updateStylesheet(self, background, foreground): self.setStyleSheet("QPushButton {background-color: %s; color: %s; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}" % (background.name(), foreground.name()))

	def enterEvent(self, event):
		# Display backward color animation on mouse hover
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)

	def leaveEvent(self, event):
		# Display forward color animation on mouse leave
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)

class LineEdit(QLineEdit):
	""""Add select all when pressed feature to QLineEdit"""
	def __init__(self, parent = None): super(LineEdit, self).__init__(parent)

	def mousePressEvent(self, _): self.setCursorPosition(len(self.text())) if self.hasSelectedText() else self.selectAll() # Select all when pressed unless text is already selected

class ScrollArea(QScrollArea):
	"""Set word wrap of QScrollArea to True"""
	def __init__(self):
		QScrollArea.__init__(self)
		self.setWidgetResizable(True)
		text = QWidget(self)
		self.setWidget(text)
		template = QVBoxLayout(text)
		self.label = QLabel(text)
		self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		self.label.setWordWrap(True)
		template.addWidget(self.label)

	def setText(self, text): self.label.setText(text)

class WebEngineView(QWebEngineView):
	"""Handle target='_blank' hyperlinks in webpages"""
	def createWindow(self, _type):
		# if not isinstance(self.window(), Window): return
		if _type in [QWebEnginePage.WebBrowserTab, QWebEnginePage.WebBrowserBackgroundTab]: return self._tab_factory_func()
		return self._window_factory_func

class TabWidget(QTabWidget):
	"""Set default tab title of QTabWidget to 'New Tab'"""
	def createTab(self):
		view = WebEngineView()
		self.addTab(view, "New Tab")

# Dialogs
# noinspection PyUnresolvedReferences,PyArgumentList
class AboutDialog(QDialog):
	"""About Simplifyc Browser dialog"""
	def __init__(self, parent = None):
		super(AboutDialog, self).__init__(parent = parent)
		template = QGridLayout() # Set layout to grid
		# Set fixed width and height
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("Simplifyc Browser") # Add title
		title_font = title.font() # Add new font
		title_font.setPointSize(50) # Set point size for font
		title_font.setBold(True) # Make font bold
		title.setFont(title_font) # Set font for title widget
		image_label = QLabel(self) # Create QLabel for image
		image = QPixmap("images/logo.png") # Load image at images/logo.png
		image_label.setPixmap(image) # Render image
		# Add widgets to layout
		template.addWidget(title, 1, 2)
		template.addWidget(QLabel("The Simplifyc Browser is made using Python 3 and the\nPyQt Library by Daniel M"), 2, 2)
		template.addWidget(image_label, 2, 1)
		for i in range(template.count()): template.itemAt(i).setAlignment(Qt.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(template) # Display the widgets

# noinspection PyUnresolvedReferences,PyArgumentList
class ConfigDialog(QDialog):
	"""Browser settings dialog"""
	def __init__(self, parent = None):
		super(ConfigDialog, self).__init__(parent = parent)
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
		entries = open("Applications/SimplifycBrowser/config/history.txt", "r").read().count("\n")
		self.history_size = QLabel(f"History Size: {os.stat('Applications/SimplifycBrowser/config/history.txt').st_size} Bytes; {entries} Entries")
		# Add PushButton with text 'History' and call function openHistory in the current class when clicked
		self.history = PushButton()
		self.history.setText("History")
		self.history.clicked.connect(self.openHistory)
		# Add PushButton with text 'Bookmarks' and call function openBookmarks in the current class when clicked
		self.bookmarks = PushButton()
		self.bookmarks.setText("Bookmarks")
		self.bookmarks.clicked.connect(self.openBookmarks)
		# Add widgets to the layout
		self.template.addWidget(title, 1, 1)
		self.template.addWidget(self.history_size, 2, 1)
		self.template.addWidget(self.history, 2, 2)
		self.template.addWidget(self.bookmarks, 3, 1)
		for i in range(self.template.count()): self.template.itemAt(i).setAlignment(Qt.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(self.template) # Display the widgets

	@staticmethod # Set function openHistory static
	def openHistory(): # Open the History dialog
		dialog = History()
		dialog.exec_()

	@staticmethod # Set function openBookmarks static
	def openBookmarks(): # Open the Bookmarks dialog
		dialog = Bookmarks()
		dialog.exec_()

class History(QDialog):
	"""History dialog"""
	def __init__(self, parent = None):
		super(History, self).__init__(parent = parent)
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
		entries = open("Applications/SimplifycBrowser/config/history.txt", "r").read().count("\n")
		self.history_info = QLabel(f"{os.stat('Applications/SimplifycBrowser/config/history.txt').st_size} Bytes with {entries} Entries")
		# Add new ScrollArea containing the text of Applications/SimplifycBrowser/config/history.txt
		self.history = ScrollArea()
		self.history.setText(str(open("Applications/SimplifycBrowser/config/history.txt", "r").read()))
		# Add new PushButton with text 'Clear History' and open the function clearHistory in the current class when clicked
		clear_history = PushButton()
		clear_history.setText("Clear History")
		clear_history.clicked.connect(self.clearHistory)
		# Add widgets to the layout
		self.template.addWidget(title)
		self.template.addWidget(self.history_info)
		self.template.addWidget(self.history)
		self.template.addWidget(clear_history)
		for i in range(self.template.count() - 1): self.template.itemAt(i).setAlignment(Qt.AlignHCenter) # Align all widgets to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(self.template) # Display the widgets

	def clearHistory(self): # Clears the history by clearing the Applications/SimplifycBrowser/config/history.txt file and updates the ScrollArea and the history QLabel
		open("Applications/SimplifycBrowser/config/history.txt", "w+").write("")
		self.history_info.update()
		history = ScrollArea()
		history.setText("")
		self.history.update()

# noinspection PyUnresolvedReferences,PyArgumentList
class Bookmarks(QDialog):
	"""Bookmarks Dialog"""
	def __init__(self, parent = None):
		super(Bookmarks, self).__init__(parent = parent)
		self.setWindowTitle("Bookmarks") # Set window title to 'Bookmarks'
		self.template = QVBoxLayout() # Set layout of dialog to Vertical Box Layout
		# Set fixed width adn height
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("Bookmarks") # Add QLabel named 'title' with text 'Bookmarks'
		# Create new font named 'title_font'
		title_font = title.font()
		title_font.setPointSize(25)
		title.setFont(title_font) # Set font of QLabel 'title' to 'title_font'
		# Add new PushButton with text 'New Bookmark' and open the function newBookmark in the current class when clicked
		new_bookmark = PushButton()
		new_bookmark.setText("New Bookmark")
		new_bookmark.clicked.connect(self.newBookmark)
		# Add widgets to the layout
		self.template.addWidget(title)
		self.template.addWidget(new_bookmark)
		for i in range(self.template.count()): self.template.itemAt(i).setAlignment(Qt.AlignHCenter) # Set alignment for all widgets in the layout to center
		self.setStyleSheet("color: white; background-color: #18082C;") # Set background color of dialog to #18082C and color of text to white
		self.setLayout(self.template) # Display widgets

	@staticmethod # Set function newBookmark static
	def newBookmark(): # Open the NewBookmark dialog
		dialog = NewBookmark()
		dialog.exec_()

# noinspection PyArgumentList
class NewBookmark(QDialog):
	"""New Bookmark Dialog"""
	def __init__(self, parent = None):
		# NOT FINISHED
		super(NewBookmark, self).__init__(parent = parent)
		self.setWindowTitle("New Bookmark")
		self.template = QVBoxLayout()
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(self.template)

class Window(QMainWindow):
	"""Main Window"""
	# noinspection PyArgumentList
	def __init__(self):
		super(Window, self).__init__()
		(self.tabs, self.bookmarks, self.url_bar, self.navigation, self.back, self.forward, self.reload, self.home, about_menu, about, self.config) = (QTabWidget(), QToolBar("Bookmarks"), LineEdit(), QToolBar("Navigation"), QAction("←", self), QAction("→", self), QAction("↺", self), QAction("🏠", self), self.menuBar().addMenu("About"), QAction(QIcon(os.path.join("images", "question.png")), "About", self), QAction("⚙", self)) # Define variables
		self.navigation.setStyleSheet("font-size: 15px;") # Set font size of all items in the QToolBar named 'navigation' to 15px
		self.tabs.setDocumentMode(True) # Set document mode for the QTabWidget named 'tabs' to True
		self.tabs.tabBarDoubleClicked.connect(self.openTab) # Call the function openTab when the tab bar is double clicked
		self.tabs.currentChanged.connect(self.tabChanged) # Call the function tabChanged when tab is changed
		self.tabs.setTabsClosable(True) # Set tabs closable
		self.tabs.tabCloseRequested.connect(self.closeTab) # Call the function closeTab when user attempts to close a tab
		self.setCentralWidget(self.tabs) # Set central widget for the window as the tab widget
		# Add the tool bars 'navigation' and 'bookmarks', with a break between them
		self.addToolBar(self.navigation)
		self.addToolBarBreak()
		self.addToolBar(self.bookmarks)
		# Add back, forward, reload, and home actions to the tool bar named 'navigation', and their actions
		self.back.triggered.connect(lambda: self.tabs.currentWidget().back())
		self.navigation.addAction(self.back)
		self.forward.triggered.connect(lambda: self.tabs.currentWidget().forward())
		self.navigation.addAction(self.forward)
		self.reload.triggered.connect(lambda: self.tabs.currentWidget().reload())
		self.navigation.addAction(self.reload)
		self.home.triggered.connect(self.toHome)
		self.navigation.addAction(self.home)
		# Pin the 'navigation' tool bar
		self.navigation.setMovable(False)
		self.url_bar.returnPressed.connect(self.toURL) # Call function toURL when 'enter' key is pressed in the 'url_bar'
		self.navigation.addWidget(self.url_bar) # Add 'url_bar' to the 'navigation' tool bar
		self.config.triggered.connect(self.openConfig) # Call function openConfig when 'config' QAction is pressed
		self.navigation.addAction(self.config) # Add 'config' QAction to 'navigation' tool bar
		about.triggered.connect(self.openAbout) # Call function openAbout when 'about' is triggered
		about_menu.addAction(about) # Add 'about' to the 'about_menu'
		self.newTab() # Add default tab
		self.show() # Show widgets

	def back(self): # Go back, and record the new url in the history file
		self.tabs.currentWidget().back()
		open("Applications/SimplifycBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def forward(self): # Go forward, and record the new url in the history file
		self.tabs.currentWidget().forward()
		open("Applications/SimplifycBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def reload(self): # Reload, and record the new url in the history file
		self.tabs.currentWidget().reload()
		open("Applications/SimplifycBrowser/config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def newTab(self, url = None, label = "New Tab"): # Create a new tab
		if url is None: url = QUrl("https://home.danielmiao1.repl.co/")
		engine = QWebEngineView()
		engine.setUrl(url)
		url = self.tabs.addTab(engine, label)
		self.tabs.setCurrentIndex(url)
		engine.urlChanged.connect(lambda link, view = engine: self.updateURLBox(link, view))
		engine.loadFinished.connect(lambda _, link = url, view = engine: self.tabs.setTabText(link, view.page().title()))

	def openTab(self, url): # Call newTab function if url is valid
		if url == -1: self.newTab()

	def tabChanged(self, _): # Update the URL box if tab URL changed
		url = self.tabs.currentWidget().url()
		self.updateURLBox(url, self.tabs.currentWidget())

	def closeTab(self, url): # Close tab
		if self.tabs.count() < 2: return
		self.tabs.removeTab(url)

	def toHome(self): # Go to 'https://home.danielmiao1.repl.co/'
		self.tabs.currentWidget().setUrl(QUrl("https://home.danielmiao1.repl.co/"))
		open("Applications/SimplifycBrowser/config/history.txt", "a+").write("browser://home\n")

	def toURL(self): # Go to the url given in the URL box or search google
		url = QUrl(self.url_bar.text())
		if url in ["browser://home", "browser:home"]:
			self.tabs.currentWidget().setUrl("https://home.danielmiao1.repl.co/")
			return
		if list(url.toString()).count(".") == 0: url = QUrl(f"https://www.google.com/search?q={url.toString()}")
		elif url.scheme() == "": url.setScheme("http")
		self.tabs.currentWidget().setUrl(url)

	def updateURLBox(self, url, engine = None): # Update URL box text to the relative URL when URL changed
		if engine != self.tabs.currentWidget(): return
		if not url.toString == "":
			open("Applications/SimplifycBrowser/config/history.txt", "a+").write(f"{url.toString()}\n")
			self.url_bar.setText("") if url.toString().lower() == "https://home.danielmiao1.repl.co/" else self.url_bar.setText(url.toString())
			self.url_bar.setCursorPosition(0)

	def contextMenuEvent(self, event): # Set context menu for central widget
		menu = QMenu(self)
		(back, forward, reload, home, action) = (menu.addAction("Back                "), menu.addAction("Forward             "), menu.addAction("Reload              "), menu.addAction("Home                "), menu.exec_(self.mapToGlobal(event.pos())))
		if action == back: self.tabs.currentWidget().back()
		elif action == forward: self.tabs.currentWidget().forward()
		elif action == reload: self.tabs.currentWidget().reload()
		elif action == home: self.toHome()

	@staticmethod # Set function openAbout static
	def openAbout(): # Open About dialog
		dialog = AboutDialog()
		dialog.exec_()

	@staticmethod # Set function openConfig static
	def openConfig(): # Open Config dialog
		dialog = ConfigDialog()
		dialog.exec_()


(browser, window) = (QApplication(sys.argv), Window())
browser.exec_() # Create new Qt application and run Window class
