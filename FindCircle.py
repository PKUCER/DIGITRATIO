import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests 
import json
import urllib
import base64
import json
import time
import os,sys
import scipy as sp
while_thres=180

def skinMask(roi):
	YCrCb=cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB) 
	(y,cr,cb)=cv2.split(YCrCb) 
	cr1=cv2.GaussianBlur(cr, (5,5), 0)
	_, skin=cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Ostu处理
	res=cv2.bitwise_and(roi,roi, mask=skin)
	return res

def removeBG(frame): 
    bgModel=cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)
    fgmask=bgModel.apply(frame, learningRate=0.1) 
    kernel=np.ones((3, 3), np.uint8)
    fgmask=cv2.erode(fgmask, kernel, iterations=1) 
    res=cv2.bitwise_and(frame, frame, mask=fgmask) 
    return res

def cropMargin(binary_image,img):
    height=binary_image.shape[0]
    width=binary_image.shape[1]
    up=0
    down=height
    for i in range(height): 
        cnt_hei=0
        for j in range(width):
            if binary_image[i][j].all()==0:
                cnt_hei+=1
        if cnt_hei > 0.9*width:
            if i < height/2:
                up=max(i,up)
            else:
                down=min(i,down)
        else:
            break

    for i in range(height-1,-1,-1): 
        cnt_hei=0
        for j in range(width):
            if binary_image[i][j].all()==0:
                cnt_hei+=1
        if cnt_hei > 0.9*width:
                down=min(i,down)
        else:
            break
    left=0
    right=width
    for i in range(width): 
        cnt_wid=0
        for j in range(height):
            if binary_image[j][i].all()==0:
                cnt_wid+=1
        if cnt_wid > 0.9*height:
            if i < width/2:
                left=max(i,left)
            else:
                right=min(i,right)
        else:
            break

    for i in range(width-1,-1,-1): #iterate lie
        cnt_wid=0
        for j in range(height):
            if binary_image[j][i].all()==0:
                cnt_wid+=1
        if cnt_wid > 0.9*height:
            if i < width/2:
                left=max(i,left)
            else:
                right=min(i,right)
        else:
            break

    pre1_picture=img[up:down,left:right]        
    return pre1_picture    

