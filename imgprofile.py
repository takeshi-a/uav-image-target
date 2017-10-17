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

def imgprofile(pathname):
	"""
	実験データファイルのプロファイル取得
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

		csvname = 'filelist_' + pathname + '.csv'
		csvpath = os.path.join(os.getcwd(), 'tmp', csvname)
		try:
			df.to_csv(csvpath, columns=['fname', 'fpath', 'DateTime', 'lat', 'lon', 'alt'])
			print('Saved the profile Successfully here:')
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
	plt.plot(df['lon'], df['lat'], 'bo') 
	plt.plot(df['lon'], df['lat'], 'b-') 

	# 始点（start）と終点（end）のプロットを矢印で示す
	for pos, x, y in zip(['start', 'end'], df['lon'].iloc[[0,-1]], df['lat'].iloc[[0,-1]]):
		plt.annotate(pos, xy=(x,y),
					xytext=(x+lon_span/20.0, y+lat_span/20.0),
					arrowprops=dict(facecolor='black', shrink = 0.05, width=1),
				    horizontalalignment='left', verticalalignment='bottom')	
	plt.show()

def plot_ref(df):
	ref_ID_lst = [30, 33, 35, 38, 41, 44]
	ref_df = df.iloc[ref_ID_lst]
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
	plt.plot(ref_df['lon'], ref_df['lat'], 'ro', markersize=10) 
	plt.plot(df['lon'], df['lat'], 'b-') 

	for i, x, y in zip(range(len(ref_ID_lst)), ref_df['lon'], ref_df['lat']):
		
		pt_str = "pt" + str(i)
		plt.annotate(pt_str, xy=(x,y),
					xytext=(x+lon_span/20.0, y+lat_span/20.0),
					arrowprops=dict(facecolor='black', shrink = 0.05, width=1),
				    horizontalalignment='left', verticalalignment='bottom')	
	plt.show()

def plot_ref2(df):
	# ref_ID_lst = [80:154]
	ref_df2 = df.iloc[201:259]
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
	plt.plot(ref_df2['lon'], ref_df2['lat'], 'bo', markersize=8) 
	plt.plot(df['lon'], df['lat'], 'b-') 

	for i, x, y in zip(ref_df2.index , ref_df2['lon'], ref_df2['lat']):
		pt_str = "{:04d}".format(i)
		plt.annotate(pt_str, xy=(x,y),
					xytext=(x+lon_span * 0.01 , y+lat_span * 0.01),
					arrowprops=dict(facecolor='black', shrink = 0.05, width=1),
				    horizontalalignment='left', verticalalignment='bottom')	


	plt.title('pattern: 4, alt = 80m, DJI_0203-0261.jpg')
	plt.show()


if __name__ == '__main__':
	pathname = input("Enter pathname: ")
	df = imgprofile(pathname)
	draw_map(df)
