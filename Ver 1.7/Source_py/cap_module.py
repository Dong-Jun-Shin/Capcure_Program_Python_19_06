"""
   캡쳐 지정을 위한 모듈
  최종 수정 - 2019.07.02
"""

import os  # 파일, 경로

from PyQt5.QtWidgets import *  # Qt 위젯 관리
from configparser import ConfigParser  # 설정 파일 생성, 읽기, 삭제

from pyautogui import screenshot, position  # 화면 관리

from fpdf import FPDF  # PDF 생성, 합치기
from PIL import Image  # 이미지 관리


class Setting:
    # 경로 지정하기
    def sel_path(self):
        working_path = QFileDialog.getExistingDirectory(self, '저장할 경로 지정', options=QFileDialog.ShowDirsOnly)
        path = str(working_path).split("/")
        length = len(path)

        if path[length - 2] == "C:":
            show_path = str(path[length - 2] + "/" + path[length - 1])
        else:
            show_path = str("/" + path[length - 2] + "/" + path[length - 1])

        self.l_dir_show.setText(show_path)
        self.textBrowser_output.clear()
        self.textBrowser_output.append("★경로 설정 완료★")

        return [working_path, path, length]

    # 좌표 구하기
    def sel_coordinate(self):
        self.textBrowser_output.clear()
        ok = QMessageBox.question(self, '시작 지정', '캡쳐할 시작 위치에 마우스를 가져다놓고 엔터를 눌러주세요.',
                                  QMessageBox.Yes)
        if ok:
            s_point = position()
            self.l_sPoint_show.setText(str(s_point))

        self.textBrowser_output.append("★시작 위치 설정 완료★")

        ok = QMessageBox.question(self, '끝 지정', '캡쳐할 끝 위치에 마우스를 가져다놓고 엔터를 눌러주세요.',
                                  QMessageBox.Yes)
        if ok:
            e_point = position()
            self.l_ePoint_show.setText(str(e_point))

        self.textBrowser_output.append("★끝 위치 설정 완료★")

        rel_x = e_point[0] - s_point[0]  # x의 상대값 저장
        rel_y = e_point[1] - s_point[1]  # y의 상대값 저장

        return [s_point, rel_x, rel_y, e_point]

    # 체크박스 설정
    def check_set_check(self, check_var):
        if check_var == 'True':
            check_var = True
        else:
            check_var = False
        self.checkBox_endClr.setChecked(check_var)


class CoordinateExtract:
    # 좌표 구하기
    def coordinate_extract(self, list_var, crd_value, s_str, e_str):
        start_str = None
        end_str = None
        for i in range(len(crd_value)):
            if crd_value[i] == s_str:
                start_str = i
            if crd_value[i] == e_str:
                end_str = i
        self.list_var = list_var
        self.list_var.append(crd_value[(start_str + 2):end_str])

    # 불러온 설정으로 다시 x좌표 구할때
    def coordinate_re_extract_x(self, list_var, crd_value, s_str, e_str):
        start_str = None
        end_str = None
        for i in range(len(crd_value)):
            if crd_value[i] == s_str:
                start_str = i
            if crd_value[i] == e_str:
                end_str = i
        self.list_var = list_var
        self.list_var.append(crd_value[(start_str + 2):(end_str - 1)])

    # 불러온 설정으로 다시 y좌표 구할때
    def coordinate_re_extract_y(self, list_var, crd_value, s_str, e_str):
        start_str = None
        end_str = None
        for i in range(len(crd_value)):
            if crd_value[i] == s_str:
                start_str = i
            if crd_value[i] == e_str:
                end_str = i
        # TODO 구조 이해하기
        self.list_var = list_var
        self.list_var.append(crd_value[(start_str + 3):(end_str - 1)])


