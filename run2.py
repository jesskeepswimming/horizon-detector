import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os
import sys
from tqdm import tqdm
import time
import json

def cost(p1,p2, gp1, gp2):
    y0 = abs(p1[1] - gp1[1])
    yw = abs(p2[1] - gp2[1])
    return y0 + yw

if len(sys.argv) != 2:
    print('Please input a folder name.')
    exit()
ts = str(int(time.time()))

folder = sys.argv[1]
os.mkdir(folder+'_result_'+ts) 

gt_data = {}
with open(folder + '/ground_truth.json') as f:
    gt_data = json.load(f)

max_l1 = (0,0)
max_l2 = (0,0)
y1 = 0
y2 = 0
costs = []
for filename in tqdm(os.listdir(folder)):
    if filename.endswith(".jpg"):
        img = cv.imread(folder+'/'+filename,1)
        dimensions = img.shape
        height = img.shape[0]
        width = img.shape[1]
        edges = cv.Canny(img,100,200)
        cdst = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

        lines = cv.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)
        max_d = 0
        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                slope = -a/b

                h = math.hypot(theta1, theta2)
                cv.line(cdst, pt1, pt2, (0,255,0), 3, cv.LINE_AA)
                if max_d < h:
                    max_l1 = pt1
                    max_l2 = pt2
                    max_d = h
                    y1 = int(slope * (0-max_l1[0]) + max_l1[1])
                    y2 = int(slope * (width-max_l1[0]) + max_l1[1])

        cv.line(img, (0, y1), (width, y2), (0,0,255), 3, cv.LINE_AA)
        cv.line(img, max_l1, max_l2, (0,255,0), 3, cv.LINE_AA)
        cv.imwrite(folder+'_result_' + ts +'/' +filename.replace('.jpg', 'canny.jpg') , cdst)
        cv.imwrite(folder+'_result_' + ts +'/' +filename, img)
        c = cost((0, y1),(width, y2), gt_data[filename]["left"], gt_data[filename]["right"])
        costs.append(c)

cost_metric = sum(costs)/len(costs)
print('Metric: ', cost_metric)
