import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
# Set the random seed for reproducibility
np.random.seed(42)
#tf.random.set_seed(42)
batch_size=32
target_size_square=150
diases=14 #read folder train and len (folders) 


# Set up the data generators for training and validation
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory('train', target_size=(target_size_square, target_size_square), batch_size=batch_size, class_mode='binary')
validation_generator = test_datagen.flow_from_directory('validate', target_size=(target_size_square, target_size_square), batch_size=batch_size, class_mode='binary')

# Build the CNN model
model = Sequential([
    Conv2D(target_size_square, (3, 3), activation='relu', input_shape=(target_size_square, target_size_square, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(target_size_square*2, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(target_size_square*2, (3, 3), activation='relu'),
    Flatten(),
    Dense(target_size_square*2, activation='relu'),
    Dense(diases, activation='sigmoid')
])


# Compile the model

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_generator, steps_per_epoch=len(train_generator), epochs=50, validation_data=validation_generator, validation_steps=len(validation_generator))

model.save('fishes.h5')