class Capture:
    # 필요 인수 체크
    def cap_check(self):
        if self.lineEdit_lctr.text() == '0':
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-몇교시인지 입력되지 않았습니다.")
            bln = False
        elif self.l_dir_show.text() == "":
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-경로가 지정되지 않았습니다.")
            bln = False
        elif self.l_sPoint_show.text() == "":
            self.textBrowser_output.clear()
            self.textBrowser_output.append("-좌표가 지정되지 않았습니다.")
            bln = False
        else:
            self.textBrowser_output.append("★캡쳐영역 설정 완료★")
            self.textBrowser_output.append("★" + self.lineEdit_lctr.text() + "교시로 설정 완료★")
            self.textBrowser_output.append("")
            bln = True
        return bln

    # JPG 이미지 생성, 폴더생성
    def jpg_capture(self, lesson, s_point, rel_x, rel_y, working_path):
        # 설정한 교시만큼 반복
        for i in range(int(lesson)):
            img_name = 1

            # 원래 경로로 복귀
            os.chdir(working_path)
            # 폴더 확인 및 생성
            if not os.path.exists(str(i + 1) + '교시'):
                os.mkdir(str(i + 1) + '교시')
            # 저장할 폴더 경로 생성 및 지정
            os.chdir(working_path + '/' + str(i + 1) + '교시')

            self.textBrowser_output.append("▶현재 캡쳐 : " + str(i + 1) + "교시")

            # 설정된 교시 내 캡쳐 반복
            while True:
                ok = QMessageBox.question(self, '캡쳐 중', "Yes = 다음 교시로 이동 \nNo = 현재 페이지 캡쳐 \nCancel = 방금 캡쳐 삭제",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

                if ok == QMessageBox.Yes:
                    # 입력 외의 교시때 종료
                    if (i + 1) == int(lesson):
                        # 폴더삭제시, 사용중 방지
                        os.chdir(working_path)
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("●●●캡쳐 종료●●●")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.statusBar().showMessage("Ready")
                        break
                    else:
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("▶" + str(i + 2) + "교시로 이동")
                        self.textBrowser_output.append("")

                        img_name = 1
                        break
                elif ok == QMessageBox.No:
                    if img_name < 10:
                        screenshot('0' + str(img_name) + '.jpg', region=(s_point[0], s_point[1], rel_x, rel_y))
                    else:
                        screenshot(str(img_name) + '.jpg', region=(s_point[0], s_point[1], rel_x, rel_y))
                    self.textBrowser_output.append("   " + str(img_name) + "페이지 저장 완료")
                    img_name += 1
                else:
                    try:
                        if img_name < 11:
                            os.remove('0' + str(img_name - 1) + '.jpg')
                        else:
                            os.remove(str(img_name - 1) + '.jpg')
                        self.textBrowser_output.append("   " + str(img_name - 1) + "페이지 삭제")
                        img_name -= 1
                    except Exception:
                        img_name = 1
                        self.textBrowser_output.clear()
                        self.textBrowser_output.append("-삭제할 이미지가 없습니다.")
                        pass

    # JPG 이미지 생성, 삭제, PDF 생성
    def pdf_capture(self, lesson, s_point, rel_x, rel_y, working_path, pdf_name):
        # 원래 경로로 복귀
        os.chdir(working_path)
        # 폴더 확인 및 생성
        if not os.path.exists('imgTemp'):
            os.mkdir('imgTemp')
        set_path = str(working_path + '/' + 'imgTemp')
        # 저장할 폴더 경로 생성 및 지정
        os.chdir(set_path)

        img_name = 1

        try:
            x = [f for f in os.listdir(set_path) if f.endswith(".jpg")]
            img_name = len(x) + 1
        except Exception:
            pass

        # 설정한 교시만큼 반복
        for i in range(int(lesson)):
            self.textBrowser_output.append("▶현재 캡쳐 : " + str(i + 1) + "교시")
            view_value = 1

            # 설정된 교시 내 캡쳐 반복
            while True:
                ok = QMessageBox.question(self, '캡쳐 중', "Yes = 다음 교시로 이동 \nNo = 현재 페이지 캡쳐 \nCancel = 방금 캡쳐 삭제",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)

                if ok == QMessageBox.Yes:
                    # 입력 외의 교시때 종료
                    if (i + 1) == int(lesson):
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("●●●캡쳐 종료●●●")
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("")
                        self.statusBar().showMessage("Ready")
                        break
                    else:
                        self.textBrowser_output.append("")
                        self.textBrowser_output.append("▶" + str(i + 2) + "교시로 이동")
                        self.textBrowser_output.append("")

                        break
                elif ok == QMessageBox.No:
                    if img_name < 10:
                        screenshot('0' + str(img_name) + '.jpg', region=(s_point[0], s_point[1], rel_x, rel_y))
                    else:
                        screenshot(str(img_name) + '.jpg', region=(s_point[0], s_point[1], rel_x, rel_y))
                    self.textBrowser_output.append("   " + str(img_name) + "({})페이지 저장 완료".format(view_value))
                    img_name += 1
                    view_value += 1
                else:
                    try:
                        if img_name < 11:
                            os.remove('0' + str(img_name - 1) + '.jpg')
                        else:
                            os.remove(str(img_name - 1) + '.jpg')
                        self.textBrowser_output.append("   " + str(img_name - 1) + "페이지 삭제")
                        img_name -= 1
                        view_value -= 1
                    except Exception:
                        img_name = 1
                        view_value = 1
                        self.textBrowser_output.clear()
                        self.textBrowser_output.append("-삭제할 이미지가 없습니다.")
                        pass

        try:
            # PDF 생성 및 원본 삭제
            x = [f for f in os.listdir(set_path) if f.endswith(".jpg")]
            FileGenerate.make_pdf(self, pdf_name, x, set_path)

            for i in range(len(x)):
                os.remove(x[i])

            os.chdir(working_path)

            if self.checkBox_endClr.isChecked():
                self.textBrowser_output.clear()

            self.textBrowser_output.append("★PDF 생성 완료★")

        except Exception:
            os.chdir(working_path)

            if self.checkBox_endClr.isChecked():
                self.textBrowser_output.clear()

            self.textBrowser_output.append("-사용할 이미지가 없습니다.")
            pass


class Config:
    # 프리셋 리스트 새로고침
    def config_list_refresh(self):
        config = ConfigParser()
        config.read('setting.ini')
        self.comboBox_loadSet.clear()
        self.comboBox_loadSet.addItems(config.sections())

    # 설정 불러오기
    def load_setting(self, config):
        config.read('setting.ini')
        section = self.comboBox_loadSet.currentText()
        option = config.options(section)
        key = []

        for i in range(len(option)):
            key.append(config.get(section, option[i]))

        # lesson
        set_lesson = key[0]
        # work_dir[0]
        set_work_dir0 = key[1]

        # x, y맵핑
        crd = CoordinateExtract()
        # 프리셋을 생성 시
        try:
            set_coordinate0 = []
            # set_coordinate0에 시작 x 좌표 추가
            crd.coordinate_extract(set_coordinate0, key[2], 'x', ',')
            # set_coordinate0에 시작 y 좌표 추가
            crd.coordinate_extract(set_coordinate0, key[2], 'y', ')')

            set_coordinate3 = []
            # set_coordinate3에 끝 x 좌표 추가
            crd.coordinate_extract(set_coordinate3, key[3], 'x', ',')
            # set_coordinate3에 끝 y 좌표 추가
            crd.coordinate_extract(set_coordinate3, key[3], 'y', ')')

        # 불러온 프리셋으로 다시 저장 시
        except Exception:
            set_coordinate0 = []
            # set_coordinate0에 시작 x 좌표 추가
            crd.coordinate_re_extract_x(set_coordinate0, key[2], '[', ',')
            # set_coordinate0에 시작 y 좌표 추가
            crd.coordinate_re_extract_y(set_coordinate0, key[2], ',', ']')

            set_coordinate3 = []
            # set_coordinate3에 끝 x 좌표 추가
            crd.coordinate_re_extract_x(set_coordinate3, key[3], '[', ',')
            # set_coordinate3에 끝 y 좌표 추가
            crd.coordinate_re_extract_y(set_coordinate3, key[3], ',', ']')

        # chk_set
        set_chkset = key[4]
        # open_set
        set_openset = key[5]
        # clr_set
        set_clrset = key[6]

        return set_lesson, set_work_dir0, set_coordinate0, set_coordinate3, set_chkset, set_openset, set_clrset


class FileGenerate:
    # PDF 생성
    def make_pdf(self, pdf_file_name, list_pages, img_dir):
        if img_dir:
            img_dir += '/'

        cover = Image.open(img_dir + str(list_pages[0]))
        width, height = cover.size

        pdf = FPDF(unit="pt", format=[width, height])

        for page in list_pages:
            pdf.add_page()
            pdf.image(img_dir + str(page), 0, 0)

        x = [f for f in os.listdir(img_dir) if f.endswith(".pdf")]
        x.append('')

        for i in range(len(x)):
            if x[i] == '':
                if (i+1) < 10:
                    pdf.output(img_dir + pdf_file_name + '_0{}차시.pdf'.format(str(i+1)), "F")
                else:
                    pdf.output(img_dir + pdf_file_name + '_{}차시.pdf'.format(str(i+1)), "F")
                break


if __name__ == '__main__':
    print("Not execute this module. Use to 'import'")