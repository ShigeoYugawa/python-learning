import os


def demo_seek_and_tell():
  sample_file = 'test_data.bin'

  # 事前準備：0〜9の数字（10バイト）が入ったテスト用バイナリファイルを作成
  with open(sample_file, 'wb') as f:
    f.write(b'0123456789')

  # バイナリ読み込みモード（rb）で開いて位置の動きを確認
  with open(sample_file, 'rb') as f:
    print(f'初期位置: {f.tell()}バイト目')  # -> 0

    # 3バイト読み込むと、位置も自動で3つ進む
    data = f.read(3)
    print(f'3バイト読込({data}): 現在 {f.tell()}バイト目')  # -> 3

    # 第2引数=1（現在位置から +4バイト進む）
    f.seek(4, 1)
    print(f'現在位置から+4移動: 現在 {f.tell()}バイト目')  # -> 7

    # 第2引数=0（先頭から 2バイト目へ戻る）
    f.seek(2, 0)
    print(f'先頭から2バイト目へ移動: 現在 {f.tell()}バイト目')  # -> 2

    # 第2引数=2（末尾から -1バイト戻る = 最後の1文字の手前）
    f.seek(-1, 2)
    print(
        f'末尾から1バイト戻る: 現在 {f.tell()}バイト目 / 残りデータ:'
        f' {f.read()}'
    )  # -> 9 / b'9'

  # 後片付け（テストファイルを削除）
  os.remove(sample_file)


if __name__ == '__main__':
  demo_seek_and_tell()
