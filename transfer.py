import cv2
import glob
import os

dw = 1./640
dh = 1./400

for im_path in os.listdir('pos'):
    #print im_path
    file1 = open('labels/'+im_path,'w')
    f = open('pos/'+im_path)
    lines = f.read().split('\n')
    for line in lines:
        if len(line)>2:
            l = line.split(' ')
            n1 = (float(l[0])+float(l[2]))/2.0
            n2 = (float(l[1])+float(l[3]))/2.0
            n3 = float(l[2]) - float(l[0])
            n4 = float(l[3]) - float(l[1])
            l1 = n1*dw
            l2 = n2*dh
            l3 = n3*dw
            l4 = n4*dh
            info = '0 '+str(l1)+' '+str(l2)+' '+str(l3)+' '+str(l4)
            file1.write(info)
            file1.close()
