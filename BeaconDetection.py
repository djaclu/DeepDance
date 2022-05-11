import cv2
import time
import socket

#beacon detection parameters
minimum_area = 25

#client setup
ip = "127.0.0.1"
port = 50010
count = 0

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ip, port))

def get_beacons():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    time.sleep(2)
    
    while True:
        ret, frame = cap.read()
        #frame = cv2.flip(frame, 1) #Projection vs. Screen
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, (0, 0, 245), (255, 10, 255))
        contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Beacon Filtering
        beacons = []
        for contour in contours:
            if cv2.contourArea(contour) >= minimum_area:
                beacons.append(contour)

        #beacons[:] = [beacon for beacon in beacons if cv2.contourArea(beacon) <= minimum_area]

        #Beacon Tracking
        beacon_queue = []
        for beacon in beacons:
            M = cv2.moments(beacon)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 5, (0, 0, 0), -1)
            beacon_queue.append((cX, cY))

        cv2.drawContours(mask, beacons, -1, (255, 10, 255), thickness=3)
        for XY in beacon_queue:
            coordinates = '{"x":'+str(XY[0])+',"y":'+str(XY[1])+'}'
            if beacon_queue.index(XY) == 0:
                clientSocket.send(coordinates.encode())

        #Beacon Visualization: Uncomment to see.
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    clientSocket.close()
    cap.release()
    cv2.destroyAllWindows()

get_beacons()



