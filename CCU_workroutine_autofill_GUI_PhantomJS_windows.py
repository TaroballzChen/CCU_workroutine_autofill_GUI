from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException,UnexpectedAlertPresentException
import calendar
import threading
import time
import os
import json
import sys

class window(QtWidgets.QWidget,):
    def __init__(self):
        super().__init__()
        self.routine = []
        self.projectnumber_list = []
        self.config = {}
        self.init_UI()
        self.LoadData()

    def LoadData(self):
        if os.path.isfile("config.json"):
            with open("config.json",'r') as json_load:
                if json_load.read() != "":
                    json_load.seek(0)
                    self.config = json.load(json_load)
                    self.ConfigReset()
        else:
            config = open("config.json",'w')
            config.close()

    def ConfigReset(self):
        self.username = self.config["username"]
        self.user_input.setText(self.username)
        self.password = self.config["password"]
        self.pass_input.setText(self.password)
        self.job_combo.setCurrentText(self.config["job"])
        self.projectnumber_list = self.config["project"]
        [self.jobs_combo.addItem(jobnum) for jobnum in self.projectnumber_list]
        self.routine = self.config["routine"]
        [self.routine_combo.addItem(routine) for routine in self.routine]
        self.wk_hr_input.setText(self.config["workhour"])


    def init_UI(self):
        self.setGeometry(100,100,700,800)

        UI_layout = QtWidgets.QVBoxLayout()
        UI_layout.addLayout(self.login_block())
        UI_layout.addLayout(self.projectnumber_block())
        UI_layout.addLayout(self.date_block())
        UI_layout.addLayout(self.routine_block())
        UI_layout.addLayout(self.Console_block())
        UI_layout.addWidget(self.run_block())

        self.setWindowTitle('CCU Workroutine Autofill GUI Ver3.0 Designed by Yuan-Yu')
        self.setLayout(UI_layout)

    def login_block(self):
        self.job_list = ["計畫主持人","專任助理","兼任助理","臨時工"]
        self.user_input = QtWidgets.QLineEdit()
        self.user_input.setFixedWidth(100)
        user_l =QtWidgets.QLabel("Username")
        self.pass_input = QtWidgets.QLineEdit()
        self.pass_input.setEchoMode(self.pass_input.Password)
        pwd_l = QtWidgets.QLabel("Password")
        self.job_combo = QtWidgets.QComboBox()
        self.job_combo.addItems(self.job_list)
        box = QtWidgets.QHBoxLayout()
        box.addWidget(user_l)
        box.addWidget(self.user_input)
        box.addWidget(pwd_l)
        box.addWidget(self.pass_input)
        box.addWidget(self.job_combo)
        return box

#####################################################################################################
    def projectnumber_block(self):
        add_projectnum = QtWidgets.QLabel("添加計畫編號")
        self.proj_year_input  = QtWidgets.QLineEdit()
        dash = QtWidgets.QLabel("-")
        self.proj_No_input  = QtWidgets.QLineEdit()
        self.add_proj_button = QtWidgets.QPushButton("添加")
        select_proj_l = QtWidgets.QLabel("選擇計畫")
        self.jobs_combo = QtWidgets.QComboBox()
        self.jobs_combo.setFixedWidth(150)
        self.proj_remove_button = QtWidgets.QPushButton("刪除選定計畫")


        box = QtWidgets.QHBoxLayout()
        box.addWidget(add_projectnum)
        box.addWidget(self.proj_year_input)
        box.addWidget(dash)
        box.addWidget(self.proj_No_input)
        box.addWidget(self.add_proj_button)
        box.addWidget(select_proj_l)
        box.addWidget(self.jobs_combo)
        box.addWidget(self.proj_remove_button)

        self.add_proj_button.clicked.connect(self.add_project_number)
        self.proj_remove_button.clicked.connect(self.remove_project_number)

        return box

    def add_project_number(self):
        project_num = self.proj_year_input.text().strip()+ '-' + self.proj_No_input.text().strip()
        self.projectnumber_list.append(project_num)
        self.jobs_combo.addItem(project_num)

    def remove_project_number(self):
        project_num = self.jobs_combo.currentText()
        if project_num == "":
            return
        remove_no = self.projectnumber_list.index(project_num)
        self.jobs_combo.removeItem(remove_no)
        self.projectnumber_list.remove(project_num)

