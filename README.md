# Module for GIS position extracting of UAV images 
## Extracting GIS info from UAV images
This module was originally made for a competition in which
competitors detect dummy dear in forest using auto-flight UAV.
You can extract the lat & lon from JPEG images taken by UAV.

## 1. Python modules
### imgprofile.py
Extract meta data from images and create SQLite DB 
- Make a image flie list to pick up
- Extract EXIF data
- Create a pandas DataFrame

### gistool.py
Original module imported in imaprofile.py that wrangles EXIF mata data and create a pandas DataFrame
which contains timestamp, lat, lon, etc.

### target.py
GUI module in which you can extract lat, lon by clicking the target points to pick up. 
- Click the points in image on matplotlib GUI
- Estimate (X,Y) on the image
- Convert (X,Y) to (lon, lat)

## 2. Jupyter Notebook
### estimate.ipynb
For estimation of algorithm.

### data_sandbox.ipynb
For scratch data.

### estimate_tolerance.ipynb
For tolerance estimation of position gap in meter.

### evaluate_result.ipynb
For evaluation of experiment data.

### flight_area.ipynb
For estimation of flight area of competition


# UAV画像のGIS座標抽出モジュール
##座標抽出システム
鹿検知コンペのための座標抽出プログラム。
指定した画像の中から任意の点の座標を抽出する。

## 1. Python modules
### imgprofile.py
画像ファイルのプロファイルを読み込み、データフレームを作る

- 画像ファイルの指定
- 画像のGPSデータを抽出
- 対地高度の設定

### gistool.py
画像のEXIFメタデータを取得して、タイムスタンプやGISデータを処理するモジュール

### target.py
画像上にある任意の点をクリックして、座標を抽出するGUIモジュール

- 画像上のプロットの指定
- プロットのXY座標の算出
- XY座標から緯度・経度の算出

## 2. Jupyter Notebook
### estimate.ipynb
計算を見積もるための参考ノートブック

### data_sandbox.ipynb
実験データの集計および精度の検証

### estimate_tolerance.ipynb
許容誤差の検証。画像方位角および高度のずれに対しては、許容範囲が大きいことがわかった。

### evaluate_result.ipynb
実験データの検証。カメラ取付角、画像方位角、高度などの様々なずれの要素を考慮すると、<br>
水平方向で10m以内の誤差に収めるには、高度を下げることが望ましい。

### flight_area.ipynb
コンペティションの飛行領域の推定


