""" モジュールの読み込み
コマンドライン引数を扱うための argparse モジュールを読み込みます。
"""
import argparse


""" パーサー（解析器）の作成
引数を解析するための土台（ArgumentParser）を作ります。
• prog='top': ヘルプ画面（-h オプション実行時など）に表示されるプログラム名です。
• description='...': このプログラムが何をするものかの説明文です。
"""
parser = argparse.ArgumentParser(
    prog='top',
    description='Show top lines from each file')


""" 必須の引数（ファイル名）の設定
プログラム実行時に必ず指定する引数（位置引数）を設定します。
• 'filenames': 受け取った値を入れる変数名です。
• nargs='+': 「1つ以上の引数を受け取る」という指定です。これにより、複数のファイルをスペース区切りで
             指定できるようになります（例: file1.txt file2.txt）。受け取った値はリスト形式になります。
"""
parser.add_argument('filenames', nargs='+')


""" オプション引数（行数）の設定
必要に応じて追加できるオプション引数（ハイフンから始まる引数）を設定します。
• '-l', '--lines': 短縮形（-l）と正式名称（--lines）のどちらでも指定できるようにします。
• type=int: 入力された値を自動的に整数（int型）に変換します。数字以外が入力されるとエラーを出してくれます。
• default=10: このオプションが指定されなかった場合の初期値（デフォルト値）を 10 に設定します。
"""
parser.add_argument('-l', '--lines', type=int, default=10)


""" 引数の解析と結果の出力
• parse_args(): 実際にコマンドラインから渡された引数を解析し、args というオブジェクトに格納します。
• print(args): 解析された結果の中身を表示します。
"""
args = parser.parse_args()
print(args)