#####################################################################################################
    def date_block(self):
        self.year_input = QtWidgets.QLineEdit()
        year = QtWidgets.QLabel("年")
        self.month_input = QtWidgets.QComboBox()
        month_list =  [str(mon) for mon in range(1,13)]
        self.month_input.addItems(month_list)
        month_l = QtWidgets.QLabel("月")
        self.date_confirm_button = QtWidgets.QPushButton("確定")

        self.datebox = QtWidgets.QHBoxLayout()
        self.datebox.addWidget(self.year_input)
        self.datebox.addWidget(year)
        self.datebox.addWidget(self.month_input)
        self.datebox.addWidget(month_l)
        self.datebox.addWidget(self.date_confirm_button)


        self.day_combo = QtWidgets.QComboBox()
        day_l = QtWidgets.QLabel("日")
        self.remove_day_button = QtWidgets.QPushButton("清除選定日")
        self.datebox.addWidget(self.day_combo)
        self.datebox.addWidget(day_l)
        self.datebox.addWidget(self.remove_day_button)


        self.date_confirm_button.clicked.connect(self.define_workday)
        self.remove_day_button.clicked.connect(self.remove_select_day)

        return self.datebox



    def define_workday(self):
        year  = self.year_input.text()
        if year.isdigit() == False:
            return
        month = self.month_input.currentText()
        date = calendar.monthcalendar((int(year)+1911),int(month))
        workday = set()
        for everyweek in date:
             del everyweek[-1]
             del everyweek[-1]
             for day in everyweek:
                 workday.add(day)
        workday.remove(0)
        self.workday = [str(x) for x in list(sorted(workday))]
        self.day_combo.clear()
        self.day_combo.addItems(self.workday)


    def remove_select_day(self):
        select_day = self.day_combo.currentText()
        if select_day == "":
            return
        remove_no = self.workday.index(select_day)
        self.workday.remove(select_day)
        self.day_combo.removeItem(remove_no)


#####################################################################################################



    def routine_block(self):
        routine_l = QtWidgets.QLabel("添加工作事項")
        self.routine_input = QtWidgets.QLineEdit()

        self.routine_confirm_button = QtWidgets.QPushButton("添加")

        wk_hr_l = QtWidgets.QLabel("時數")
        self.wk_hr_input = QtWidgets.QLineEdit()
        self.wk_hr_input.setFixedWidth(30)

        added_routine_l = QtWidgets.QLabel("已添加事項")
        self.routine_combo = QtWidgets.QComboBox()
        self.routine_combo.setFixedWidth(150)
        self.routine_remove_button = QtWidgets.QPushButton("刪除事項")


        box = QtWidgets.QHBoxLayout()
        box.addWidget(routine_l)
        box.addWidget(self.routine_input)
        box.addWidget(self.routine_confirm_button)
        box.addWidget(wk_hr_l)
        box.addWidget(self.wk_hr_input)
        box.addWidget(added_routine_l)
        box.addWidget(self.routine_combo)
        box.addWidget(self.routine_remove_button)

        self.routine_confirm_button.clicked.connect(self.add_workroutine)
        self.routine_remove_button.clicked.connect(self.remove_workroutine)
        return box


    def add_workroutine(self):
        routine = self.routine_input.text()
        self.routine.append(routine)
        self.routine_combo.addItem(routine)



    def remove_workroutine(self):
        routine = self.routine_combo.currentText()
        if routine == "":
            return
        remove_no = self.routine.index(routine)
        self.routine.remove(routine)
        self.routine_combo.removeItem(remove_no)


##################################################################################################################

    def Console_block(self):
        self.text = QtWidgets.QPlainTextEdit()
        self.text.setStyleSheet(
            """QPlainTextEdit {background-color: #333;
                               color: #00FF00;
                               font-family: Courier;}""")
        self.text.document().setPlainText("Welcome to CCU Auto fill workroutine System !\n"
                                          "---------------------------------------------------------------------------------")
        self.text.setReadOnly(True)
        box = QtWidgets.QHBoxLayout()
        box.addWidget(self.text)
        return box

    def update_Console(self,message):
        self.text.appendPlainText(message)
        self.text.update()



