# -*- coding: utf-8 -*-
import os
import sys

import json

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class PushButton(QPushButton):
	# noinspection PyUnresolvedReferences
	def __init__(self):
		super().__init__()
		self._animation = QVariantAnimation(startValue = QColor("white"), endValue = QColor("#18082C"), valueChanged = self.valueChanged, duration = 200)
		self.updateStylesheet(QColor("#18082C"), QColor("white"))
		self.setCursor(QCursor(Qt.PointingHandCursor))

	def valueChanged(self, color): self.updateStylesheet(color, QColor("white") if self._animation.direction() == QAbstractAnimation.Forward else QColor("#18082C"))

	def updateStylesheet(self, background, foreground): self.setStyleSheet("QPushButton {background-color: %s; color: %s; padding: 16px 32px; text-align: center; text-decoration: none; font-size: 16px; margin: 4px 2px; border: 2px solid white;}" % (background.name(), foreground.name()))

	def enterEvent(self, event):
		self._animation.setDirection(QAbstractAnimation.Backward)
		self._animation.start()
		super().enterEvent(event)

	def leaveEvent(self, event):
		self._animation.setDirection(QAbstractAnimation.Forward)
		self._animation.start()
		super().leaveEvent(event)

class LineEdit(QLineEdit):
	def __init__(self, parent = None): super(LineEdit, self).__init__(parent)

	def mousePressEvent(self, _): self.setCursorPosition(len(self.text())) if self.hasSelectedText() else self.selectAll()

class ScrollArea(QScrollArea):
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
	def createWindow(self, _type):
		# if not isinstance(self.window(), Window): return
		if _type in [QWebEnginePage.WebBrowserTab, QWebEnginePage.WebBrowserBackgroundTab]: return self._tab_factory_func()
		return self._window_factory_func

class TabWidget(QTabWidget):
	def createTab(self):
		view = WebEngineView()
		self.addTab(view, "New Tab")

# noinspection PyUnresolvedReferences,PyArgumentList
class AboutDialog(QDialog):
	def __init__(self, parent = None):
		super(AboutDialog, self).__init__(parent = parent)
		template = QGridLayout()
		self.setFixedHeight(self.height() - 175)
		self.setFixedWidth(self.width() + 100)
		title = QLabel("Simplifyc Browser")
		title_font = title.font()
		title_font.setPointSize(50)
		title_font.setBold(True)
		title.setFont(title_font)
		image_label = QLabel(self)
		image = QPixmap("images/logo.png")
		image_label.setPixmap(image)
		template.addWidget(title, 1, 2)
		template.addWidget(QLabel("The Simplifyc Browser is made using Python 3 and the\nPyQt Library by Daniel M"), 2, 2)
		template.addWidget(image_label, 2, 1)
		for i in range(template.count()): template.itemAt(i).setAlignment(Qt.AlignHCenter)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(template)

# noinspection PyUnresolvedReferences,PyArgumentList
class ConfigDialog(QDialog):
	def __init__(self, parent = None):
		super(ConfigDialog, self).__init__(parent = parent)
		self.setWindowTitle("Settings")
		self.template = QGridLayout()
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("Settings")
		title_font = title.font()
		title_font.setPointSize(25)
		title.setFont(title_font)
		entries = open("config/history.txt", "r").read().count("\n")
		self.history_size = QLabel(f"History Size: {os.stat('config/history.txt').st_size} Bytes; {entries} Entries")
		self.history = PushButton()
		self.history.setText("History")
		self.history.clicked.connect(self.openHistory)
		self.bookmarks = PushButton()
		self.bookmarks.setText("Bookmarks")
		self.bookmarks.clicked.connect(self.openBookmarks)
		self.template.addWidget(title, 1, 1)
		self.template.addWidget(self.history_size, 2, 1)
		self.template.addWidget(self.history, 2, 2)
		self.template.addWidget(self.bookmarks, 3, 1)
		for i in range(self.template.count()): self.template.itemAt(i).setAlignment(Qt.AlignHCenter)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(self.template)

	@staticmethod
	def openHistory():
		dialog = History()
		dialog.exec_()

	@staticmethod
	def openBookmarks():
		dialog = Bookmarks()
		dialog.exec_()

class History(QDialog):
	def __init__(self, parent = None):
		super(History, self).__init__(parent = parent)
		self.setWindowTitle("History")
		self.template = QVBoxLayout()
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("History")
		title_font = title.font()
		title_font.setPointSize(25)
		title.setFont(title_font)
		entries = open("config/history.txt", "r").read().count("\n")
		self.history_info = QLabel(f"{os.stat('config/history.txt').st_size} Bytes with {entries} Entries")
		self.history = ScrollArea()
		self.history.setText(str(open("config/history.txt", "r").read()))
		clear_history = PushButton()
		clear_history.setText("Clear History")
		clear_history.clicked.connect(self.clearHistory)
		self.template.addWidget(title)
		self.template.addWidget(self.history_info)
		self.template.addWidget(self.history)
		self.template.addWidget(clear_history)
		for i in range(self.template.count() - 1): self.template.itemAt(i).setAlignment(Qt.AlignHCenter)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(self.template)

	def clearHistory(self):
		open("config/history.txt", "w+").write("")
		history_info = QLabel("0 Bytes with 0 Entries")
		self.history_info.update()
		history = ScrollArea()
		history.setText("")
		self.history.update()

