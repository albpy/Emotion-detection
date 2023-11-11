import os
import re

directory = os.getcwd()
print(directory)
pattern_t_rmv = r'^\d+'

file_list = os.listdir(directory)

for filename in file_list:
    if re.match(pattern_t_rmv, filename):
        newname = re.sub(pattern_t_rmv, '' , filename)
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, newname)
        if os.path.exists(new_path):
            base, ext = os.path.splitext(newname)
            i=1
            while os.path.exists(new_path):
                newname = f"{base}_{i}{ext}"
                new_path = os.path.join(directory, newname)
                i+=1
        os.rename(old_path, new_path)