####################################################################################################################


    def run_block(self):
        self.run_button = QtWidgets.QPushButton("執行")
        self.run_button.clicked.connect(self.login_click)
        return self.run_button

    def login_click(self):
        self.run_button.setEnabled(False)
        self.username = self.user_input.text()
        self.password = self.pass_input.text()
        job = self.job_combo.currentText()
        self.jobnum = "'"+str(self.job_list.index(job) + 1)+"'"
        myThread = threading.Thread(target=self.DataSave)
        myThread.start()
        self.driver_start()




    def driver_start(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('https://miswww1.ccu.edu.tw/pt_proj/index.php')
        self.driver.set_page_load_timeout(50)
        self.driver.implicitly_wait(30)
        self.login_action(self.username,self.password,self.jobnum)
        self.solve_popup_window()
        myThread = threading.Thread(target=self.write_routine)
        myThread.start()

    def solve_popup_window(self):
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except UnexpectedAlertPresentException:
            pass
        except NoAlertPresentException:
            pass
        except Exception:
            pass

    def login_action(self,username,password,select_job):
        self.driver.find_element_by_name("staff_cd").send_keys(username)
        self.driver.find_element_by_name("passwd").send_keys(password)
        self.driver.find_element_by_xpath(("//select[@name='proj_type']/option[@value=%s]") % select_job).click()
        self.driver.find_element_by_xpath("/html/body/center/form/input[1]").click()
        self.mythread = MyThread("已進入工作日誌系統")
        self.mythread.signal.connect(self.update_Console)
        self.mythread.start()
        time.sleep(2)


    def write_routine(self):
         s = 0
         for eachday in self.workday:
            self.driver.get("https://miswww1.ccu.edu.tw/pt_proj/main2.php")
            self.driver.find_element_by_xpath(("//select[@name='type']/option[@value=%s]") % ("'"+self.jobs_combo.currentText()+"'")).click()

            y = self.driver.find_element_by_name('yy')
            y.send_keys(Keys.BACK_SPACE * 5)
            y.send_keys(self.year_input.text())

            m = self.driver.find_element_by_name('mm')
            m.send_keys(Keys.BACK_SPACE * 5)
            m.send_keys(self.month_input.currentText())

            d = self.driver.find_element_by_name('dd')
            d.send_keys(Keys.BACK_SPACE * 5)
            d.send_keys(eachday)

            self.driver.find_element_by_name('hrs').send_keys(self.wk_hr_input.text())
            #   self.driver.find_element_by_name('workin').send_keys(random.choice(workroutine))                    #隨機填入工作內容
            self.driver.find_element_by_name('workin').send_keys(self.routine[s % len(self.routine)])  # 依序填入工作內容
            self.driver.find_element_by_xpath("/html/body/form/center/input[1]").click()
            s += 1
            mythread = MyThread('以輸入'+self.year_input.text()+' 年 '+self.month_input.currentText()+' 月 '+eachday+'日 工作'+ self.wk_hr_input.text()+'小時')
            mythread.signal.connect(self.update_Console)
            mythread.start()
         else:
             time.sleep(2)
             self.driver.get("https://miswww1.ccu.edu.tw/pt_proj/main2.php")
             mythread = MyThread("---------------------------------------------------------------------------------\n"
                                 "全數輸入完畢")
             mythread.signal.connect(self.update_Console)
             mythread.start()
             time.sleep(3)
             self.driver.find_element_by_xpath("/html/body/form/center/input[2]").click()
             mythread2 = MyThread("---------------------------------------------------------------------------------\n"
                                  '將產生批號')
             mythread2.signal.connect(self.update_Console)
             mythread2.start()

             self.driver.find_element_by_xpath("/html/body/center[2]/input").click()
             self.solve_popup_window()
             self.driver.get("https://miswww1.ccu.edu.tw/pt_proj/print_sel.php")
             self.driver.find_element_by_xpath(
                 ("//select[@name='unit_cd1']/option[@value=%s]") % ("'" + self.jobs_combo.currentText() + "'")).click()
             self.driver.find_element_by_xpath("/html/body/form/center/input[1]").click()
             self.driver.find_element_by_xpath("/html/body/center/form/table/tbody/tr[1]/th[1]/input").click()
             self.driver.find_element_by_xpath("/html/body/center/form/input[1]").click()
             self.driver.find_element_by_xpath("/html/body/center/input").click()
             mythread3 = MyThread("---------------------------------------------------------------------------------\n"
                                  '以產生批號 感謝使用！！')
             mythread3.signal.connect(self.update_Console)
             mythread3.start()
             self.run_button.setEnabled(True)
             time.sleep(5)
             self.driver.close()

    def DataSave(self):
        with open("config.json",'w') as json_dump:
            self.config["username"] = self.username
            self.config["password"] = self.password
            self.config["job"] = self.job_combo.currentText()
            self.config["jobnum"] = self.jobnum
            self.config["project"] = self.projectnumber_list
            self.config["routine"] = self.routine
            self.config["workhour"] = self.wk_hr_input.text()
            json.dump(self.config,json_dump)




class MyThread(QThread):
    signal = pyqtSignal(str)
    def __init__(self,text):
        super(MyThread, self).__init__()
        self.text = text

    def run(self):
        self.signal.emit(self.text)
        self.deleteLater()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run = window()
    run.show()
    sys.exit(app.exec_())
