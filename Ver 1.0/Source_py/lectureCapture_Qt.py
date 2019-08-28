from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pynput import mouse
import sys, UI
import time
import pyautogui
import os
import subprocess


class MyWindow(QMainWindow, UI.Ui_MainWindow):
   ###이벤트 루프 -------------------------------------------------------------
    def __init__(self):
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        super().__init__()
        self.setupUi(self)
        #actionExit_1.triggered.connect(qApp.quit)
        
        self.path_Button.clicked.connect(self.pt_btn_clicked)
        self.position_Button.clicked.connect(self.Po_btn_clicked)
        self.capture_Button.clicked.connect(self.cap_btn_clicked)
        self.cancle_Button.clicked.connect(self.exit_btn_clicked)
        self.clear_Button.clicked.connect(self.clr_btn_clicked)
        
        self.statusBar().showMessage('Ready')

   ###(슬롯)콜백 함수 ---------------------------------------------------------
    def slot_view(self):
        #To-do : 경로가 하나 상위, 폴더로 출력됨
        subprocess.Popen(r'explorer /select, {args}'.format(args = work_dir[0].replace('/','\\')))
        
    ##수정 버튼 ------------------------------------------------------------
    def pt_btn_clicked(self):
        global work_dir
        work_dir = self.selPath()                   # workingPath, path, length

    def Po_btn_clicked(self):
        global position
        position = self.selPosition()               # sPoint, rel_x, rel_y

    ##언더라인 버튼 --------------------------------------------------------
    def cap_btn_clicked(self):
        self.statusBar().showMessage('Processing...')

        global lesson
        lesson = self.lineEdit_lctr.text()

        if lesson == '0':
            self.textBrowser_output.append("-몇교시인지 입력되지 않았습니다.")
        else:
            self.textBrowser_output.append("★캡쳐영역 설정 완료★")
            self.textBrowser_output.append("★" + str(lesson) + "교시로 설정 완료★")
            self.textBrowser_output.append("")

        sPoint = position[0]
        rel_x = position[1]
        rel_y = position[2]
        workingPath = work_dir[0]

        self.capture(lesson, sPoint, rel_x, rel_y, workingPath)
        
        
    def exit_btn_clicked(self):
        sys.exit()
        

    def clr_btn_clicked(self):
        self.textBrowser_output.clear()
        
   ###기능 함수 --------------------------------------------------------------
    def selPosition(self):
        ok = QMessageBox.question(self, '시작 지정', '캡쳐할 시작 위치에 마우스를 가져다놓고 엔터를 눌러주세요.',
                                     QMessageBox.Yes)
        if ok:
            sPoint = pyautogui.position()
            self.l_sPoint_show.setText(str(sPoint))

        self.textBrowser_output.append("★시작 위치 설정 완료★")
            
        ok = QMessageBox.question(self, '끝 지정', '캡쳐할 끝 위치에 마우스를 가져다놓고 엔터를 눌러주세요.',
                                     QMessageBox.Yes)
        if ok:
            ePoint = pyautogui.position()
            self.l_ePoint_show.setText(str(ePoint))

        self.textBrowser_output.append("★끝 위치 설정 완료★")
        
        rel_x = ePoint[0]-sPoint[0]     # x의 상대값 저장
        rel_y = ePoint[1]-sPoint[1]     # y의 상대값 저장

        
        return sPoint, rel_x, rel_y


    def selPath(self):
        workingPath = QFileDialog.getExistingDirectory(self, '저장할 경로 지정', options=QFileDialog.ShowDirsOnly)
        path = str(workingPath).split("/")
        length = len(path)

        if path[length-2] == "C:" :
            showPath = str(path[length-2]+"/"+path[length-1])
        else:
            showPath = str("/"+path[length-2]+"/"+path[length-1])
        
        self.l_dir_show.setText(showPath)
        self.textBrowser_output.append("★경로 설정 완료★")
        
        return workingPath, path, length


    def capture(self, lesson, sPoint, rel_x, rel_y, workingPath):
         for i in range(int(lesson)):                                               ##설정한 교시만큼 반복
            imgName=1
            os.chdir(workingPath)                                                    #원래 경로로 복귀
            if not os.path.exists(str(i+1)+'교시'):                                  #폴더 확인 및 생성
                os.mkdir(str(i+1)+'교시')
            os.chdir(workingPath+'/'+str(i+1)+'교시')                                #저장할 폴더 경로 생성 및 지정
            
            self.textBrowser_output.append("▶현재 캡쳐 : " + str(i+1) + "교시")
            
            while True:                                                             ##설정된 교시 내 캡쳐 반복
                ok = QMessageBox.question(self, '캡쳐 중', 'Yes = 다음 교시로 이동, No = 현재 페이지 캡쳐',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if ok == QMessageBox.Yes:
                    if (i+1) == int(lesson) :                                        #입력 외의 교시때 종료
                        os.chdir(workingPath)                                        #폴더삭제시, 사용중 방지
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("●●●캡쳐 종료●●●")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.statusBar().showMessage('Ready')
                        break
                    else:
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("▶" + str(i+2) + "교시로 이동")
                        self.textBrowser_output.append("")

                        imgName=1
                        break
                else:
                    im3 = pyautogui.screenshot(str(imgName)+'.jpg', region=(sPoint[0], sPoint[1],rel_x, rel_y))
                    self.textBrowser_output.append("   " + str(imgName) + "페이지 저장 완료")
                    imgName += 1
            
###메인 함수
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
