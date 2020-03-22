# -*- coding: utf-8 -*-
import tensorflow.keras as keras
import numpy as np
import cv2

def generate_cam(img_path,model,img_shape=(256,256)):
    #Aqui carrego uma imagem para texte somente
    img =  keras.preprocessing.image.load_img(img_path, 
                                              target_size=img_shape,
                                              interpolation='nearest')    
    
    
    
    #Verificar o processamento na entrada e na saida da imagem.
    #divergencias no pre-processamento da imagem pode causar instabilidade no funcionamento do modelo
    x = keras.preprocessing.image.img_to_array(img)
    x = x*1./255
    #x = ((x-x.mean())/x.std())
    
    x = np.expand_dims(x, axis=0)
    
    
    
    
    pred = model.predict(x)
    
    
    class_output = model.output[:,1]
    last_conv_layer = model.get_layer('block5_conv3')#Esse é o nome do ultimo layer de convoluçõa da rede
    
    
    
    
    
    grads = keras.backend.gradients(class_output, last_conv_layer.get_output_at(-1))[0]
    
    pooled_grads = keras.backend.mean(grads, axis=(0, 1, 2))
    iterate = keras.backend.function([model.input], [pooled_grads, last_conv_layer.get_output_at(-1)[0]])
    
    
    pooled_grads_value, conv_layer_output_value = iterate([x])
    
    for i in range(512):
        conv_layer_output_value[:, :, i] *=  pooled_grads_value[i] 
    
    
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    
    
    
    #Cuidamos do préprocessamento básico da imagem
    
    
    img = cv2.imread(img_path)
    #img = cv2.resize(im, (960, 540))  
    
    #Regulamos a estética do mapa de calor
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    
    
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    superimposed_img = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    
    return img,superimposed_img,pred