# noinspection PyUnresolvedReferences,PyArgumentList
class Bookmarks(QDialog):
	def __init__(self, parent = None):
		super(Bookmarks, self).__init__(parent = parent)
		self.setWindowTitle("Bookmarks")
		self.template = QVBoxLayout()
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		title = QLabel("Bookmarks")
		title_font = title.font()
		title_font.setPointSize(25)
		title.setFont(title_font)
		new_bookmark = PushButton()
		new_bookmark.setText("New Bookmark")
		new_bookmark.clicked.connect(self.newBookmark)
		self.template.addWidget(title)
		self.template.addWidget(new_bookmark)
		for i in range(self.template.count()): self.template.itemAt(i).setAlignment(Qt.AlignHCenter)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(self.template)

	@staticmethod
	def newBookmark():
		dialog = NewBookmark()
		dialog.exec_()

# noinspection PyArgumentList
class NewBookmark(QDialog):
	def __init__(self, parent = None):
		super(NewBookmark, self).__init__(parent = parent)
		self.setWindowTitle("New Bookmark")
		self.template = QVBoxLayout()
		self.setFixedWidth(500)
		self.setFixedHeight(500)
		self.setStyleSheet("color: white; background-color: #18082C;")
		self.setLayout(self.template)

class Window(QMainWindow):
	# noinspection PyArgumentList
	def __init__(self):
		super(Window, self).__init__()
		(self.tabs, self.status, self.bookmarks, self.url_bar, self.navigation, self.back, self.forward, self.reload, self.home, about_menu, about, self.config) = (QTabWidget(), QStatusBar(), QToolBar("Bookmarks"), LineEdit(), QToolBar("Navigation"), QAction("←", self), QAction("→", self), QAction("↺", self), QAction("🏠", self), self.menuBar().addMenu("About"), QAction(QIcon(os.path.join("images", "question.png")), "About", self), QAction("⚙", self))
		self.navigation.setStyleSheet("font-size: 15px;")
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.openTab)
		self.tabs.currentChanged.connect(self.tabChanged)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.closeTab)
		self.setCentralWidget(self.tabs)
		self.setStatusBar(self.status)
		self.addToolBar(self.navigation)
		self.addToolBarBreak()
		self.addToolBar(self.bookmarks)
		self.back.triggered.connect(lambda: self.tabs.currentWidget().back())
		self.navigation.addAction(self.back)
		self.forward.triggered.connect(lambda: self.tabs.currentWidget().forward())
		self.navigation.addAction(self.forward)
		self.reload.triggered.connect(lambda: self.tabs.currentWidget().reload())
		self.navigation.addAction(self.reload)
		self.home.triggered.connect(self.toHome)
		self.navigation.setMovable(False)
		self.navigation.addAction(self.home)
		self.url_bar.returnPressed.connect(self.toURL)
		self.navigation.addWidget(self.url_bar)
		self.config.triggered.connect(self.openConfig)
		self.navigation.addAction(self.config)
		about.setStatusTip("About")
		about.triggered.connect(self.openAbout)
		about_menu.addAction(about)
		self.newTab(QUrl("https://home.danielmiao1.repl.co/"), "New Tab")
		self.show()

	def back(self):
		self.tabs.currentWidget().back()
		open("config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def forward(self):
		self.tabs.currentWidget().forward()
		open("config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def reload(self):
		self.tabs.currentWidget().reload()
		open("config/history.txt", "a+").write(f"{self.url_bar.text()}\n")

	def newTab(self, url = None, label = "New Tab"):
		if url is None: url = QUrl("https://home.danielmiao1.repl.co/")
		engine = QWebEngineView()
		engine.setUrl(url)
		url = self.tabs.addTab(engine, label)
		self.tabs.setCurrentIndex(url)
		engine.urlChanged.connect(lambda link, view = engine: self.updateURLBox(link, view))
		engine.loadFinished.connect(lambda _, link = url, view = engine: self.tabs.setTabText(link, view.page().title()))

	def openTab(self, url):
		if url == -1: self.newTab()

	def tabChanged(self, _):
		url = self.tabs.currentWidget().url()
		self.updateURLBox(url, self.tabs.currentWidget())

	def closeTab(self, url):
		if self.tabs.count() < 2: return
		self.tabs.removeTab(url)

	def toHome(self):
		self.tabs.currentWidget().setUrl(QUrl("https://home.danielmiao1.repl.co/"))
		open("config/history.txt", "a+").write("browser://home\n")

	def toURL(self):
		url = QUrl(self.url_bar.text())
		if url in ["browser://home", "browser:home"]:
			self.tabs.currentWidget().setUrl("https://home.danielmiao1.repl.co/")
			return
		if list(url.toString()).count(".") == 0: url = QUrl(f"https://www.google.com/search?q={url.toString()}")
		elif url.scheme() == "": url.setScheme("http")
		self.tabs.currentWidget().setUrl(url)

	def updateURLBox(self, url, engine = None):
		if engine != self.tabs.currentWidget(): return
		if not url.toString == "":
			open("config/history.txt", "a+").write(f"{url.toString()}\n")
			self.url_bar.setText("") if url.toString().lower() == "https://home.danielmiao1.repl.co/" else self.url_bar.setText(url.toString())
			self.url_bar.setCursorPosition(0)

	def contextMenuEvent(self, event):
		menu = QMenu(self)
		(back, forward, reload, home, action) = (menu.addAction("Back                "), menu.addAction("Forward             "), menu.addAction("Reload              "), menu.addAction("Home                "), menu.exec_(self.mapToGlobal(event.pos())))
		if action == back: self.tabs.currentWidget().back()
		elif action == forward: self.tabs.currentWidget().forward()
		elif action == reload: self.tabs.currentWidget().reload()
		elif action == home: self.toHome()

	@staticmethod
	def openAbout():
		dialog = AboutDialog()
		dialog.exec_()

	@staticmethod
	def openConfig():
		dialog = ConfigDialog()
		dialog.exec_()


(browser, window) = (QApplication(sys.argv), Window())
browser.exec_()
