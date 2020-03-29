# Rafael Scherer
# Métricas IA
"""Este Programa com INPUT sendo as classes de uma lista de dados, as predições
pelo modelo de machine learning da classe de cada valor na lista além da probabilidade
predita para a classe definida pelo modelo, retorna a MATRIZ DE CONFUSÃO, as MÉTRICAS derivadas da matriz,
além de Curva ROC/Precision-Recall e o ponto de corte ótimo do exame com base no Índice de Youden, e os
valores de intervalo de confiança de cada métrica baseados em técnica de Bootstrap"""

import pybootstrap as pb
import numpy
from math import sqrt

# INPUT
goldstandard = [0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1]  # List of class defined by the goldstandard
prediction = [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0,
              0]  # List of predicted class by the Machine Learning Model
predictionprob = [-1, 0.7, -0.5, 0.9, -0.4, -0.4, -0.8, -0.1, 0.9, -0.5, -0.6, 0.2, 0.2, -0.3, 0.9, -0.5,
                  -0.6]  # List of predicted probability for the predicted class

# Confusion Matrix
# Which class represents disease
disease = 1
healthy = 0


# Round Numbers of a list
def arredonda(met):
    for i, c in enumerate(met):
        arred = round(c, 1)
        met[i] = arred
    return met


# Confidence Intervals - Wilson Score
def wilson(p, n, z=1.96):
    p = p / 100
    n = len(n)
    denominator = 1 + z ** 2 / n
    centre_adjusted_probability = p + z * z / (2 * n)
    adjusted_standard_deviation = sqrt((p * (1 - p) + z * z / (4 * n)) / n)

    lower_bound = round((centre_adjusted_probability - z * adjusted_standard_deviation) / denominator, 1) * 100
    upper_bound = round((centre_adjusted_probability + z * adjusted_standard_deviation) / denominator, 1) * 100
    return (lower_bound, upper_bound)


# Confidence Intervals - Bootstrap approach
def confidence(lista, stat):
    bootstrap = pb.bootstrap(lista, confidence=0.95, iterations=10000, sample_size=1.0, statistic=stat)
    return bootstrap


matchlist = list()


def confusionlist(prediction, goldstandard):
    for i, p in enumerate(prediction):
        if disease == p:
            if p == goldstandard[i]:
                matchlist.append(0)  # TP
            elif p != goldstandard[i]:
                matchlist.append(1)  # FP
        if disease != p:
            if p == goldstandard[i]:
                matchlist.append(2)  # TN
            elif p != goldstandard[i]:
                matchlist.append(3)  # FN
    return matchlist


def confusionmatrix(conflist):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i, p in enumerate(prediction):
        if conflist[i] == 0:
            TP += 1
        if conflist[i] == 1:
            FP += 1
        if conflist[i] == 2:
            TN += 1
        if conflist[i] == 3:
            FN += 1
    return TP, FP, TN, FN


# Metrics
def sensv(lista):
    TP = lista.count(0)
    FN = lista.count(3)
    if TP + FN > 0:
        sensivity = 100 * TP / (TP + FN)
    else:
        sensivity = 0
    return sensivity


def spec(lista):
    TN = lista.count(2)
    FP = lista.count(1)
    if TN + FP > 0:
        specificity = 100 * TN / (TN + FP)
    else:
        specificity = 0
    return specificity


def positivepred(lista):
    TP = lista.count(0)
    FP = lista.count(1)
    if TP + FP > 0:
        PPV = 100 * TP / (TP + FP)
    else:
        PPV = 0
    return PPV


def negativepred(lista):
    TN = lista.count(2)
    FN = lista.count(3)
    if TN + FN > 0:
        PNV = 100 * TN / (TN + FN)
    else:
        PNV = 0
    return PNV


def acur(lista):
    TN = lista.count(2)
    FN = lista.count(3)
    TP = lista.count(0)
    FP = lista.count(1)
    Accuracy = 100 * (TP + TN) / (TP + TN + FP + FN)
    return Accuracy


def LRP(lista):
    sensivity = sensv(lista)
    specificity = spec(lista)
    if 100 - specificity > 0:
        LRpos = sensivity / (100 - specificity)
    else:
        LRpos = 0
    return LRpos


def LRN(lista):
    sensivity = sensv(lista)
    specificity = spec(lista)
    if specificity > 0:
        LRneg = (100 - sensivity) / specificity
    else:
        LRneg = 0
    return LRneg


def type1(lista):
    specificity = spec(lista)
    type1error = 100 - specificity
    return type1error


def type2(lista):
    sensivity = sensv(lista)
    type2error = 100 - sensivity
    return type2error


