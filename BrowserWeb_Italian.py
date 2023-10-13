# Software Name: Browser Web
# Author: Bocaletto Luca
# Site Web: https://www.elektronoide.it

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
        
        # Pulsante per tornare indietro
        back_btn = QAction("Indietro", self)
        back_btn.setStatusTip("Torna alla pagina precedente")
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)

        # Pulsante per avanzare
        forward_btn = QAction("Avanti", self)
        forward_btn.setStatusTip("Vai alla pagina successiva")
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)

        # Pulsante per ricaricare la pagina
        reload_btn = QAction("Ricarica", self)
        reload_btn.setStatusTip("Ricarica la pagina corrente")
        reload_btn.triggered.connect(self.browser.reload)
        nav_bar.addAction(reload_btn)

        # Pulsante per tornare alla pagina iniziale
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Torna alla pagina iniziale")
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        # Aggiunge un'azione per aggiornare l'URL nella barra degli indirizzi quando cambia la pagina
        self.browser.urlChanged.connect(self.update_urlbar)

        self.setCentralWidget(self.browser)
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1024, 768)  # Imposta la dimensione minima

        # Impostazioni avanzate di sicurezza e privacy
        self.setup_security_settings()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://duckduckgo.com"))  # Imposta DuckDuckGo come pagina iniziale

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
        # Disabilita l'esecuzione di JavaScript (potenziale fonte di tracciamento)
        self.browser.page().settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)

        # Blocco delle richieste di risorse di terze parti (possibili tracker)
        self.browser.page().profile().cookieStore().deleteAllCookies()  # Cancella i cookie

    def block_third_party_requests(self, info):
        if info.requestUrl().host() != info.firstPartyRequestUrl().host():
            info.block(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Web Browser")
    window = WebBrowser()
    window.show()
    app.exec_()
