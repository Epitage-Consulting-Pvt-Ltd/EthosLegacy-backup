def camer():
    import cv2

    #    from picamera.array import PiBGRArray
    from picamera2 import Picamera2
    import os

    # Load the cascade
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    #    face_cascade = cv2.CascadeClassifier( os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml") ) #New Line
    cv2.startWindowThread()  # New Line
    picam2 = Picamera2()  # New Line
    # To capture video from webcam.
    #    cap = cv2.VideoCapture(0)
    #    if not cap.isOpened():     #New Line
    #        print("Cannot Open Camera")    #NL
    #        exit()                 #NL
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XBGR8888', "size": (800, 600)})) #NewLine
    picam2.start()	#NL
    while True:
        # Read the frame
        #_, img = cap.read()
        # NewAlternative
        im = picam2.capture_array()
        #        ret, img = cap.read()  #NL
        #        _, img = cv2.imread(img_path)  #NL
        #        if not _:              #NL
        #                print("Can't receive frame . Exiting...")
        #                break
        #        if _: # if ret is True:        #NL
        #               gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ... other code ...
        #        else:                  #NL
        #                print("empty frame")
        #                exit(1)
        # Convert to grayscale
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #       gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)    #NL
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30),flags = cv2.CASCADE_SCALE_IMAGE)
        # Spelling channged gray --> grey
        #faces = face_cascade.detectMultiScale(grey, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        # NewAlternate to above
        #        faces = face_detector.detectMultiScale(grey, 1.3, 5)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)

        # Display
        cv2.imshow("Webcam Check", im)

        # Stop if escape key is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the VideoCapture object
    #cap.release()
    cv2.destroyAllWindows()