def dumpRotateImage(img,degree):
    height, width=img.shape[:2]
    heightNew=int(width * np.fabs(np.sin(np.radians(degree)))+height * np.fabs(np.cos(np.radians(degree))))
    widthNew=int(height * np.fabs(np.sin(np.radians(degree)))+width * np.fabs(np.cos(np.radians(degree))))
    matRotation=cv2.getRotationMatrix2D((width//2, height//2), degree, 1)
    matRotation[0,2]+=(widthNew - width)//2
    matRotation[1,2]+=(heightNew - height)//2
    imgRotation=cv2.warpAffine(img, matRotation,(widthNew,heightNew),borderValue=(255,255,255))
    return imgRotation

def findCircle(g,img):
    yuan0=cv2.HoughCircles(g,cv2.HOUGH_GRADIENT,1,
                            100,param1=100,
                            param2=10,
                            minRadius=0,
                            maxRadius=50)
    yuans=yuan0[0,:,:]
    yuan=np.uint16(np.around(yuans))
    circle_x=0
    circle_y=0
    circle_r=10000
    res=[]

    for i in yuan[:]: 
        xx=int(i[0])
        yy=int(i[1])
        rr=int(i[2])
        if xx-rr <0:
            left=1
        else:
            left=xx-rr
        if yy-rr <0:
            down=1
        else:
            down=yy-rr
        right=min(i[0]+i[2],img.shape[1])
        up=min(i[1]+i[2],img.shape[0])
        cnt=0
        for ii in range(down, up-1):
            for jj in range(left, right-1):
                if img[ii][jj][0] >=while_thres and img[ii][jj][1] >=while_thres and img[ii][jj][2] >=while_thres:
                    cnt+=1
        if cnt > 0.5*i[2]*i[2] and (xx< 0.3 * img.shape[1] or xx > 0.7 * img.shape[1]) and (yy< 0.3 * img.shape[0] or yy > 0.7 * img.shape[0]):
            if rr<circle_r:
                circle_r=rr
                circle_x=xx
                circle_y=yy
                res.append(circle_r)
                cv2.circle(img,(circle_x,circle_y),circle_r,(255,0,0),thickness=-1,lineType=cv2.FILLED)
                if img.shape[1] > img.shape[0]: #width>height
                    if xx < 0.3 * img.shape[1]: # on the left
                        trans=dumpRotateImage(img,90)
                        img=cv2.flip(trans, 0)
                    elif xx > 0.7 * img.shape[1]: #on the right
                        trans=dumpRotateImage(img,90)
                        img=cv2.flip(trans, 1)
                else:
                    #print(img.shape)
                    if yy > 0.7 * img.shape[0]:
                        img=dumpRotateImage(img,90)
                        img=dumpRotateImage(img,90)
    res.sort(reverse=True)
    circle_r=res[0]
    return img,circle_r

def findRadius(filepath): #find logo radius and rotate the image with 0.5 size 
    img=cv2.imread(filepath)#image read be 'gray'
    img=cv2.resize(img,(int(0.5*img.shape[1]),int(0.5*img.shape[0])))
    img=cv2.bilateralFilter(img,9,75,75)
    roi=img
    res=skinMask(roi) #进行肤色检测
    kernel=np.ones((3,3), np.uint8) #设置卷积核
    erosion=cv2.erode(res, kernel) #腐蚀操作
    erosion=cv2.erode(erosion, kernel) #腐蚀操作
    erosion=cv2.erode(erosion, kernel) #腐蚀操作
    erosion=cv2.erode(erosion, kernel) #腐蚀操作
    img=cropMargin(res,img)
    img2=cropMargin(res,res)
    origin=img
    binaryimg_convex=cv2.Canny(img2, 0, 255) #二值化，canny检测
    cv2.waitKey(0)
    ret,thresh=cv2.threshold(binaryimg_convex,0,255,0)
    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img,res=findCircle(binaryimg_convex,img)
    return img, res

def parseImage(img_dir,img_name,result_dir):
    try:
        cropped_dir=result_dir+'_cropped'
        if os.path.exists(cropped_dir)==False:
            os.mkdir(cropped_dir)
        img_path=os.path.join(img_dir,img_name)
        frame,res=findRadius(img_path)
        radius=res
        if res < 10000:
            with open(result_dir+'_radius.txt','a') as f1:
                cv2.imwrite(os.path.join(cropped_dir,img_name),frame)
                f1.write(str(img_name)+' '+str(radius)+'\n')
        else:
            with open(result_dir+'_without_logo.txt', 'a') as f:
                f.write(str(img_name)+'\n')

    except Exception:
        with open(result_dir+'_without_logo.txt', 'a') as f:
            f.write(str(img_name)+'\n')


if __name__=="__main__":
    img_dir='images'
    #检查文件夹格式
    if os.path.exists(img_dir)==False:
        print("No Such Directory!")
        sys.exit()

    if os.path.exists(img_dir+'_preprocessed')==False:
        os.mkdir(img_dir+'_preprocessed')

    result_dir='./'+img_dir+'_preprocessed/'+img_dir
    with open(result_dir+'_list.txt','w') as f:
        for i in os.listdir(img_dir):
            f.write(str(i)+'\n')
    file_list=result_dir+'_list.txt'
    cnt=0
    with open(file_list) as f:
        for img in f:
            if img.find('.jpeg') < 0 and img.find('.jpg') < 0 and img.find('.png') < 0:
                continue 
            cnt+=1
            img_name=img.strip()
            print(img_name,cnt)
            parseImage(img_dir,img_name,result_dir)