def evaluate(function, lista, namefunction='', printwilson=True, printbootstrap=False):
    if printbootstrap == True:
        conf = confidence(lista, function)
        conf = [conf[0], conf[1]]
        conf = arredonda(conf)
    else:
        conf = 0
    s = round(function(lista), 1)
    w = wilson(s, lista)

    print(f'- {namefunction}: {s} ', end='')
    if printwilson == True:
        print(f'- Wilson Score: {w} ', end='')
    if printbootstrap == True:
        print(f'- Bootstrap: {conf}')
    else:
        print('')
    return s, wilson, conf


conflist = confusionlist(prediction, goldstandard)
confmat = confusionmatrix(conflist)

print(
    '-' * 45 + f'\n Matriz de Confusão (Tabela de Contingência):\n TP: {confmat[0]} FP: {confmat[1]}\n FN: {confmat[3]} TN: {confmat[2]} \n' + '-' * 45)

evaluate(sensv, conflist, 'Sensivity(Recall)', printbootstrap=True)
evaluate(spec, conflist, 'Specificity', printbootstrap=True)
evaluate(positivepred, conflist, 'Positive Preditive Rate (Precision)', printbootstrap=True)
evaluate(negativepred, conflist, 'Negative Preditive Rate', printbootstrap=True)
evaluate(acur, conflist, 'Accuracy', printbootstrap=True)
evaluate(LRP, conflist, 'Likelihood Ratio +', False, printbootstrap=True)
evaluate(LRN, conflist, 'Likelihood Ratio -', False, printbootstrap=True)
evaluate(type1, conflist, 'Type 1 Error', printbootstrap=True)
evaluate(type2, conflist, 'Type 2 Error', printbootstrap=True)

# ROC Curve/Precision Recall Curve
predictiondyn = prediction[:]
youd = list()
false_positive_rate = list()
true_positive_rate = list()
precision = list()

for cutpoint in range(0, 21, 1):
    cutpoint = (cutpoint - 10) / 10
    print(f'Cutpoint: {cutpoint}')
    for i, p in enumerate(predictiondyn):
        if disease == prediction[i]:
            if cutpoint > predictionprob[i]:
                predictiondyn[i] = healthy
            elif cutpoint <= predictionprob[i]:
                predictiondyn[i] = disease
        if healthy == prediction[i]:
            if cutpoint <= predictionprob[i]:
                predictiondyn[i] = disease
            elif cutpoint > predictionprob[i]:
                predictiondyn[i] = healthy

    #    print(predictiondyn)
    #    print(goldstandard)
    ci = confusionlist(predictiondyn, goldstandard)
    c = confusionmatrix(ci)
    #    print(ci)
    #    print(c)

    evaluate(sensv, ci, 'Sensivity(Recall)')
    evaluate(spec, ci, 'Specificity')
    evaluate(positivepred, ci, 'Positive Preditive Rate')
    evaluate(negativepred, ci, 'Negative Preditive Rate')
    evaluate(acur, ci, 'Accuracy')
    evaluate(LRP, ci, 'Likelihood Ratio +', False)
    evaluate(LRN, ci, 'Likelihood Ratio -', False)
    evaluate(type1, ci, 'Type 1 Error')
    evaluate(type2, ci, 'Type 2 Error')

    youden = sensv(ci) + spec(ci) - 100
    print(f'Youden Index: {youden}')

    youd.append(youden)
    false_positive_rate.append(type1(ci))
    true_positive_rate.append(sensv(ci))
    precision.append(positivepred(ci))

    del ci[:]

import matplotlib.pyplot as plt
import numpy as np

false_positive_rate2 = [0.01*x for x in false_positive_rate]
true_positive_rate2 = [0.01*x for x in true_positive_rate]
precision2 = [0.01*x for x in precision]


x = false_positive_rate2
y = true_positive_rate2
z = precision2

# This is the ROC curve
plt.subplot(1,2,1)
plt.title('ROC Curve')
plt.xlabel('1 -Specificity')
plt.ylabel('Sensivity')

plt.plot(x,y,'bo')
plt.plot(x,y)
plt.plot(x,x,'g--')
#plt.savefig('/Users/rafaelscherer/Desktop/ROC.png')

plt.subplot(1,2,2)
plt.title('Precision Recall Curve')
plt.ylabel('PPV (Precision)')
plt.xlabel('Sensivity')
plt.plot(y,z,'bo')
plt.plot(y,z)
#plt.savefig('/Users/rafaelscherer/Desktop/Precion_Recall.png')

# This is the AUC
auc = round(np.trapz(y,x),3)
print(f'Area Under Curve: {auc}')
youdstring = str(round(np.argmax(youd)/10-1,1))
youdmax = round(max(youd),2)
print(f'Cutpoint - Youden Index: (' + youdstring + ') - ('+ str(youdmax) + ')')