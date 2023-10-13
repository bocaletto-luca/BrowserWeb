# Software Name: Web Browser
# Author: Luca Bocaletto
# Website: https://www.elektronoide.it

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate)
        
        nav_bar = QToolBar()
        nav_bar.addWidget(self.url_bar)
        self.addToolBar(nav_bar)
        
        # Button to go back
        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Go back to the previous page")
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # Button to go forward
        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Go to the next page")
        forward_btn.triggered connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # Button to reload the page
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload the current page")
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # Button to go to the home page
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go back to the home page")
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        # Add an action to update the URL in the address bar when the page changes
        self.browser.urlChanged.connect(self.update_urlbar)

        self.setCentralWidget(self.browser)
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1024, 768)  # Set the minimum size

        # Advanced security and privacy settings
        self.setup_security_settings()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://duckduckgo.com"))  # Set DuckDuckGo as the home page

    def navigate(self):
        user_input = self.url_bar.text()
        if "." in user_input:
            url = QUrl.fromUserInput(user_input)
        else:
            search_query = user_input
            url = QUrl("https://duckduckgo.com/?q={}".format(search_query))
        
        self.browser.setUrl(url)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def setup_security_settings(self):
        # Disable JavaScript execution (a potential source of tracking)
        self.browser.page().settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)

        # Block third-party resource requests (possible trackers)
        self.browser.page().profile().cookieStore().deleteAllCookies()  # Clear cookies

    def block_third_party_requests(self, info):
        if info.requestUrl().host() != info.firstPartyRequestUrl().host():
            info.block(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Web Browser")
    window = WebBrowser()
    window.show()
    app.exec_()
