import random,colorama,keyboard,os,cv2,time,sys
from pyfiglet import Figlet
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject 
from PIL import Image
mySerial=SerialObject("COM3",9600,1)
def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    h=[
        [0, 0, 0, 0, 0],[1, 1, 1, 1, 1],[0, 1, 1, 0, 0]
    ]

    detector = HandDetector(maxHands=1)

    count=0
    timer = 0
    stateResult = False
    startGame = False
    scores = [0, 0]  # [AI, Player]
    
    while True:
        imgG = Image.open("Resources/game_over.png")
        imgW=Image.open("Resources/won.png")
        imgBG = cv2.imread("Resources/BG.png")
        success, img = cap.read()
    
        imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
        imgScaled = imgScaled[:, 80:480]
    
        # Find Hands
        hands, img = detector.findHands(imgScaled)  # with draw
    
        if startGame:
    
            if stateResult is False:
                timer = time.time() - initialTime
                cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
    
                if timer > 3:
                    stateResult = True
                    timer = 0
    
                    if hands:
                        playerMove = None
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        if fingers == [0, 0, 0, 0, 0]:
                            playerMove = 1
                        if fingers == [1, 1, 1, 1, 1]:
                            playerMove = 2
                        if fingers == [0, 1, 1, 0, 0]:
                            playerMove = 3
    
                        randomNumber = random.randint(1, 3)
                        count=count+1
                        print(f"Turn {count}")
                        
                        mySerial.sendData(h[randomNumber-1])
                        imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    
                        # Player Wins
                        if (playerMove == 1 and randomNumber == 3) or \
                                (playerMove == 2 and randomNumber == 1) or \
                                (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1
    
                        # AI Wins
                        if (playerMove == 3 and randomNumber == 1) or \
                                (playerMove == 1 and randomNumber == 2) or \
                                (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1
                        
    
        imgBG[234:654, 795:1195] = imgScaled
        
            
        if stateResult:
            
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    
        cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
        # cv2.imshow("Image", img)
        cv2.imshow("BG", imgBG)
        # cv2.imshow("Scaled", imgScaled)
        if scores[1]>scores[0]:
            cv2.destroyWindow("BG")
            
            count=0
            imgW.show()
            time.sleep(5)
            startGame = False
            scores=[0,0]
        elif count==6:
            cv2.destroyWindow("BG")
            count=0
            imgG.show()
            time.sleep(5)
            
            startGame = False
        
        key = cv2.waitKey(1)
        if key == ord('s'):
            startGame = True
            initialTime = time.time()
            stateResult = False
            imgG.close()
            imgW.close()
        # elif key==ord('t'):
        #     count=5
        elif key==ord('r'):
            imgG.close()
            scores = [0, 0]
            startGame = False
            initialTime = time.time()
            stateResult = True
            imgG.close()
            imgW.close()
        # elif key==ord('w'):
        #     scores[1]=5
        elif key==ord('m'):
            cv2.destroyWindow("BG")
            menu()
        elif key==ord('q'):
            cv2.destroyAllWindows()
            imgG.close()
            imgW.close()
            sys.exit()
def menu():
    os.system("cls")
    figlet=Figlet()
    print(colorama.Fore.GREEN+figlet.renderText("Welcome to Rock Paper Scissor"))
    print(colorama.Fore.GREEN+figlet.renderText("You have to five tries"))
    print(colorama.Fore.GREEN+"Press [s] to start",colorama.Fore.BLUE+"Press [r] to reset",colorama.Fore.BLACK+"Press [m] go to menu",colorama.Fore.RED+"Press [q] to start",sep="\n")
    while True:
        if keyboard.is_pressed("s"):
            os.system("cls")
            return
        elif keyboard.is_pressed("q"):
            cv2.destroyAllWindows()
            os.system("cls")
            sys.exit()
            
main()