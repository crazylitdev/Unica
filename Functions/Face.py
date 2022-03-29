import face_recognition
import cv2
import numpy as np
import pickle
import time


class Recognition:

    def __init__(self) -> None:
        self.namePKL = open("./Database/name.pkl", "rb")
        self.embedPKL = open("./Database/embed.pkl", "rb")
        self.nameDict = pickle.load(self.namePKL)
        self.embedDict = pickle.load(self.embedPKL)
        self.embedPKL.close()
        self.namePKL.close()
        self.knownEncodings = []
        self.knownNames = []
        for id , embedList in self.embedDict.items():
            for embed in embedList:
                self.knownEncodings += [embed]
                self.knownNames += [id]
				
    def start(self) -> None:
        'This function detects faces if and locate them if they are in the database.'
        videoCapture = cv2.VideoCapture(0)
        faceLocations = []
        faceEncodings = []
        faceNames = []
        processFrame = True
        while True  :
            try:
                a, frame = videoCapture.read()
                resizedFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                RGBResizedFrame = resizedFrame[:, :, ::-1]
                if processFrame:
                    faceLocations = face_recognition.face_locations(RGBResizedFrame)
                    faceEncodings = face_recognition.face_encodings(RGBResizedFrame, faceLocations)
                    faceNames = []
                    for faceEncoding in faceEncodings:
                        matches = face_recognition.compare_faces(self.knownEncodings, faceEncoding)
                        name = "Unknown"
                        faceDistances = face_recognition.face_distance(self.knownEncodings, faceEncoding)
                        bestMatchIndex = np.argmin(faceDistances)
                        if matches[bestMatchIndex]:
                            name = self.knownNames[bestMatchIndex]
                        faceNames.append(name)

                processFrame = not processFrame

                for (top, right, bottom, left), name in zip(faceLocations, faceNames):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, self.nameDict[name], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except KeyError:
                continue

        videoCapture.release()
        cv2.destroyAllWindows()

class Train:

    def __init__(self) -> None:
        self.name = input("Enter Your Name : ")
        self.id = input("Enter ID : ")
        self.namePKL = open("./Database/name.pkl", "rb")
        self.embedPKL = open("./Database/embed.pkl", "rb")
        try:
            self.nameDict = pickle.load(self.namePKL)
            self.embedDict = pickle.load(self.embedPKL)
        except:
            self.nameDict = {}
            self.embedDict = {}
        namePKL = open("./Database/name.pkl", "wb")
        pickle.dump(self.nameDict, namePKL)
        self.embedPKL.close()
        self.namePKL.close()
        namePKL.close()

    def start(self) -> None:
        for i in range(5):
            key = cv2.waitKey(1)
            webcam = cv2.VideoCapture(0)
            while True:
                check, frame = webcam.read()
                cv2.imshow("Capturing", frame)
                resizedFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                RGBResizedFrame = resizedFrame[:, :, ::-1]
                key = cv2.waitKey(1)
                if key == ord('s') : 
                    faceLocations = face_recognition.face_locations(RGBResizedFrame)
                    if faceLocations != []:
                        faceEncoding = face_recognition.face_encodings(frame)[0]
                        if self.id in self.embedDict:
                            self.embedDict[self.id] += [faceEncoding]
                        else:
                            self.embedDict[self.id] = [faceEncoding]
                        webcam.release()
                        cv2.waitKey(1)
                        cv2.destroyAllWindows()     
                        break
                elif key == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    break
        self.embedPKL = open("./Database/embed.pkl", "wb")
        pickle.dump(self.embedDict, self.embedPKL)
        self.embedPKL.close()


# Train().start()
Recognition().start()