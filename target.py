"""
target.py

This module processes GIS data of drone images.

Takeshi Akutsu 
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from math import pi, cos, sin
import gistool
from gistool import get_GPS, deg2dms, dms2deg
from imgprofile import imgprofile, draw_map
from PIL import Image
# import glob

# 画像パラメータ
POLE_RADIUS = 6356752.314   #極半径
EQUATOR_RADIUS = 6378137    #赤道半径

# 画像の方位角（上向きの角度。真北を基準として反時計回りに角度表示）
img_dir = 0

# 画像処理クラス
class clicker_class(object):
    def __init__(self, ax):
        self.canvas = ax.get_figure().canvas
        self.pt_lst = []
        self.pt_plot = ax.plot([], [], marker='o', color='r',
                               linestyle='none', zorder=5, markersize=10)[0]
        self.connect()

    def connect(self):
        self.cidbutton = self.canvas.mpl_connect('button_press_event',
                                                self.click_event)
        # self.cidkeypress = self.canvas.mpl_connect('key_press_event', 
        #                                         self.press)

    # def press(self, event):
    #     print('press', event.key)

    def click_event(self, event):
        ''' Extracts locations from the user'''
        print(event)
        if event.button == 1:
            self.pt_lst.append((event.xdata, event.ydata))
        elif event.button == 3:
            self.remove_pt((event.xdata, event.ydata))

        self.redraw()

    def remove_pt(self, loc):
        if len(self.pt_lst) > 0:
            self.pt_lst.pop(np.argmin(map(lambda x:
                                          np.sqrt((x[0] - loc[0]) ** 2 +
                                                  (x[1] - loc[1]) ** 2),
                                          self.pt_lst)))

    def redraw(self):
        if len(self.pt_lst) > 0:
            x, y = zip(*self.pt_lst)
        else:
            x, y = [], []
        self.pt_plot.set_xdata(x)
        self.pt_plot.set_ydata(y)
        self.canvas.draw()


def draw_target_pts(img):
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    px_high, px_wid = img.shape[:2]
    plt.imshow(img)
    plt.axis('off')
    plt.plot(px_wid/2, px_high/2, 'r*', markersize=10)
    cc = clicker_class(ax)
    plt.show()  
    return cc.pt_lst

def make_df(pt_lst, imgpath):
    # 目標点リストのデータフレームの作成
    df = pd.DataFrame(pt_lst, columns= ['xdata', 'ydata'])
    gps = get_GPS(imgpath)

    # 画像のピクセル高（px_high）とピクセル幅（px_wid）を抽出
    px_high, px_wid = np.array(Image.open(imgpath)).shape[:2]

    # ファイル名の登録
    df['file'] = os.path.basename(imgpath)
    # 画像座標の変換：原点を左上から画像中心へ、Y軸を反転
    df['xdata_trans'] = df['xdata'] - (px_wid / 2)
    df['ydata_trans'] = - df['ydata'] + (px_high / 2)
    # 画像座標の単位変換：ピクセルからメートルへ
    df['x_meter'] = img_size_h / px_wid * df['xdata_trans']
    df['y_meter'] = img_size_v / px_high * df['ydata_trans']
    # 方位角の回転補正
    df['x_target'] = cos(img_dir * pi / 180.0) * df['x_meter'] + sin(img_dir * pi / 180.0) * df['y_meter']
    df['y_target'] = - sin(img_dir * pi / 180.0) * df['x_meter'] + cos(img_dir * pi / 180.0) * df['y_meter']

    # 座標中心からの距離を緯度・経度に変換
    # x座標をDEG形式およびDMS形式の経度に変換
    df['x_deg'] = df['x_target'] * 180 / (pi * EQUATOR_RADIUS * cos(gps['lat'] * pi / 180.0))
    df['lon_deg'] = gps['lon'] + df['x_deg']
    df['lon_dms'] = df['lon_deg'].map(deg2dms)
    # y座標をDEG形式およびDMS形式の経度に変換
    df['y_deg'] = df['y_target'] / POLE_RADIUS * 180 / pi
    df['lat_deg'] = gps['lat'] + df['y_deg']
    df['lat_dms'] = df['lat_deg'].map(deg2dms)

    return df



if __name__ == '__main__':
    pathname = input("Enter pathname: ")
    img_df = imgprofile(pathname)
    draw_map(img_df)

    # 撮影の対地高度
    height = input('Enter elevation height of image:')
    if height == "":
        height = 100
    height = float(height)

    # ccd_num_v = 3456 # num of ccd images vertical, 3456 for X4, 3956 for X5S 
    # ccd_num_h = 4608 # num of ccd images horizontal, 4608 for X4, 5280 for X5S

    ccd_size_v = 13     # vertical ccd image size [mm]
    ccd_size_h = 17.3   # horizontal ccd image size [mm]

    f_length = 25 # focal length [mm]

    img_size_v = ccd_size_v/float(f_length)*height
    img_size_h = ccd_size_h/float(f_length)*height


    target_df = pd.DataFrame({})
    while True:

        id_num = input('Enter image ID num (ex: 0001 > DJI_0001.JPG)\nID num:')
        if len(id_num)!=4:
            print('Invalid number, enter 4 digits!')
        else:
            imgfile = 'DJI_' + str(id_num) + '.JPG'
            imgpath = os.path.join(os.getcwd(), pathname, imgfile)
            print('data loaded: ' + imgfile)
            try:
                img = np.array(Image.open(imgpath))
                pt_lst = draw_target_pts(img)
                df = make_df(pt_lst, imgpath)
                print('added {} points\n'.format(df.shape[0]))
                target_df = target_df.append(df, ignore_index=True)

            except:
                print('File Not Exist\n')

        key = input('continue? [y/n]')
        if key == 'n':
            print('Stopped process.\n')
            break

    print('total {} points\n'.format(target_df.shape[0]))
    print(target_df[['file', 'lat_deg', 'lon_deg']])
    # csvname = 'result_' + '{:03d}'.format(int(height)) + 'm.csv'
    targetcsv = 'target_' + pathname + '.csv'
    try:
        target_df.to_csv(targetcsv, columns=['file', 'lat_deg', 'lon_deg',
                                                'xdata', 'ydata', 'xdata_trans', 'ydata_trans', 'x_meter', 'y_meter',
                                                'x_target', 'y_target', 'x_deg', 'y_deg'
                                                ])
        print("Target points are saved as {}".format(targetcsv))
    except PermissionError:
        print('PermissionError')