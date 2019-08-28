from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from fpdf import FPDF
from PIL import Image
import sys, UI
import pyautogui
import os
import subprocess

def makePdf(pdfFileName, listPages, dir):
    if (dir):
        dir += "/"

    cover = Image.open(dir + str(listPages[0]))
    width, height = cover.size

    pdf = FPDF(unit="pt", format=[width, height])

    for page in listPages:
        pdf.add_page()
        pdf.image(dir + str(page), 0, 0)

    x = [f for f in os.listdir(dir) if f.endswith(".pdf")]
    x.append('')

    for i in range(len(x)):
        if x[i] == '':
            pdf.output(dir + pdfFileName + "{}.pdf".format(str(i)), "F")
            break


####UI-------------------------------------------------------------------------

class MyWindow(QMainWindow, UI.Ui_MainWindow):  #UI.Ui_MainWindow
   ###이벤트 루프 -------------------------------------------------------------
    def __init__(self):
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        super().__init__()
        self.setupUi(self)

        self.setOpen_Button.clicked.connect(self.set_open_clicked)
        self.path_Button.clicked.connect(self.pt_btn_clicked)
        self.position_Button.clicked.connect(self.po_btn_clicked)
        self.jpgCap_Button.clicked.connect(self.jpg_cap_btn_clicked)
        self.pdfCap_Button.clicked.connect(self.pdf_cap_btn_clicked)
        self.cancle_Button.clicked.connect(self.exit_btn_clicked)
        self.folderOpen_Button.clicked.connect(self.folder_open_clicked)
        self.clear_Button.clicked.connect(self.clr_btn_clicked)
        #self.save_Button.clicked.connect(self.save_clicked)

        self.statusBar().showMessage('Ready')

        #setOpen_Button 전역변수 할당
        self.resize(290, 455)
        global default
        default = self.size()



   ###구현 중인 함수 ---------------------------------------------------------

    def save_clicked(self):
        global chkSet
        chkSet = self.checkBox_lastSet.isChecked()
        global clrSet
        clrSet = self.checkBox_endClr.isChecked()

        setName = ["lesson", "work_dir[0]","position[0]","position[3]","chkSet","clrSet" ]
        setValue = [self.lesson, self.work_dir[0], self.position[0], self.position[3], chkSet, clrSet]
                    #교시, 사진저장경로, 시작위치,      끝위치,     설정,  내역지우기

        f = open("setting.txt","w")
        for i in range(len(setValue)):
            f.write(setName +"="+str(setValue))

        self.textBrowser_output.append("★설정 저장 완료★")

    ##수정 버튼 ------------------------------------------------------------
    def set_open_clicked(self):
        if self.size() == default:
            self.resize(560, 455)
            self.setOpen_Button.setText("설정◀")
        else:
            self.resize(290, 455)
            self.setOpen_Button.setText("설정▶")

    def pt_btn_clicked(self):
        global work_dir
        work_dir = self.selPath()                   # workingPath, path, length

    def po_btn_clicked(self):
        global position
        position = self.selPosition()               # sPoint, rel_x, rel_y

    ##언더라인 버튼 --------------------------------------------------------
    def jpg_cap_btn_clicked(self):
        self.statusBar().showMessage('Processing...')

        global lesson
        lesson = self.lineEdit_lctr.text()

        if lesson == '0':
            self.textBrowser_output.append("-몇교시인지 입력되지 않았습니다.")
        elif self.l_dir_show.text() == "":
            self.textBrowser_output.append("-경로가 지정되지 않았습니다.")
        elif self.l_sPoint_show.text() == "":
            self.textBrowser_output.append("-좌표가 지정되지 않았습니다.")
        else:
            self.textBrowser_output.append("★캡쳐영역 설정 완료★")
            self.textBrowser_output.append("★" + str(lesson) + "교시로 설정 완료★")
            self.textBrowser_output.append("")

            sPoint = position[0]
            rel_x = position[1]
            rel_y = position[2]
            workingPath = work_dir[0]

            self.jpgCapture(lesson, sPoint, rel_x, rel_y, workingPath)

        if self.checkBox_endClr.isChecked():
            self.textBrowser_output.clear()

    def pdf_cap_btn_clicked(self):
        self.statusBar().showMessage('Processing...')

        global lesson
        lesson = self.lineEdit_lctr.text()

        if lesson == '0':
            self.textBrowser_output.append("-몇교시인지 입력되지 않았습니다.")
        elif self.l_dir_show.text() == "":
            self.textBrowser_output.append("-경로가 지정되지 않았습니다.")
        elif self.l_sPoint_show.text() == "":
            self.textBrowser_output.append("-좌표가 지정되지 않았습니다.")
        else:
            self.textBrowser_output.append("★캡쳐영역 설정 완료★")
            self.textBrowser_output.append("★" + str(lesson) + "교시로 설정 완료★")
            self.textBrowser_output.append("")

            sPoint = position[0]
            rel_x = position[1]
            rel_y = position[2]
            workingPath = work_dir[0]

            self.pdfCapture(lesson, sPoint, rel_x, rel_y, workingPath)

    def exit_btn_clicked(self):
        sys.exit()

    def folder_open_clicked(self):
        if self.l_dir_show.text() == "":
            self.textBrowser_output.append("-경로가 지정되지 않았습니다.")
        else:
            subprocess.Popen('explorer /open, {args}'.format(args = work_dir[0].replace('/','\\')))

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


        return sPoint, rel_x, rel_y, ePoint

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

    def jpgCapture(self, lesson, sPoint, rel_x, rel_y, workingPath):
         for i in range(int(lesson)):                                               ##설정한 교시만큼 반복
            imgName=1
            os.chdir(workingPath)                                                    #원래 경로로 복귀
            if not os.path.exists(str(i+1)+'교시'):                                  #폴더 확인 및 생성
                os.mkdir(str(i+1)+'교시')
            os.chdir(workingPath+'/'+str(i+1)+'교시')                                #저장할 폴더 경로 생성 및 지정

            self.textBrowser_output.append("▶현재 캡쳐 : " + str(i+1) + "교시")

            while True:                                                             ##설정된 교시 내 캡쳐 반복
                ok = QMessageBox.question(self, '캡쳐 중', "Yes = 다음 교시로 이동 \nNo = 현재 페이지 캡쳐 \nCancel = 방금 캡쳐 삭제",
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

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
                elif ok == QMessageBox.No:
                    if imgName < 10:
                        im3 = pyautogui.screenshot('0'+str(imgName)+'.jpg', region=(sPoint[0], sPoint[1],rel_x, rel_y))
                    else:
                        im3 = pyautogui.screenshot(str(imgName) + '.jpg', region=(sPoint[0], sPoint[1], rel_x, rel_y))
                    self.textBrowser_output.append("   " + str(imgName) + "페이지 저장 완료")
                    imgName += 1
                else:
                    try:
                        if imgName < 11:
                            os.remove('0' + str(imgName - 1) + '.jpg')
                        else:
                            os.remove(str(imgName - 1) + '.jpg')
                        self.textBrowser_output.append("   " + str(imgName - 1) + "페이지 삭제")
                        imgName -= 1
                    except:
                        self.textBrowser_output.append("-삭제할 이미지가 없습니다.")
                        pass

    def pdfCapture(self, lesson, sPoint, rel_x, rel_y, workingPath):
        os.chdir(workingPath)  # 원래 경로로 복귀
        if not os.path.exists('imgTemp'):  # 폴더 확인 및 생성
            os.mkdir('imgTemp')
        setPath = str(workingPath + '/' + 'imgTemp')
        os.chdir(setPath)  # 저장할 폴더 경로 생성 및 지정

        imgName = 1
        try:
            x = [f for f in os.listdir(setPath) if f.endswith(".jpg")]
            imgName = len(x)+1
        except:
            pass

        for i in range(int(lesson)):  ##설정한 교시만큼 반복
            self.textBrowser_output.append("▶현재 캡쳐 : " + str(i + 1) + "교시")
            viewValue = 1

            while True:  ##설정된 교시 내 캡쳐 반복
                ok = QMessageBox.question(self, '캡쳐 중', "Yes = 다음 교시로 이동 \nNo = 현재 페이지 캡쳐 \nCancel = 방금 캡쳐 삭제",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

                if ok == QMessageBox.Yes:
                    if (i + 1) == int(lesson):  # 입력 외의 교시때 종료
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("●●●캡쳐 종료●●●")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.statusBar().showMessage('Ready')
                        break
                    else:
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("▶" + str(i + 2) + "교시로 이동")
                        self.textBrowser_output.append("")

                        break
                elif ok == QMessageBox.No:
                    if imgName < 10:
                        im3 = pyautogui.screenshot('0' + str(imgName) + '.jpg',
                                                   region=(sPoint[0], sPoint[1], rel_x, rel_y))
                    else:
                        im3 = pyautogui.screenshot(str(imgName) + '.jpg', region=(sPoint[0], sPoint[1], rel_x, rel_y))
                    self.textBrowser_output.append("   " + str(imgName) + "({})페이지 저장 완료".format(viewValue))
                    imgName += 1
                    viewValue += 1
                else:
                    try:
                        if imgName < 11:
                            os.remove('0' + str(imgName - 1) + '.jpg')
                        else:
                            os.remove(str(imgName - 1) + '.jpg')
                        self.textBrowser_output.append("   " + str(imgName - 1) + "페이지 삭제")
                        imgName -= 1
                        viewValue -= 1
                    except:
                        self.textBrowser_output.append("-삭제할 이미지가 없습니다.")
                        pass

        try:
            #PDF생성 및 원본 삭제
            x = [f for f in os.listdir(setPath) if f.endswith(".jpg")]
            makePdf("file", x, setPath)

            for i in range(len(x)):
                os.remove(x[i])

            os.chdir(workingPath)

            if self.checkBox_endClr.isChecked():
                self.textBrowser_output.clear()

            self.textBrowser_output.append("★PDF 생성 완료★")
        except:
            if self.checkBox_endClr.isChecked():
                self.textBrowser_output.clear()

            self.textBrowser_output.append("-사용할 이미지가 없습니다.")
            pass

###메인 함수
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

'''
----------------------------------------------------------------------------
[2]기존 진행하던 캡쳐가 있을 시, 자동으로 캡쳐 '이어서 하기' 기능 추가
    (덮어쓰기 방지기능, 캡쳐한 파일 이후 이어서 이미지 생성)
    try except, 

[3]사용관련 버그 수정
   -마지막 캡쳐 지우기 버그 수정
   -이미지가 없을 시, PDF생성 안되는 버그 수정
'''