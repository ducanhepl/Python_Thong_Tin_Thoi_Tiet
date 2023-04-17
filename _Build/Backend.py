import os
import sys
import json
import requests
from bs4 import BeautifulSoup 
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
    )
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from Login_GUI import Ui_MainWindow as lg
from History_GUI import Ui_MainWindow as htr
from Weather_GUI import Ui_MainWindow as wea


#Login window
class Login(QMainWindow, lg):            
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.checkBox.stateChanged.connect(self.b_RememberInfo)
        self.login_button.clicked.connect(self.Login)        

    def Login(self):
        if self.GetUserName() and self.GetPassWord():            
            self.openMainWindow()                   
        else:
            QMessageBox.about(self, "Message", "Fail to login!")

    def b_RememberInfo(self):
        return self.checkBox.isChecked()
                        
    def GetUserName(self):
        username = self.username_text.toPlainText()
        return username
    
    def GetPassWord(self):
        password = self.password_text.text()     
        return password
    #open main window
    def openMainWindow(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

#Weather window    
class WeatherWindow(QMainWindow, wea):
    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0,500)
        self.connectSignalsSlots()
        

    def openHistoryWindow(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    def connectSignalsSlots(self):
        self.hanoi_button.clicked.connect(self.hanoi_weather)
        self.danang_button.clicked.connect(self.danang_weather)
        self.hochiminh_button.clicked.connect(self.hochiminh_weather)
        self.history_button.clicked.connect(self.openHistoryWindow)

    def get_data(self, url):
        html = requests.get(url)       
        soup = BeautifulSoup(html.text, 'html.parser')
        result = {}
        result['location'] = soup.find('span', attrs={'itemprop':'addressLocality'}).text
        result['time'] = soup.find("span", attrs={"class": "d-inline-block"}).text
        result['weather'] = soup.find("span", attrs={"class": "fs-3 fw-bold"}).text
        result['temperature'] = soup.find("span", attrs={"class": "text-primary fs-3"}).text
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(result['location']))
        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem(result['time']))
        self.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem(result['weather']))
        self.tableWidget.setItem(3, 0, QtWidgets.QTableWidgetItem(result['temperature']))

        data = [result]
        if os.path.isfile('history.json') is False:
            with open("history.json", "w") as outfile:
                json.dump(data, outfile)
        else:
            listObj = []
            with open('history.json') as fp:
                  listObj = json.load(fp)
            listObj.append(result)
            with open('history.json', 'w') as json_file:
                json.dump(listObj, json_file, indent=4, separators=(',',': '))
        

    def hanoi_weather(self):     
        url = 'https://www.weather-atlas.com/en/vietnam/hanoi'      
        self.get_data(url)
        

    def danang_weather(self):
        url = 'https://www.weather-atlas.com/en/vietnam/da-nang'       
        self.get_data(url)

    def hochiminh_weather(self):
        url = 'https://www.weather-atlas.com/en/vietnam/ho-chi-minh-city'      
        self.get_data(url)
            
#History window
class History(QMainWindow, htr):

    def __init__(self):
        super().__init__()        
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0,500)
        self.connectSignalsSlots()
        self.show_history()

    #back to weather window                       
    def returnWeatherWindow(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def connectSignalsSlots(self):
        self.return_button.clicked.connect(self.returnWeatherWindow)

    def show_history(self):
        if os.path.isfile('history.json') is True:
            f = open('history.json')
            data = json.load(f)
            n = len(data)
            row = 0
            if len(data) > 10:
                while len(data) - n < 10:
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(data[n-1].values())))
                    row += 1
                    n -= 1
            else:
                for i in range(0,len(data)):
                    self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(data[n-1].values())))
                    n -= 1
                                    
            
            
                                     
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    login = Login()   
    weatherwindow = WeatherWindow()
    history = History()
    widget.addWidget(login)    
    widget.addWidget(weatherwindow)
    widget.addWidget(history)
    widget.setFixedHeight(295)
    widget.setFixedWidth(520)
    widget.show()
    sys.exit(app.exec_())
