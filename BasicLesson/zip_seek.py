import os
import struct
import sys


def read_zip_headers_seek(zip_path, limit=3):
  """f.seek() を使ってメモリ消費を最小限に抑えたバイナリ解析版"""
  # ファイル全体のサイズを事前に取得（f.read()で中身を読まずにサイズだけ調べる）
  total_size = os.path.getsize(zip_path)

  with open(zip_path, 'rb') as f:
    for i in range(limit):
      # 現在の読み取り位置（f.tell()）から固定長ヘッダ(30B)が残っているか確認
      if f.tell() + 30 > total_size:
        break

      # 先頭14Bを読み飛ばす（第2引数の 1 は「現在位置からの相対移動」を意味する）
      f.seek(14, 1)

      # 続く16Bだけをディスクから直接読み込む
      header_data = f.read(16)
      crc32, comp_size, uncomp_size, filenamesize, extra_size = struct.unpack(
          '<IIIHH', header_data
      )

      # ファイル名の長さ分だけ読み込み、文字列に変換
      filename = f.read(filenamesize).decode('utf-8', errors='replace')

      print(f'[{i+1}] ファイル名: {filename}')
      print(
          f'    CRC32: {hex(crc32)} | 圧縮後: {comp_size}B | 圧縮前:'
          f' {uncomp_size}B'
      )

      # 拡張フィールドと圧縮データ本体はメモリに読み込まず、位置だけスキップする
      f.seek(extra_size + comp_size, 1)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print('使い方: python zip_seek.py <ZIPファイル名>')
    sys.exit(1)

  read_zip_headers_seek(sys.argv)
