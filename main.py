import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QTabWidget, 
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt


class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spondan's Tabbed Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.create_new_tab()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.init_toolbar()

        # Keep URL bar in sync with current tab
        self.tabs.currentChanged.connect(self.update_url_bar_from_tab)
        
        self.init_bookmark_bar()
        self.bookmarks = {} 

    def init_toolbar(self):
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav_bar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        nav_bar.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        dark_mode_btn = QAction("Toggle Dark Mode", self)
        dark_mode_btn.triggered.connect(self.toggle_dark_mode)
        nav_bar.addAction(dark_mode_btn)

        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(self.create_new_tab)
        nav_bar.addAction(new_tab_btn)

        nav_bar.addWidget(self.url_bar)
        
        bookmark_btn = QAction("Bookmark Page", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        nav_bar.addAction(bookmark_btn)

    def create_new_tab(self, url=None):
        new_tab = BrowserTab()
        if url:
            new_tab.browser.setUrl(QUrl(url))
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

        # Update tab title on page load
        new_tab.browser.titleChanged.connect(
            lambda title, tab=new_tab: self.tabs.setTabText(self.tabs.indexOf(tab), title)
        )

        # Keep URL bar in sync
        new_tab.browser.urlChanged.connect(self.update_url_bar_from_browser)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def current_browser(self):
        return self.tabs.currentWidget().browser

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http"):
            # Smart search if not a URL
            url = "https://www.google.com/search?q=" + url.replace(" ", "+")
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar_from_browser(self, q):
        self.url_bar.setText(q.toString())

    def update_url_bar_from_tab(self, i):
        if i >= 0:
            browser = self.current_browser()
            self.url_bar.setText(browser.url().toString())
            browser.urlChanged.connect(self.update_url_bar_from_browser)

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://www.google.com"))

    def toggle_dark_mode(self):
        if self.styleSheet():
            self.setStyleSheet("")  # Light mode
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                    color: #ffffff;
                }
                QTabWidget::pane {
                    border: 1px solid #444;
                }
                QTabBar::tab {
                    background: #2c2c2c;
                    color: white;
                    padding: 8px;
                }
                QTabBar::tab:selected {
                    background: #3a3a3a;
                }
                QLineEdit {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QToolBar {
                    background-color: #1e1e1e;
                    spacing: 10px;
                }
                QToolButton {
                    color: white;
                    background-color: transparent;
                    border: none;
                    padding: 5px;
                }
                QToolButton:hover {
                    background-color: #333333;
                }
            """)
    def init_bookmark_bar(self):
        self.bookmark_frame = QFrame()
        self.bookmark_layout = QHBoxLayout()
        self.bookmark_frame.setLayout(self.bookmark_layout)
        self.bookmark_frame.setFrameShape(QFrame.StyledPanel)
        self.bookmark_frame.setStyleSheet("background-color: #1e1e1e;")
    
        # Add bookmark bar under toolbar
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.bookmark_frame)
        self.layout.addWidget(self.tabs)
    
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def add_bookmark(self):
        browser = self.current_browser()
        title = browser.title() or "Untitled"
        url = browser.url().toString()
    
        if url in self.bookmarks:
            return  # Skip duplicates
    
        # Create a button styled like a tab
        btn = QPushButton(title)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2c2c2c;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px 12px;
                margin-right: 4px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
        """)
        # Clicking opens the URL in the current tab (you can change to create_new_tab(url=url) for new tab)
        btn.clicked.connect(lambda _, url=url: self.create_new_tab(url=url))
    
        self.bookmark_layout.addWidget(btn)
        self.bookmarks[url] = btn




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
