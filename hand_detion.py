import cv2
from cvzone.HandTrackingModule import HandDetector
from controller import cnt 
import pyfirmata
# # Nhập cổng COM kết nối với Arduino ở đây
comport='COM3'

board=pyfirmata.Arduino(comport)

# Nối 5 led với các chân từ D2 tới D6
led_1=board.get_pin('d:2:o')
led_2=board.get_pin('d:3:o')
led_3=board.get_pin('d:4:o')
led_4=board.get_pin('d:5:o')
led_5=board.get_pin('d:6:o')
led_l = [led_1, led_2, led_3, led_4, led_5]
def led(fingerUp):
    fc = 0
    for x in range(len(fingerUp)):
        led_l[x].write(fingerUp[x])
        fc += fingerUp[x]
    cv2.putText(frame, f'Finger count:{fc}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

detetor = HandDetector(detectionCon=0.8, maxHands=1)

video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    frame = cv2.flip(frame,1)
    hands, img = detetor.findHands(frame)
    if hands:
        lmlist=hands[0]
        fingerUp = detetor.fingersUp(lmlist)
        print(fingerUp)
        cnt.led(fingerUp)  # Gọi phương thức led từ đối tượng cnt
        led(fingerUp)

    cv2.imshow("Window", frame)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
