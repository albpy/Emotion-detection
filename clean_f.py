import os
import mediapipe as mp
import cv2

detect_the_face = mp.solutions.face_detection.FaceDetection()

class_tag = []
def scanRecurse(rootdir):
    printDir = False
    for dir in os.scandir(rootdir):
        if dir and printDir == False:
            print(type(dir))
        printDir = True
        if dir.is_dir(): # Get all class directory
            class_tag.append(dir.name)
    filenms = {cls : [] for cls in class_tag} 
    dir_ocuur = 0
    for dir in os.scandir(rootdir):
        if dir.is_dir():
            for file in os.scandir(dir):
                filenms[dir.name].append(file.name)
                 
    # print(filenms)      
    return filenms

def detect_faces(picture):
    try:
        rgb_img = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)
    except:
        return []
    results = detect_the_face.process(rgb_img)
    faces = []
    if results.detections != None:
        for face in results.detections:
            bounding_box = face.location_data.relative_bounding_box
            faces.append(bounding_box)
    return faces
def disconnect_2_faces(filenms, target):
    imageCount = 0
    for dirname in filenms.keys():
        target_dir = os.path.join(target, dirname)
        # print(source_dir)
        for files in filenms[dirname]:
            # for filename in files:
            file_path = os.path.join(target_dir, files)
            image= cv2.imread(file_path)
            bounding_boxes = detect_faces(image)
      
            if len(bounding_boxes) == 1:
                imageCount+=1
                height,width,channel = image.shape
                # print(height,width,channel)
                x,y = max(int(bounding_boxes[0].xmin*width), 0), max(int(bounding_boxes[0].ymin*height), 0)
                w,h = min(int(bounding_boxes[0].width*width), width-x),min(int(bounding_boxes[0].height*height), height-y)
                # print((x, y),(w,h))
                bbx_img = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
                #croppedImage = image[y:y+h,x:x+w]
                cv2.imwrite(file_path, bbx_img)
            else:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(file_path)

target = os.getcwd()
file_names = scanRecurse(target)                
disconnect_2_faces(file_names, target)