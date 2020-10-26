from __future__ import division
from models import model_1 
from models import model_2
import cv2
import time
import numpy as np
#import find_circle
import base64
import os,sys
threshold=0.1
#nPoints=22
radius=dict()
name=dict()
def trans(img_len,ra):
    ori_len=float(img_len)*15/ra
    res=str(np.around(ori_len, decimals=2))
    return res

#第一个参数代表是否有经过裁剪的带Logo图，第二个参数表示用了哪个模型
def calActual(model_type,result_dir, preprocess_dir):
    #带logo图片是0.5倍的，直接根据图中的像素计算实际长度
    radius_path=preprocess_dir+'/images_radius.txt'
    with open(radius_path) as f:
        for i in f:
            ii=i.strip().split(' ')
            fname=ii[0].split('.')[0].replace('-','')
            ra=ii[1]
            radius[fname]=ra
            name[fname]=str(ii[0])

    with open(result_dir+'images_final_result_'+str(model_type),'w') as fw:
        with open(result_dir+'images_result_'+str(model_type)) as f:
            for i in f:
                ii=i.strip().split(' ')
                fname=ii[0].split('.')[0].replace('-','')
                if fname in radius.keys():
                    ra=float(radius[fname])
                else:
                    ra=64.6
                thumb=trans(ii[1],ra)
                fore=trans(ii[2],ra)
                middle=trans(ii[3],ra)
                ring=trans(ii[4],ra)
                little=trans(ii[5],ra)
                res=float(ii[2])/float(ii[4])
                tfd=str(np.around(res, decimals=2))
                fw.write(ii[0]+' '+tfd+' '+thumb+' '+fore+' '+middle+' '+ring+' ' +little+'\n')


if __name__ == "__main__":
    #检查文件夹格式
    img_dir='images'
    if os.path.exists(img_dir)==False:
        print("No Such Directory!")
        sys.exit()

    if os.path.exists(img_dir+'_result')==False:
        os.mkdir(img_dir+'_result')
    result_dir='./'+img_dir+'_result/'
    preprocess_dir='./'+img_dir+'_preprocessed'
    cropped_dir='./'+img_dir+'_preprocessed/images_cropped'
    cnt=0
    
    #检测带logo的图片
    with open(preprocess_dir+'/'+img_dir+'_radius.txt') as ft:
        for img in ft:
            if img.find('.jpeg') < 0 and img.find('.jpg') < 0 and img.find('.png') < 0:
                continue 
            cnt+=1
            img_name=img.strip().split(' ')[0]
            #如果带logo，检测cropped文件夹下的图片
            print(cnt,img_name)
            model_1.parseImage1(cropped_dir, img_name, result_dir, 1)
            #第一个参数代表是否有经过裁剪的带Logo图，第二个参数表示用了哪个模型
            model_2.parseImage2(cropped_dir, img_name, result_dir, 1)
    
    print('Images With Logo Is Dond:'+str(cnt))
    cnt=0
    #检测没有logo的图片
    if os.path.exists(preprocess_dir+'/'+img_dir+'_without_logo.txt'):
        with open(preprocess_dir+'/'+img_dir+'_without_logo.txt') as fn:
            for img in fn:
                if img.find('.jpeg') < 0 and img.find('.jpg') < 0 and img.find('.png') < 0:
                    continue 
                cnt+=1
                img_name=img.strip()
                #如果没有logo，检测原文件夹下的图片
                print(cnt,img_name)
                model_1.parseImage1(img_dir, img_name, result_dir, 2)
                model_2.parseImage2(img_dir, img_name, result_dir, 2)
        print('Images Without Logo Is Dond:'+str(cnt))
    #计算实际长度
    
    calActual(1,result_dir,preprocess_dir)
    calActual(2,result_dir,preprocess_dir)
