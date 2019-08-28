"""
   캡쳐 지정 프로그램
최종 수정 - 2019.07.02
"""
import sys  # 실행, 종료

from PyQt5.QtWidgets import *  # Qt 위젯 관리
from configparser import ConfigParser  # 설정 파일 생성, 읽기, 삭제

from PyQt5.QtCore import *  # Qt 윈도우 관리
from subprocess import Popen  # 윈도우 프로그램 실행

import cap_module
import UI


# UI----------------------------------------------------------------------------
class MyWindow(QMainWindow, UI.Ui_MainWindow):
    # 이벤트 루프 ---------------------------------------------------------------
    def __init__(self):
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.setOpen_Button.clicked.connect(self.set_open_clicked)
        self.path_Button.clicked.connect(self.pt_btn_clicked)
        self.position_Button.clicked.connect(self.po_btn_clicked)
        self.jpgCap_Button.clicked.connect(self.jpg_cap_btn_clicked)
        self.pdfCap_Button.clicked.connect(self.pdf_cap_btn_clicked)
        self.cancle_Button.clicked.connect(self.exit_btn_clicked)
        self.folderOpen_Button.clicked.connect(self.folder_open_clicked)
        self.clear_Button.clicked.connect(self.clr_btn_clicked)
        self.saveSet_Button.clicked.connect(self.save_clicked)
        self.lstDel_Button.clicked.connect(self.list_delete_clicked)
        self.loadSet_Button.clicked.connect(self.load_settings_clicked)
        self.reset_Button.clicked.connect(self.reset_btn_clicked)
        self.statusBar().showMessage("Ready")

        # 설정 목록 불러오기
        global config
        config = ConfigParser()
        config.read('setting.ini')
        self.comboBox_loadSet.addItems(config.sections())

        # 기본 창 사이즈 세팅
        global default
        self.resize(290, 455)
        default = self.size()

        # PDF Name 여부 정의
        global pdf_name_bool
        pdf_name_bool = False

    # 설정 버튼 --------------------------------------------------------------
    def reset_btn_clicked(self):
        try:
            global lesson
            lesson = None

            global work_dir
            work_dir[0] = None

            global coordinate
            coordinate = None

            self.lineEdit_lctr.setText("0")
            self.l_dir_show.setText("")
            self.l_sPoint_show.setText("")
            self.l_ePoint_show.setText("")
            self.textBrowser_output.clear()
            self.checkBox_lastChk.setChecked(False)
            self.checkBox_openSet.setChecked(False)
            self.checkBox_endClr.setChecked(True)
        except Exception:
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-초기 상태입니다.")

    # 수정 버튼 -------------------------------------------------------------
    # 경로 버튼
    def pt_btn_clicked(self):
        global work_dir
        work_dir = cap_module.Setting.sel_path(self)  # workingPath, path, length

    # 좌표 버튼
    def po_btn_clicked(self):
        global coordinate
        coordinate = cap_module.Setting.sel_coordinate(self)  # sPoint, rel_x, rel_y

    # 설정 버튼
    def set_open_clicked(self):
        if self.size() == default:
            self.resize(560, 455)
            self.setOpen_Button.setText("설정◀")
        else:
            self.resize(290, 455)
            self.setOpen_Button.setText("설정▶")

    # 언더라인 버튼 --------------------------------------------------------
    # JPG 캡쳐
    def jpg_cap_btn_clicked(self):
        self.statusBar().showMessage("Processing...")

        bln = cap_module.Capture.cap_check(self)
        if bln:
            global lesson
            lesson = self.lineEdit_lctr.text()
            s_point = coordinate[0]
            rel_x = coordinate[1]
            rel_y = coordinate[2]
            working_path = work_dir[0]

            cap_module.Capture.jpg_capture(self, lesson, s_point, rel_x, rel_y, working_path)

            if self.checkBox_endClr.isChecked():
                self.textBrowser_output.clear()

        self.statusBar().showMessage("Ready")

    # 캡쳐 후 PDF 생성
    def pdf_cap_btn_clicked(self):
        self.statusBar().showMessage("Processing...")

        bln = cap_module.Capture.cap_check(self)
        if bln:
            global lesson
            lesson = self.lineEdit_lctr.text()
            s_point = coordinate[0]
            rel_x = coordinate[1]
            rel_y = coordinate[2]
            working_path = work_dir[0]

            if not pdf_name_bool:
                global pdf_name
                pdf_name = "file"

            cap_module.Capture.pdf_capture(self, lesson, s_point, rel_x, rel_y, working_path, pdf_name)

        self.statusBar().showMessage("Ready")

    # 종료 버튼
    def exit_btn_clicked(self):
        sys.exit()

    # 폴더 오픈 버튼
    def folder_open_clicked(self):
        if self.l_dir_show.text() == "":
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-경로가 지정되지 않았습니다.")
        else:
            Popen('explorer /open, {args}'.format(args=work_dir[0].replace('/', '\\')))

    # 내역지우기 버튼
    def clr_btn_clicked(self):
        self.textBrowser_output.clear()

    # 설정 버튼 --------------------------------------------------------------
    # 설정 저장 버튼
    def save_clicked(self):
        global set_name
        global chkSet
        chkSet = self.checkBox_lastChk.isChecked()
        global openSet
        openSet = self.checkBox_openSet.isChecked()
        global clrSet
        clrSet = self.checkBox_endClr.isChecked()

        # 설정 정보들이 있는지 확인
        try:
            set_name = ["lesson", "work_dir[0]", "coordinate[0]", "coordinate[3]", "chkSet", "openSet", "clrSet"]
            set_value = [self.lineEdit_lctr.text(), work_dir[0], coordinate[0], coordinate[3], chkSet, openSet, clrSet]
            #                    교시,             사진저장경로,   시작위치,       끝위치,      설정,  열기,  내역지우기
            file_bool = True
        except Exception:
            set_value = ''
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-저장할 설정 정보가 없습니다.")
            file_bool = False

        # 설정 정보들에 따라 실행
        if file_bool:
            try:
                # 파일 존재 확인용 오픈
                f = open("setting.ini", "r")
                f.close()
                # 파일 추가를 위한 오픈
                f = open("setting.ini", "a")
            except Exception:
                # 파일 없을 시, 생성
                f = open("setting.ini", "w")

            if not self.lineEdit_saveName.text() == '':
                # 중복 이름 체크
                chk = open("setting.ini", "r")
                line = chk.readlines()
                save_name = self.lineEdit_saveName.text()
                overlap = True

                for i in range(len(line)):
                    if line[i] == str('[' + save_name + ']\n'):
                        overlap = False
                        break

                if overlap:
                    # 파일 쓰기
                    section_name = self.lineEdit_saveName.text()
                    f.write('[{}]\n'.format(section_name))

                    for i in range(len(set_value)):
                        f.write(str(set_name[i]) + '=' + str(set_value[i]) + '\n')
                    f.write('\n')

                    f.close()

                    # 리스트 새로고침
                    cap_module.Config.config_list_refresh(self)

                    self.textBrowser_output.clear()
                    self.textBrowser_output.append("★설정 저장 완료★")
                else:
                    self.textBrowser_output.clear()
                    self.textBrowser_output.append("-다른 이름을 정해주세요.")
            else:
                self.textBrowser_output.clear()
                self.textBrowser_output.append("-설정의 이름을 정해주세요.")

    # 설정 불러오기
    def load_settings_clicked(self):
        try:
            # setLesson, setWork_dir0, setCoordinate0, setCoordinate3, setChkset, setOpenset setClrset
            key_value = cap_module.Config.load_setting(self, config)

            # setLesson
            global lesson
            lesson = key_value[0]
            self.lineEdit_lctr.setText(lesson)

            # setWork_dir0
            global work_dir
            work_dir = ['', '', '']
            work_dir[0] = key_value[1]
            path = str(work_dir[0]).split("/")
            length = len(path)

            if path[length - 2] == "C:":
                show_path = str(path[length - 2] + "/" + path[length - 1])
            else:
                show_path = str("/" + path[length - 2] + "/" + path[length - 1])
            self.l_dir_show.setText(show_path)

            # setCoordinate0
            global coordinate
            coordinate = ['', '', '', '']
            coordinate[0] = key_value[2]
            self.l_sPoint_show.setText("Point" + str(coordinate[0]))

            # setCoordinate3
            coordinate[3] = key_value[3]
            self.l_ePoint_show.setText("Point" + str(coordinate[3]))

            # setCoordinate3 - setCoordinate0
            coordinate[1] = int(key_value[3][0]) - int(key_value[2][0])  # x의 상대값 저장
            coordinate[2] = int(key_value[3][1]) - int(key_value[2][1])  # y의 상대값 저장

            # setChkset
            chk_set = key_value[4]
            cap_module.Setting.check_set_check(self, chk_set)

            # setOpenset
            open_set = key_value[5]
            cap_module.Setting.check_set_check(self, open_set)

            # setClrset
            clr_set = key_value[6]
            cap_module.Setting.check_set_check(self, clr_set)

            # pdfFileName
            global pdf_name
            pdf_name = self.comboBox_loadSet.currentText()

            global pdf_name_bool
            pdf_name_bool = True

        except Exception:
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-불러올 설정이 없습니다.")

    # 설정 지우기
    def list_delete_clicked(self):
        try:
            section = self.comboBox_loadSet.currentText()
            f = open("setting.ini", "r")
            line = f.readlines()
            start_p = 0

            # 섹션 찾기
            for i in range(len(line)):
                if line[i] == str('[' + section + ']\n'):
                    start_p = i
                    break
            # 섹션 지우기
            for i in range(9):
                line[i + start_p] = ''
            # 수정된 텍스트 새로 쓰기
            f = open("setting.ini", "w")
            for i in range(len(line)):
                f.write(line[i])

            f.close()

            # 리스트 새로고침
            cap_module.Config.config_list_refresh(self)

            self.textBrowser_output.append("-\"" + section + "\"을 삭제했습니다.")
        except Exception:
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-지울 설정이 없습니다.")


# 메인 함수
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

'''
----------------------------------------------------------------------------
# 아무것도 없는 0번째때, 범위가 0이어서 for문 실행x -> +1 해줌으로써 0번째 ~ 실행
        try:
            x = [f for f in os.listdir(str(os.getcwd())) if f.endswith(".ini")]
            for i in range(len(x) + 1):
                open("setting" + str(i) + ".ini", "r")
        except:
            f = open("setting" + str(i) + ".ini", "w")
###구현 중인 함수 ---------------------------------------------------------
        #checkBox_lastChk 구현하기

        # setOpen_Button 전역변수 할당
        if self.checkBox_openSet.isChecked():
            self.resize(560, 455)
            self.setOpen_Button.setText("설정◀")
        else:
            self.resize(290, 455)
            self.setOpen_Button.setText("설정▶")
        global default
        default = self.size()
'''
