import sys
import zipfile


def read_zip_info_standard(zip_path, limit=3):
  """標準ライブラリ zipfile を使った実務向けの安全な実装"""
  # zipfile.ZipFile で開く（中身をすべてメモリに読み込むわけではないので省メモリ）
  with zipfile.ZipFile(zip_path, 'r') as zf:
    # infolist() でZIP内の全ファイル情報のリストを取得（先頭からlimit個だけ処理）
    for i, info in enumerate(zf.infolist()[:limit]):
      print(f'[{i+1}] ファイル名: {info.filename}')
      print(
          f'    CRC32: {hex(info.CRC)} | 圧縮後: {info.compress_size}B |'
          f' 圧縮前: {info.file_size}B'
      )


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('使い方: python zip_standard.py <ZIPファイル名>')
    sys.exit(1)

  read_zip_info_standard(sys.argv[1])
