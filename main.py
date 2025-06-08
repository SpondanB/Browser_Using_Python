import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spondan's Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Web engine view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)

        # Navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        # Back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)
        
        # home button
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(lambda: self.browser.setUrl(QUrl("https://www.google.com")))
        nav_bar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Update URL bar when page changes
        self.browser.urlChanged.connect(self.update_url_bar)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
