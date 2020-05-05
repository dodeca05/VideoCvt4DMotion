import cv2
import numpy as np
import os
import pickle
import struct
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def analysis(VideoPath, prc, name, number):
    cap = cv2.VideoCapture(VideoPath)
    ret, frame = cap.read()
    _, width, _ = frame.shape

    FilePath = VideoPath.split('.')
    FilePath = FilePath[0]
    print("파일 확인")
    
    try:
        with open("./" + name + "_xpos/" + number + "_" + name + '_xpos.pkl', "rb") as f:
            x_data = pickle.load(f)
            print("x data 확인")
    except:
        print("xpos파일 없음")
        exit()

    try:
        with open("./" + name + "_ypos/" + number + "_" + name + '_ypos.pkl', "rb") as f:
            y_data = pickle.load(f)
            print("y data 확인")
    except:
        print("ypos파일 없음")
        exit()

    try:
        with open("./" + name + "_zpos/" + number + "_" + name + '_zpos.pkl', "rb") as f:
            z_data = pickle.load(f)
            print("z data 확인")
    except:
        print("zpos파일 없음")
        exit()

    try:
        with open('./' + name + "_hist/" + number + "_" + name + '_hist.pkl', "rb") as f:
            hist_data = pickle.load(f)
            print("hist data 확인")
    except:
        print("hist파일 없음")
        exit()
    print("파일 확인 완료")

    #Fuzzy 함수 구현
    dx = ctrl.Antecedent(np.arange(0, 11, 1), 'dx')
    dy = ctrl.Antecedent(np.arange(0, 11, 1), 'dy')
    dz = ctrl.Antecedent(np.arange(0, 11, 1), 'dz')
    hist = ctrl.Antecedent(np.arange(0, 11, 1), 'hist')
    move = ctrl.Consequent(np.arange(0, 11, 1), 'move')

    dx.automf(3)
    dy.automf(3)
    dz.automf(3)
    hist.automf(3)

    move['low'] = fuzz.trimf(move.universe, [0, 0, 5])
    move['medium'] = fuzz.trimf(move.universe, [0, 5, 10])
    move['high'] = fuzz.trimf(move.universe, [5, 10, 10])

    rule1 = ctrl.Rule(dx['poor'] & hist['poor'], move['low'])
    rule2 = ctrl.Rule(dx['poor'] & hist['average'], move['low'])
    rule3 = ctrl.Rule(dx['poor'] & hist['good'], move['high'])
    rule4 = ctrl.Rule(dx['average'] & hist['poor'], move['low'])
    rule5 = ctrl.Rule(dx['average'] & hist['average'], move['medium'])
    rule6 = ctrl.Rule(dx['average'] & hist['good'], move['high'])
    rule7 = ctrl.Rule(dx['good'] & hist['poor'], move['medium'])
    rule8 = ctrl.Rule(dx['good'] & hist['average'], move['high'])
    rule9 = ctrl.Rule(dx['good'] & hist['average'], move['high'])

    rule10 = ctrl.Rule(dy['poor'] & hist['poor'], move['low'])
    rule11 = ctrl.Rule(dy['poor'] & hist['average'], move['medium'])
    rule12 = ctrl.Rule(dy['poor'] & hist['good'], move['high'])
    rule13 = ctrl.Rule(dy['average'] & hist['poor'], move['low'])
    rule14 = ctrl.Rule(dy['average'] & hist['average'], move['high'])
    rule15 = ctrl.Rule(dy['average'] & hist['good'], move['high'])
    rule16 = ctrl.Rule(dy['good'] & hist['poor'], move['medium'])
    rule17 = ctrl.Rule(dy['good'] & hist['average'], move['high'])
    rule18 = ctrl.Rule(dy['good'] & hist['average'], move['high'])

    rule19 = ctrl.Rule(dz['poor'] & hist['poor'], move['low'])
    rule20 = ctrl.Rule(dz['poor'] & hist['average'], move['medium'])
    rule21 = ctrl.Rule(dz['poor'] & hist['good'], move['high'])
    rule22 = ctrl.Rule(dz['average'] & hist['poor'], move['low'])
    rule23 = ctrl.Rule(dz['average'] & hist['average'], move['high'])
    rule24 = ctrl.Rule(dz['average'] & hist['good'], move['high'])
    rule25 = ctrl.Rule(dz['good'] & hist['poor'], move['medium'])
    rule26 = ctrl.Rule(dz['good'] & hist['average'], move['high'])
    rule27 = ctrl.Rule(dz['good'] & hist['good'], move['high'])

    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    #y data 가공
    y_scalar = []
    y_move = []
    y_move.append(0)
    for i in range(0, len(y_data) - 1):
