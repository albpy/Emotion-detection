import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers.legacy import Adam

from tensorflow.keras.preprocessing import image
#for profressive loading
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import PIL
import cv2

import os

from tensorflow.keras.callbacks import LearningRateScheduler
import tensorflow.keras.backend as K

from tensorflow.keras import losses

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import random
import numpy as np

from tensorflow.keras.callbacks import EarlyStopping

early_stoping = EarlyStopping(monitor = 'val_loss', patience=1, restore_best_weights=True)



train_folder = 'train\\'
test_folder = 'test\\'
validation_folder = 'validation\\'

IMG_WIDTH = 48
IMG_HEIGHT = 48
BATCH_SIZE = 64

train_data_generator = ImageDataGenerator(rescale=1.0/255, zoom_range=0.2, height_shift_range=0.2, fill_mode='nearest')
train_generator=train_data_generator.flow_from_directory(train_folder, target_size=(IMG_WIDTH, IMG_HEIGHT), batch_size=BATCH_SIZE, class_mode='categorical', shuffle = True, color_mode="grayscale")

num_of_tr = train_generator.n
print("num of train images" , num_of_tr)

validation_data_generator = ImageDataGenerator(rescale=1.0/255, zoom_range=0.2, height_shift_range=0.2, fill_mode='nearest')
validation_generator = validation_data_generator.flow_from_directory(validation_folder, target_size=(IMG_WIDTH, IMG_HEIGHT), batch_size=BATCH_SIZE, class_mode='categorical', shuffle = True,  color_mode="grayscale")

num_of_val = validation_generator.n
print("num of validation images" , num_of_val)

test_data_generator = ImageDataGenerator(rescale=1.0/255, zoom_range=0.2, height_shift_range=0.2, fill_mode='nearest')
test_generator = validation_data_generator.flow_from_directory(test_folder, target_size=(IMG_WIDTH, IMG_HEIGHT), batch_size=BATCH_SIZE, class_mode='categorical', shuffle = True,  color_mode="grayscale")

num_of_test = test_generator.n
print("num of validation images" , num_of_val)


class_names = {value : key for key, value in train_generator.class_indices.items()}

def what_classes(class_names):
    for key, value in class_names.items():
        print(f"{key} : {value}")
    
def show_rand_imges(train_folder):
    for cls in os.scandir(train_folder):
        folder = os.path.join(train_folder, cls.name)
        file__name = [file.name for file in os.scandir(folder)]
        for i in range(5):
            file_name = random.choice(file__name)
            image_path = os.path.join(folder, file_name)
            img = mpimg.imread(image_path)
            ax = plt.subplot(1,5,i+1)
            ax.title.set_text(file_name)
            plt.imshow(img)
            
import ctypes
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002) #prevent screen saver or sleep  

initial_lr = 0.0001
m = 10
    
def cust_lr(epoch):
    return initial_lr/(1+epoch/m)  

what_classes(class_names)
#show_rand_imges(train_folder)

def train(initial_lr = initial_lr, m =10, model = None):
    lr_scheduler = LearningRateScheduler(cust_lr) 
    if model == None:
        
        model = Sequential()

        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(7, activation='softmax'))
   
        hist = model.compile(loss='categorical_crossentropy',optimizer=Adam(learning_rate=0.0001, decay=1e-6),metrics=['accuracy'])

        model_trained = model.fit_generator(
                    train_generator,
                    steps_per_epoch=num_of_tr // BATCH_SIZE,
                    epochs=30,
                    validation_data=validation_generator,
                    validation_steps=num_of_val // BATCH_SIZE,
                    )    
        model.save('emotions.h5', model_trained)
        
    else:
        hist = model.compile(loss='categorical_crossentropy',optimizer=Adam(learning_rate=0.0001, decay=1e-6),metrics=['accuracy'])
        model_trained = model.fit_generator(
                    train_generator,
                    steps_per_epoch=num_of_tr // BATCH_SIZE,
                    epochs=30,
                    validation_data=validation_generator,
                    validation_steps=num_of_val // BATCH_SIZE,
                    callbacks = [early_stoping])    
    model.evaluate(test_generator, steps = 10)
    
    
    plt.plot(model_trained.history['loss'], label = 'Train loss')
    plt.plot(model_trained.history['val_loss'], label = 'Validation loss')
    plt.xlabel('Epoch')
    plt.ylabel('loss')
    plt.legend()
    plt.show()
    
train()


    

