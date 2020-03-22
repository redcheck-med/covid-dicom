# -*- coding: utf-8 -*-
from tensorflow.keras.applications import VGG16
from tensorflow.keras import models
from tensorflow.keras.layers import  Dense, Lambda
from tensorflow.keras import backend as K
from tensorflow.keras.optimizers import SGD



def global_average_pooling(x):
    """Aplica o GBP nos ouputs do max pooling da rede."""
    return K.mean(x, axis = (2, 3))

def global_average_pooling_shape(input_shape):
    return input_shape[0:2]


def build_vgg16_GAP(input_shape=(128, 256, 3)):
    vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    #Congelo os layer que não irei treinar
    #Textar deixar os ultimos layers treinaveis
    for layer in vgg_conv.layers[:-5]:
        layer.trainable = False
        
    model = models.Sequential()

    #Adiciono os pesos da VGG16
    for vgg_layer in vgg_conv.layers:
        model.add(vgg_layer)
    
    #Aqui é utilizado Global Averga pooling
    model.add(Lambda(global_average_pooling, 
	              output_shape=global_average_pooling_shape))
    
    model.add(Dense(2, activation = 'softmax', kernel_initializer='uniform'))
	
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(loss = 'binary_crossentropy',optimizer =sgd, metrics=['accuracy'])
                           
    return model