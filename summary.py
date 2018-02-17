import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

csvlist = glob.glob('target_*.csv')

frames = []
for csv in csvlist:
	rdf = pd.read_csv(csv, index_col=0)
	frames.append(rdf)

result = pd.concat(frames)

# result.columns
# Index(['file', 'lat_deg', 'lon_deg', 'dir_sgn', 'img_dir', 'xdata', 'ydata',
#        'xdata_trans', 'ydata_trans', 'x_meter', 'y_meter', 'x_target',
#        'y_target', 'x_deg', 'y_deg'],
#       dtype='object')

csvlist2 = glob.glob('*_flist.csv')

frames2 = []
for csv in csvlist2:
	route_df = pd.read_csv(csv, index_col=0)
	frames2.append(route_df)

route = pd.concat(frames)


def result_map(route, result):
	"""
	データファイル全てのジオタグ座標をまとめてグラフに出力し、飛行経路を表示する
	Input:
		df: データフレーム
	"""
	lat_max = route['lat'].max()
	lat_min = route['lat'].min()
	lat_span = abs(lat_max - lat_min)
	lon_max = route['lon'].max()
	lon_min = route['lon'].min() 
	lon_span = abs(lon_max - lon_min)
	bottom_left = [lon_min - 0.05 * lon_span, lat_min - 0.05 * lat_span] 
	top_right = [lon_max + 0.05 * lon_span, lat_max + 0.05 * lat_span]
	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot(111)
	plt.xlim(bottom_left[0], top_right[0])
	plt.ylim(bottom_left[1], top_right[1])
	plt.xlabel('lon')
	plt.ylabel('lat')
	plt.title('plot map: ALL results'.format(pathname))
	plt.plot(route['lon'], route['lat'], 'bo') 
	plt.plot(route['lon'], route['lat'], 'b-') 
	plt.plot(result['lon_deg'], result['lat_deg'], 'r*', markersize=5)


# 	corners_T = corners.T
# 	plt.plot(np.vstack((corners, corners[0])).T[1], np.vstack((corners, corners[0])).T[0], 'r--')

# 	# 始点（start）と終点（end）のプロットを矢印で示す
# 	for fname, x, y in zip(df.fname.loc[::10], df.lon.loc[::10], df.lat.loc[::10]):
# 		if fname[:3] == 'DJI':
# 			fnum = fname.split('_')[1].split('.')[0]
# 		else:
# 			fnum = fname.split('.')[0]

# 		plt.annotate(fnum, xy=(x,y),
# 					xytext=(x+lon_span/20.0, y+lat_span/25.0),
# 					arrowprops=dict(facecolor='black', shrink = 0.05, width=1),
# 				    horizontalalignment='left', verticalalignment='bottom')	

# 	plt.show()

