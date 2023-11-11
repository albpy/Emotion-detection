import imagehash
import os
from PIL import Image
directory = os.getcwd()
class_tag = []
hash_es = {}
duplicate_path = []
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

def hash_val(image_path):
    with Image.open(image_path) as img:
        return imagehash.average_hash(img)
def remove_carbon(target, duplicate_path,filenms):
    for dirname in filenms.keys():
        target_dir = os.path.join(target, dirname)
        for files in filenms[dirname]:
            file_path = os.path.join(target_dir, files)
            if file_path in duplicate_path:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"removed{file_path}")
def rem_dupes(tardir, filenms):
    for dirname in filenms.keys():
        tar_dir = os.path.join(tardir, dirname)
        # print(tardir_dir)
        for files in filenms[dirname]:
            # for filename in files:
            file_path = os.path.join(tar_dir, files)
            if os.path.exists(file_path):
                if file_path.endswith(".jpg"):
                    hash_ed = hash_val(file_path)
                    # print(hash_ed)
                    if hash_ed in hash_es:
                        duplicate_path.append(file_path)
                    else:
                        hash_es[hash_ed] = file_path
    remove_carbon(tardir, duplicate_path, filenms)
    
filename = scanRecurse(directory)
rem_dupes(directory, filename)