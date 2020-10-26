"""
This model is finetuned from OpenPose. Please see:
https://github.com/CMU-Perceptual-Computing-Lab/openpose_train and
https://github.com/CMU-Perceptual-Computing-Lab/openpose for more details.
"""
from __future__ import division
import os,sys
import cv2
import time
import numpy as np
#import FindCircle
import base64
protoFile="./models/model_1_src/pose_deploy.prototxt"
weightsFile="./models/model_1_src/iter_120000.caffemodel"
threshold=0.1
nPoints=22
POSE_PAIRS=[ [2,4],[5,8],[9,12],[13,16],[17,20],[20,20] ]
net=cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def getDistance(m, n):
    res=np.sqrt(np.sum((m - n) ** 2))
    res=np.around(res, decimals=2)
    return res

def getSkeletonStr(points, vis_circle):
    skeleton_str=''
    for i in range(21):
        try:
            x=points[i][0]
            y=points[i][1]
            if vis_circle==1:
                x=x*2.0
                y=y*2.0
            skeleton_str+=' '+str(x)+' '+str(y)
        except Exception:
            skeleton_str+=' Placeholder Placeholder'
    return skeleton_str

def drawSkeleton(points, frame, color=(0, 0, 255)):
    res=[]
    for pair in POSE_PAIRS:
        partA=pair[0]
        partB=pair[1]
        if points[partA] and points[partB]:
            x=np.array(points[partA])
            y=np.array(points[partB])
            distance=getDistance(x, y)
        if points[partA] and points[partB] and (points[partA] != points[partB]):
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(frame, points[partA], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, points[partB], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            res.append(distance)
            cv2.putText(frame, "{}".format(distance), (points[partB][0],points[partB][1]-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, lineType=cv2.LINE_AA)
    return res, frame

def parseImage1(img_dir, img_name, result_dir, vis_circle):
    if os.path.exists(result_dir+'images_visualization')==False:
        os.mkdir(result_dir+'images_visualization')
    #try:
    img_path=os.path.join(img_dir,img_name)
    frame=cv2.imread(img_path)
    frameCopy=np.copy(frame)
    frameWidth=frame.shape[1]
    frameHeight=frame.shape[0]
    aspect_ratio=frameWidth/frameHeight
    threshold=0.1
    inHeight=368
    inWidth=int(((aspect_ratio*inHeight)*8)//8)
    inpBlob=cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output=net.forward()
    points=[]
    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap=output[0, i, :, :]
        probMap=cv2.resize(probMap, (frameWidth, frameHeight))
        # Find global maxima of the probMap.
        minVal, prob, minLoc, point=cv2.minMaxLoc(probMap)
        if prob > threshold :
            cv2.circle(frameCopy, (int(point[0]), int(point[1])), 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            points.append((int(point[0]), int(point[1])))
        else :
            points.append(None)
    res, frame=drawSkeleton(points, frame, (0, 0, 255))
    if len(res)==5:
        skeleton_str=getSkeletonStr(points, vis_circle)
        cv2.imwrite(result_dir+'images_visualization/'+img_name.split('.')[0]+'_apis_1.'+img_name.split('.')[-1], frame)
        cv2.imwrite(result_dir+'images_visualization/'+ img_name.split('.')[0]+'_apid_1.'+img_name.split('.')[-1], frameCopy)
        with open(result_dir+'images_result_1', 'a') as f:
            f.write(img_name+' '+str(res[0])+' '+str(res[1])+' '+str(res[2])+' '+str(res[3])+' '+str(res[4])+'\n')            
        with open(result_dir+'images_keypoints_1', 'a') as f:
            f.write(img_name+skeleton_str+'\n')            
    else:
        with open(result_dir+'images_failure_1', 'a') as f2:
            f2.write(str(img_name)+'\n')
    '''
    except Exception:
        with open(result_dir+'images_failure_1', 'a') as f3:
            f3.write(str(img_name)+'\n')
            '''
