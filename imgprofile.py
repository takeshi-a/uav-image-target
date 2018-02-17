"""
imgprofile.py

This module collects drone photo data and creates dataframe.

Takeshi Akutsu 
"""

# collect drone photo image data from folder

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from glob import glob
from gistool import get_GPS, get_datetime

# 画像パラメータ
POLE_RADIUS = 6356752.314   #極半径
EQUATOR_RADIUS = 6378137    #赤道半径

# 高尾実験エリアの四隅の定義（緯度、経度）
left_bottom = (35.699241, 139.235341) # pt1, 左下
right_bottom = (35.699241, 139.235588) # pt2, 右下
right_top = (35.699466, 139.235588) # pt3,右上
left_top = (35.699466, 139.235341) # pt4, 左上


# # 飛行エリアの四隅の定義（緯度、経度）
# left_bottom = (35.798097, 138.121126) # pt1, 左下
# right_bottom = (35.797269, 138.123157) # pt2, 右下
# right_top = (35.803047, 138.126746) # pt3,右上
# left_top = (35.803874, 138.124729) # pt4, 左上


# 四隅をnp.arrayにまとめる
corners = np.array([left_bottom, right_bottom, right_top, left_top])

# 飛行エリアの中心座標
lat_center, lon_center = corners.mean(axis=0)
center = (lat_center, lon_center)
MYLATITUDE = lat_center
MYLONGITUDE = lon_center

# 緯度差をY軸距離に変換する
def d_lat2dy(d_lat):
    dy = POLE_RADIUS * d_lat * pi / 180
    return dy

# 経度差をX軸距離に変換する
def d_lon2dx(d_lon):
    dx = EQUATOR_RADIUS * cos(MYLATITUDE * pi / 180) * d_lon * pi / 180
    return dx


def imgprofile(pathname):
	"""
	実験データファイルのプロファイル取得
	指定したフォルダ内のすべてのJPGファイルのメタデータを取得する
	Input:
		pathname: 画像データのフォルダ名
	Output:
		df: メタデータのデータフレーム
			fname: ファイル名
			fpath: absolute file path
			DateTime: time stamp of image file
			lat: latitude [DEG]
			lon: longitude [DEG]
			alt: altitude [m]
	"""
	imgpath = os.path.join(os.getcwd(), pathname)
	if os.path.exists(imgpath) == False:
		print("NG! The pathname is invalid.")
		print("DataFrame with empty data is returned.")
		df = pd.DataFrame({})
	else:
		print("OK! The pathname is valid.")

		imglst = glob(os.path.join(imgpath, '*.JPG'))
		df = pd.DataFrame(imglst, columns=["fpath"])
		df['fname'] = df['fpath'].map(os.path.basename)
		df['DateTime'] = df['fpath'].map(get_datetime)
		gps_keys = ['lat', 'lon', 'alt']
		for k in gps_keys:
			df[k] = df['fpath'].map(get_GPS).apply(pd.Series)[k].apply(pd.Series)

		csvname = pathname + '_flist.csv'
		csvpath = os.path.join(os.getcwd(), csvname)
		try:
			df.to_csv(csvpath, columns=['fname', 'fpath', 'DateTime', 'lat', 'lon', 'alt'])
			print('Saved the profile data in:')
			print(csvpath, '\n')
		except:
			print('Warning: Failed to save the profile data!\n')
	return df

def draw_map(df):
	"""
	データファイル全てのジオタグ座標をまとめてグラフに出力し、飛行経路を表示する
	Input:
		df: データフレーム
	"""
	lat_max = df['lat'].max()
	lat_min = df['lat'].min()
	lat_span = abs(lat_max - lat_min)
	lon_max = df['lon'].max()
	lon_min = df['lon'].min() 
	lon_span = abs(lon_max - lon_min)
	bottom_left = [lon_min - 0.05 * lon_span, lat_min - 0.05 * lat_span] 
	top_right = [lon_max + 0.05 * lon_span, lat_max + 0.05 * lat_span]
	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot(111)
	plt.xlim(bottom_left[0], top_right[0])
	plt.ylim(bottom_left[1], top_right[1])
	plt.xlabel('lon')
	plt.ylabel('lat')
	plt.title('plot map: {}'.format(pathname))
	plt.plot(df['lon'], df['lat'], 'bo') 
	plt.plot(df['lon'], df['lat'], 'b-') 

	corners_T = corners.T
	plt.plot(np.vstack((corners, corners[0])).T[1], np.vstack((corners, corners[0])).T[0], 'r--')

	# 始点（start）と終点（end）のプロットを矢印で示す
	for fname, x, y in zip(df.fname.loc[::10], df.lon.loc[::10], df.lat.loc[::10]):
		if fname[:3] == 'DJI':
			fnum = fname.split('_')[1].split('.')[0]
		else:
			fnum = fname.split('.')[0]

		plt.annotate(fnum, xy=(x,y),
					xytext=(x+lon_span/20.0, y+lat_span/25.0),
					arrowprops=dict(facecolor='black', shrink = 0.05, width=1),
				    horizontalalignment='left', verticalalignment='bottom')	

	plt.show()

if __name__ == '__main__':
    print('### Retrieve EXIF data ###\n')
	pathname = input("Enter pathname: ")
	df = imgprofile(pathname)
	draw_map(df)
