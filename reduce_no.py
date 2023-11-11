import os
import random
curdir=os.getcwd()

train_dir = "C:\\Users\\albin\\OneDrive\\Documents\\Python\\ethiopian_sign_symbol_kaggle\\Xml-test-train-jpg\\Microexp\\train"


for d in os.scandir(train_dir):
    train_files = []

    if d.is_dir():
        for f in os.scandir(os.path.join(train_dir, d.name)):
            dirs = os.path.join(curdir, f.name)
            train_files.append(dirs)
        print(len(train_files))

for d in os.scandir(os.getcwd()):
    if d.is_dir():
        dirs = os.path.join(curdir, d.name)
        files = os.listdir(dirs)
        random.shuffle(files)
        target_fle_cnt = 2000
        files_cnt_to_rmv = len(files)-target_fle_cnt
        s = 0
        while(len(os.listdir(dirs))>2000):
            try:
                files_to_rmv = os.path.join(dirs, files[s])
                if files_to_rmv in train_files:
                    os.remove(files_to_rmv)
                    
                    print(f"Removed {files_to_rmv}")
                s+=1
            except:
                print(s)
        print(f"removed {files_cnt_to_rmv} files")
               