##        diff_x = (y_data[i+1][0] - y_data[i][0])**2
##        diff_y = (y_data[i+1][1] - y_data[i][1])**2
            
##        if sig==1:
##            y_scalar.append(np.sqrt(diff_x + diff_y)
##        else:
##            y_scalar.append(-np.sqrt(diff_x + diff_y)

        if y_data[i+1][1] - y_data[i][1] >0:
            y_move.append(-(50 * y_data[i+1][0] / width - 25))
        else:
            y_move.append(50 * y_data[i+1][0] / width - 25)
    
    
    
##    y_scalar = []
##    y_move = []
##    for i in range(0, len(y_data) - 1):
##        y_scalar.append(np.sqrt((y_data[i+1][0] - y_data[i][0])**2 + (y_data[i+1][1] - y_data[i][1])**2))
##    y_std = np.std(y_scalar)
##    y_avg = np.mean(y_scalar)
##    y_move.append(0)
##    hist_std = np.std(hist_data)
##    hist_avg = np.mean(hist_data)
##    hist_move = []
##    move = 0
##    for i in range(0, len(y_scalar)):
##        #y 움직임 or 히스트 변화가 표준편차보다 클 경우
##        if y_scalar[i] > y_avg + y_std or y_scalar[i] < y_avg - y_std or hist_data[i] > hist_avg + hist_std or hist_data[i] < hist_avg - hist_std:
##            move = 1
##        y_move.append(move)
##        move = 0

    if len(hist_data) < len(x_data):
        hist_data.append(np.mean(hist_data))

    x_output = [0] * len(x_data)
    for i, x in enumerate(sorted(range(len(x_data)), key=lambda y: x_data[y])):
        x_output[x] = 10 * i / len(x_data)

    y_output = [0] * len(y_move)
    for i, x in enumerate(sorted(range(len(y_move)), key=lambda y: y_move[y])):
        y_output[x] = 10 * i / len(y_move)

    z_output = [0] * len(z_data)
    for i, x in enumerate(sorted(range(len(z_data)), key=lambda y: z_data[y])):
        z_output[x] = 10 * i / len(z_data)

    hist_output = [0] * len(hist_data)
    for i, x in enumerate(sorted(range(len(hist_data)), key=lambda y: hist_data[y])):
        hist_output[x] = 10 * i / len(hist_data)
    

    file = open("./" + name + "_4ds/" + number + "_" + name + ".4ds", "wb")
    bf = struct.pack("i", len(x_data))
    file.write(bf)
    for i in range(len(x_data)):
        tipping.input['dx'] = x_output[i]
        tipping.input['dy'] = y_output[i]
        tipping.input['dz'] = z_output[i]
        tipping.input['hist'] = hist_output[i]
        tipping.compute()
        if tipping.output['move'] < 6.5:
            x_data[i] = 0
            y_move[i] = 0
            z_data[i] = 0
        
        bf = struct.pack("i", int(x_data[i]))
        file.write(bf)
        bf = struct.pack("i", int(y_move[i]))
        file.write(bf)
        bf = struct.pack("i", int(z_data[i]))
        file.write(bf)
    file.close()
    os.remove('./' + name + "_xpos/" + number + "_" + name + '_xpos.pkl')
    os.remove('./' + name + "_ypos/" + number + "_" + name + '_ypos.pkl')
    os.remove('./' + name + "_zpos/" + number + "_" + name + '_zpos.pkl')
    os.remove('./' + name + "_hist/" + number + "_" + name + '_hist.pkl')
