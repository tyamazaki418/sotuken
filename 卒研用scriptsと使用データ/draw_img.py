#!/usr/bin/python3
#coding:UTF-8
#縦横比保存
#USAGE: ./draw_img.py 画像横サイズ 画像縦サイズ データファイル名

import numpy as np
import csv
import sys

img_x = int(sys.argv[1]) # 画像サイズ：横
img_y = int(sys.argv[2]) # 画像サイズ：縦
fname = sys.argv[3]

maxpix = 255 #グレースケール最大階調値

img = np.array([float(img_x),float(img_y)])
pix  = np.zeros((img_x,img_y),dtype=int) # 画素値（ゼロで初期化）

#参照、移動の方向
hear,right,left,up,down,up_right = [np.array(list) for list in [[0,0],[1,0],[-1,0],[0,1],[0,-1],[1,1]]]

def setpic (point): #画素値の設定
    #直線が通過するごとに1だけ増やす
#    pix[tuple(point)] = np.min([pix[tuple(point)]+1,maxpix])
    pix[tuple(point)] = 1 #2値画像

def drawline(from_p, dest_p): #from_p-dest_pを結ぶ直線を描画する
  
    dx,dy = dest_p-from_p

    if dx<0: #終点が第2，3象限にある場合は逆向きに描画
        dest_p,from_p = from_p,dest_p
        dx,dy = dest_p-from_p

    n_vec = np.array([dy, -dx]) #直線の法線ベクトル

    start = np.array([int(np.floor(p)) for p in from_p]) #移動の出発点
    endp = np.array([int(np.floor(p)) for p in dest_p]) #移動の終点

    setpic(start) #出発点の画素値を処理

    movp =  np.copy(start) #移動点の初期化
    
    #直線が right と up_right の間を通っているとき right に移動、そうでなければmov2に移動
    #mov2：直線の終点が第1象限にあるとき up、 第4象限にあるとき down
    mov2 = up if dy>=0 else down

    while not (np.allclose(movp,endp)): #移動点が終点に達するまで繰り返し

        vec1 = movp + right - from_p
        vec2 = movp + up_right - from_p

        if np.dot(n_vec,vec1)*np.dot(n_vec,vec2) <= 0: #right と up_right の間を通過
            movp += right
        else:
            movp += mov2
                
        setpic(movp) #移動後の画素値を処理

#データファイルの読み込み
with open(fname,'r') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    dat = np.array([row for row in reader])
    
#描画領域より大きい場合のスケール変換（縦横比は保存）
max,min = np.max(dat,axis=0),np.min(dat,axis=0) #各軸に沿った最大と最小
width,height = max-min #画像のオリジナルサイズ
imgw,imgh = img-1 #描画領域の横・縦の最大値

rat = np.max([width/imgw, height/imgh])
dat = dat/rat #1/ratにリスケール
max,min = (max, min)/rat

#中心が一致するように平行移動
mid = (max+min)/2.0
dat = [row-mid+img/2. for row in dat]
    
#描画    
for i in range(len(dat)-1):
    drawline(dat[i],dat[i+1])

##    
## 画像データの出力
## 
#マジックナンバー：P1 2値画像、P2 グレースケール、P3 カラー
#print ("P2\n %d %d\n%d" % (img_x,img_y,maxpix)) #マジックナンバー 横 縦
print ("P1\n %d %d" % (img_x,img_y)) #マジックナンバー 横 縦
#2値画像の場合は maxpix は入れない

writer = csv.writer(sys.stdout,delimiter=' ',lineterminator='\n')
for row in np.flipud(pix.T): # pix を転置して縦方向に反転（配列の並びの関係で必要）
#    writer.writerow(row)
    writer.writerow((row+1)%2) #反転表示：2値画像
#    writer.writerow(maxpix-row) #反転表示：グレースケール
