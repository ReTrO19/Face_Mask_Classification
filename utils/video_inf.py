import cv2
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models
import dlib
import time
import numpy as np
# import imutils

def convert_and_trim_bb(image, rect):
    # extract the starting and ending (x, y)-coordinates of the
    # bounding box
    startX = rect.left()
    startY = rect.top()
    endX = rect.right()
    endY = rect.bottom()
    # ensure the bounding box coordinates fall within the spatial
    # dimensions of the image
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, image.shape[1])
    endY = min(endY, image.shape[0])
    # compute the width and height of the bounding box
    w = endX - startX
    h = endY - startY
    # return our bounding box coordinates
    return (startX, startY, w, h)


def infer_on_video(face_cnn,video_path):
    """
    Run inference on Video
    :params face_cnn Boolean If true it will run face detection using CNN if False will use HOG Detector
    :params video_path Input video that you want to run inference on

    :retrun None
    """
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, image_frame = cap.read()
        rgb = cv2.cvtColor(image_frame,cv2.COLOR_BGR2RGB)

        if face_detection_cnn:
            detect_model_path = "mmod_human_face_detector.dat"
        else:
            detect_model_path = None

        if detect_model_path is not None:
            cnn_face_detector = dlib.cnn_face_detection_model_v1(detect_model_path)
        else:
            detector = dlib.get_frontal_face_detector()

        model = models.load_model('h5_weigth\\mnm_model.h5')

        classes = ['With Mask','Without Mask']

        start = time.time()
        print("[INFO[ PERFORMING FACE DETECTION WITH DLIB]]")

        if detect_model_path is not None:
            rects = cnn_face_detector(rgb, 1)
        else:
            rects = detector(rgb,1)

        end = time.time()

        print("[INFO] FACE DETECTION TOOK {:.4f} seconds".format(end - start))
        
        if detect_model_path is not None:
            boxes = [convert_and_trim_bb(image_frame,r.rect) for r in rects]
        else:
            boxes = [convert_and_trim_bb(image_frame,r) for r in rects]

        # print("Boxes === >",boxes)
        for single_box in boxes:
            x,y,w,h = single_box[0],single_box[1],single_box[2],single_box[3]

            face_resized_img = image_frame[y:y+h,x:x+w]
            face_resized_img = cv2.resize(face_resized_img,(150,150))
            face_resized_img = np.expand_dims(face_resized_img, axis=0)
            face_resized_img = np.vstack([face_resized_img])

            model_predict = model.predict(face_resized_img)
            print(model_predict)
            pred = np.argmax(model_predict,axis=1)
            print(pred)
            class_name = classes[pred[0]]

            cv2.rectangle(image_frame,(x,y-30),(x + w,y),(255,255,225),-1)
            cv2.putText(image_frame,class_name, (x , y-10),cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.rectangle(image_frame,(x,y),(x + w, y + h),(0,255,0),2)

        cv2.imshow("Output:",image_frame)
        cv2.waitKey(1)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Input values for the infer_on_image function')
    parser.add_argument('--face_cnn','-fc',type=bool,help='Pass True if CNN Face Detector else False to use HOG Detector. ',required=True)
    parser.add_argument('--inp_vid','-vid',help='Pass video file as an input. ',required=True)

    args = parser.parse_args()
    infer_on_video(args.face_cnn,args.inp_vid)