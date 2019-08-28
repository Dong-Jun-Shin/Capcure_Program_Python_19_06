from pynput import mouse
import time
import pyautogui
import os

sta = time.time()
#----------------------------------------------------------------------------------------------------------------------
### 이미지 캡쳐
def capture(sPoint,rel_x, rel_y):

    im3 = pyautogui.screenshot(str(imgName)+'.jpg', region=(sPoint[0], sPoint[1],rel_x, rel_y))
    print(str(imgName) + "페이지 저장 완료")

###현재 마우스 위치 값 받기

ready = input("◈시작지정 -> enter를 입력해주세요.")
sPoint = pyautogui.position()
print("지정한 시작위치 :", sPoint)
print

ready = input("◈끝지정 -> enter를 입력해주세요.")
ePoint = pyautogui.position()
print("지정한 끝위치 : ", ePoint)


###캡쳐 영역값 잡기
rel_x = ePoint[0] - sPoint[0]     # x의 상대값 저장
rel_y = ePoint[1] - sPoint[1]     # y의 상대값 저장
print("  ★캡쳐영역 설정 완료★")
print()

###몇교시인지 값 받기
print("◈몇 교시인가요?")
lesson = input()
print("  ★" + lesson + "교시로 설정 완료★")
print()
print()

###캡쳐 시작


imgName=1
for i in range(int(lesson)):                                           ##설정한 교시만큼 반복
    os.chdir(r'C:/Users/tlseh/Desktop/임시 저장/')                      #원래 경로로 복귀
    if not os.path.exists(str(i+1)+'교시'):                             #폴더 확인 및 생성
        os.mkdir(str(i+1)+'교시')
    os.chdir(r'C:/Users/tlseh/Desktop/임시 저장/'+str(i+1)+'교시')      #저장할 폴더 경로 생성 및 지정
    
    print("●●●캡쳐 시작●●●")
    print("(0 = 다음교시로 이동, Enter = 현재 구역 캡쳐)")
    print("  ▶현재 캡쳐 : " + str(i+1) + "교시")
    
    while True:                                                ##설정된 교시 내 캡쳐 반복
        cmd = input()
        if cmd == '0':
            if (i+1) == int(lesson) :                           #입력 외의 교시때 종료
                os.chdir(r'C:/Users/tlseh/Desktop/임시 저장/')  #폴더삭제시, 사용중 방지
                print()
                print()
                print("●●●캡쳐 종료●●●")
                break
            else:
                print()
                print("▶" + str(i+2) + "교시로 이동")
                print()
                print()
                imgName=1
                break
        else:
            capture(sPoint,rel_x, rel_y)
            imgName += 1
#----------------------------------------------------------------------------------------------------------------------
cur = time.time()
currunt_time = cur - sta
print("소요시간 : %s초" % round(currunt_time,2))
