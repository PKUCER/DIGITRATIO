from __future__ import division
import cv2
import time
import numpy as np
#import FindCircle
import base64
import os,sys

from .model_2_src.aip import AipBodyAnalysis

APP_ID='22753355'
API_KEY='5Ndxh5smd6w9X8W1BMAf9Fu9'
SECRET_KEY='FFsYOfySVgKj9BGGX23xQfAPLkNxjat0'
threshold=0.1
nPoints=22
POSE_PAIRS=[ [2,4],[5,8],[9,12],[13,16],[17,20],[20,20] ]

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

def getContent(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def fixPoint(frame, frameCopy, img_path, vis_circle):
    client=AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    image= getContent(img_path)    
    content=client.handAnalysis(image)
    points2=['']*23


    skeleton_str=''
    res = ''

    try:
        if content:
            data=content
            result=data['hand_info']
            for hand in result:
                cnt_part=0
                for hand_part in hand['hand_parts']:
                    value=hand['hand_parts'][hand_part]
                    pin=(value['x'],value['y'])
                    points2[int(hand_part)]=pin
                    cv2.circle(frameCopy, pin, 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                    cnt_part+=1
            res, frame=drawSkeleton(points2, frame, (0, 0, 255))

            if len(res)==5:
                skeleton_str=getSkeletonStr(points2, vis_circle)
            else:
                skeleton_str=str(content)

        else:
            skeleton_str = 'response content is null'
    except Exception as e:
        skeleton_str = str(content)+','+str(repr(e))

    return skeleton_str, frame, frameCopy, res

def parseImage2(img_dir, img_name, result_dir, vis_circle):
    img_path=os.path.join(img_dir,img_name)
    frame=cv2.imread(img_path)
    frameCopy=np.copy(frame)
    skeleton_str, frame, frameCopy, res=fixPoint(frame, frameCopy, img_path, vis_circle)
    if len(res) == 5:
        cv2.imwrite(result_dir+'images_visualization/'+img_name.split('.')[0]+'_apis_2.'+img_name.split('.')[-1], frame)
        cv2.imwrite(result_dir+'images_visualization/'+img_name.split('.')[0]+'_apid_2.'+img_name.split('.')[-1], frameCopy)
        with open(result_dir+'images_result_2', 'a') as f:
            f.write(img_name+' '+str(res[0])+' '+str(res[1])+' '+str(res[2])+' '+str(res[3])+' '+str(res[4])+'\n')            
        with open(result_dir+'images_keypoints_2', 'a') as f:
            f.write(img_name+skeleton_str+'\n')             
    else:
        with open(result_dir+'images_failure_2', 'a') as f2:
            f2.write(str(img_name)+','+skeleton_str+'\n')
    
