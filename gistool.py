from PIL import Image
from PIL.ExifTags import TAGS
import unittest
from math import modf

def get_datetime(file):

    img = Image.open(file)

    # Exifデータを取得
    try:
      exif = img._getexif()
    except AttributeError:
      return {}

    # タグIDそのままでは人が読めないのでデコードして、テーブルに格納する
    exif = img._getexif()
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    datetime = exif_table['DateTime']
    return datetime

def get_GPS(file):
    """
    指定した画像のEXIFデータからGPS_infoを取り出す
    引数
        file : 画像のファイル名

    返り値
        gps: 画像ファイルのGPSデータ。ディクショナリ形式。
            gps['lat']: 緯度 -90<=lat<=90, float, 小数点以下6桁
            gps['lon']: 経度 -180<=lon<=180, float, 小数点以下6桁
            gps['alt']: 高度 float
    """
    im = Image.open(file)

    # Exif データを取得
    # 存在しなければそのまま終了 空の辞書を返す
    try:
        exif = im._getexif()
    except AttributeError:
        return {}

    # タグIDそのままでは人が読めないのでデコードして、テーブルに格納する
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value

    # 緯度latの読み取り。Nを正、Sを負として処理する。
    lat_dir = exif_table['GPSInfo'][1]
    lat = exif_table['GPSInfo'][2]

    if lat_dir[0] == "S":
        sgn = -1
    else:
        sgn = 1

    lat = sgn * (float(lat[0][0]) + float(lat[1][0])/60.0 + float(lat[2][0])/lat[2][1]/3600.0)
    lat = float("{:.6f}".format(lat))

    # 経度lonの読み取り。Eを正、Wを負として処理する。
    lon_dir = exif_table['GPSInfo'][3]
    lon = exif_table['GPSInfo'][4]

    if lon_dir[0] == "W":
        sgn = -1
    else:
        sgn = 1
        
    lon = sgn * (float(lon[0][0]) + float(lon[1][0])/60.0 + float(lon[2][0])/lon[2][1]/3600.0)
    lon = float("{:.6f}".format(lon))

    alt = exif_table['GPSInfo'][6]
    alt = float(alt[0])/float(alt[1])
    gps = dict({'lat': lat, 'lon': lon, 'alt': alt})
    return gps

def deg2dms(deg_num):
    """
    緯度・経度をDEG形式からDMS形式へ変換する
    引数
        deg_num: DEG形式緯度・経度。float型。 ex. 31.012345
    戻り値
        dms_num: DMS形式経度・緯度。tuple。(deg, min, sec)
    """
    res, deg = modf(deg_num)
    res, min = modf(res * 60)
    sec = res * 60
    return int(deg), int(min), round(sec, 3)

def dms2deg(dms_num):
    """
    緯度・経度をDMS形式からDEG形式へ変換する
    引数
        dms_num: DMS形式経度・緯度。tuple。(deg, min, sec)
    戻り値
        deg_num: DEG形式緯度・経度。float型。 ex. 31.012345
    """
    deg_num = dms_num[0] + dms_num[1]/60.0 + dms_num[2]/3600.0
    return round(deg_num, 6)


class TestGistool(unittest.TestCase):
    """
    本モジュールのテストコード（for unittest）
    unittest.TestCaseのサブクラスとすることで自動的にunittestの
    テストケースであると認識される。
    """

    def tearDown(self):
        """ 各テストメソッドの最後に実行するコード """
        print('tearDown: テストメソッドを1つ実行しました')

    def test_get_GPS(self):
        path = r"data/DJI_0132.JPG"
        gps_ans = {'lat': 37.286447, 'lon': 139.473903, 'alt': 213.796}
        self.assertEqual(get_GPS(path), gps_ans)

    def test_deg2dms(self):
        dms_ans = (37, 17, 11.209)
        self.assertEqual(deg2dms(37.286447), dms_ans)
        dms_ans = (139, 28, 26.051)
        self.assertEqual(deg2dms(139.473903), dms_ans)

    def test_dms2deg(self):
        deg_ans = 37.286447
        self.assertAlmostEqual(dms2deg((37, 17, 11.209)), deg_ans)
        deg_ans = 139.473903
        self.assertAlmostEqual(dms2deg((139, 28, 26.051)), deg_ans)

if __name__ == "__main__":
    unittest.main()

