from PIL import Image
import os

direc = os.getcwd()

for dirs in os.scandir(direc):
    if dirs.is_dir():
        path = os.path.join(direc, dirs.name)
        for file in os.scandir(dirs):
            if file.name.endswith('.png'):
                png_file = os.path.join(path, file.name)
                png_image = Image.open(png_file)
                jpg_rename = os.path.splitext(file.name)[0] + '.jpg'
                jpg_file = os.path.join(path, jpg_rename)
                png_image.save(jpg_file, 'JPEG')
                os.remove(png_file)
            
            
                 



