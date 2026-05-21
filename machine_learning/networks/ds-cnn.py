import tensorflow as tf
from tensorflow.keras import layers, models

def build_dscnn(input_shape=(49, 40, 1), num_classes=12):
    model = models.Sequential(name="DS-CNN")

    model.add(layers.InputLayer(input_shape=input_shape, name="Input"))

    model.add(layers.Conv2D(16, (3, 3), strides=(2, 2), padding='same', 
                            activation='relu', name="Conv_1"))

    model.add(layers.DepthwiseConv2D((3, 3), padding='same', 
                                     activation='relu', name="Depthwise_1"))
    model.add(layers.Conv2D(32, (1, 1), padding='same', 
                            activation='relu', name="Pointwise_1"))

    model.add(layers.MaxPooling2D((2, 2), name="Pool_1"))

    model.add(layers.DepthwiseConv2D((3, 3), padding='same', 
                                     activation='relu', name="Depthwise_2"))
    model.add(layers.Conv2D(64, (1, 1), padding='same', 
                            activation='relu', name="Pointwise_2"))

    model.add(layers.GlobalAveragePooling2D(name="GAP"))
    model.add(layers.Dense(num_classes, activation='softmax', name="Output"))

    return model

dscnn_model = build_dscnn()
dscnn_model.summary()