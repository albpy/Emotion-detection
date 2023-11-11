import os
import cv2
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

def resize_to_50x50(filenms, dirs):
    for dirname in filenms.keys():
        target_dir = os.path.join(dirs, dirname)
        for files in filenms[dirname]:
            file_path = os.path.join(target_dir, files)
            image = cv2.imread(file_path)
            if image is not None:
                pass
                #res_img = cv2.resize(image, (96,96))
                #cv2.imwrite(file_path, res_img)
            #print(file_path)
            else:
                print(f'file {file_path} is empty')
                os.remove(file_path)
        print(target_dir)
            
            
    
    
    
dirs = os.getcwd()

file_nms = scanRecurse(dirs)
resize_to_50x50(file_nms, dirs)

