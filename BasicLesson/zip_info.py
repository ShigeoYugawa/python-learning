"""
ZIPファイルの先頭には「ローカルファイルヘッダ」という決まった並びのバイト列が入っています。
struct.unpack を使って、そのバイト列をPythonの数値データに変換しています。
"""

import struct, sys

def read_zip_headers(zip_path, limit=3):

    # バイナリ読み込みモード（rb）でZIPファイルを開きます。
    with open(zip_path, 'rb') as f:
        data = f.read()

    start = 0
    # 最初の 3 つのファイルヘッダを表示する
    for i in range(limit):
        # 残りデータがヘッダの固定長部分（30B）に満たなければ終了（struct.error防止）
        # ※30Bの内訳 = 読み飛ばす基本情報(14B) + サイズや長さの数値情報(16B)
        if start + 30 > len(data):
            break

        # ヘッダの先頭14バイト（シグネチャやバージョン情報など）を読み飛ばします。
        start += 14

        # 続く16バイトをリトルエンディアン（<）で5つの数値（I=4バイト整数×3、H=2バイト整数×2）に分解します。
        fields = struct.unpack('<IIIHH', data[start:start+16])

        # 分解した数値から「CRC32」「圧縮後サイズ」「圧縮前サイズ」「ファイル名の長さ」「拡張フィールドの長さ」を取得します。
        crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

        start += 16

        # 取得した「ファイル名の長さ」の分だけバイト列を切り出し、ファイル名を取得します。
        #filename = data[start:start+filenamesize]
        filename = data[start : start + filenamesize].decode(
           'utf-8', errors='replace'
        )
        start += filenamesize
        
        # 拡張フィールドと圧縮データ本体を読み飛ばし、次のファイルのヘッダ位置まで移動します。
        #extra = data[start:start+extra_size]
        #print(filename, hex(crc32), comp_size, uncomp_size)

        # 結果を表示
        print(f'[{i+1}] ファイル名: {filename}')
        print(
            f'    CRC32: {hex(crc32)} | 圧縮後: {comp_size}B | 圧縮前:'
            f' {uncomp_size}B'
        )

        # 次のヘッダまで進む
        start += extra_size + comp_size


# コマンドラインから直接実行された時だけ動く処理
if __name__ == '__main__':
    # コマンドライン引数でZIPファイルが指定されているか確認
    if len(sys.argv) < 2:
        print('使い方: python zip_info.py <ZIPファイル名>')
        sys.exit(1)

    target_zip = sys.argv[1]
    read_zip_headers(target_zip)