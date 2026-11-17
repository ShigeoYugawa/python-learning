
import argparse
import csv
from pathlib import Path


def read_csv(file_path: Path) -> None:
    """
    CSVファイルを読み込み、各行のデータを表示する。

    Args:
        file_path: 読み込むCSVファイルのパス

        python csv_read.py input/sample.csv
        python csv_read.py --help
    """
    try:
        # CSVファイルを読み込みモードで開く。
        # newline="" は csv モジュールの推奨設定。
        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            # DictReaderを使用すると、
            # 先頭行の列名をキーとした辞書形式でデータを取得できる。
            reader = csv.DictReader(file)

            # CSVのデータを1行ずつ辞書として取得する。
            # row["name"] のように列名を指定して値を参照できる。
            for row in reader:
                print(row)

    # 指定されたファイルが存在しない場合
    except FileNotFoundError:
        print(f"[ERROR] ファイルが見つかりません: {file_path}")

    # ファイルへのアクセス権限がない場合
    except PermissionError:
        print(f"[ERROR] ファイルへのアクセスが拒否されました: {file_path}")


def parse_args() -> argparse.Namespace:
    """
    コマンドライン引数を解析する。

    Returns:
        argparse.Namespace: 解析された引数
    """
    # コマンドライン引数の解析を行うパーサーを生成する。
    parser = argparse.ArgumentParser(
        description="CSVファイルを読み込んで内容を表示します。"
    )

    # 必須の位置引数を定義する。
    # type=Path により、受け取った文字列をPathオブジェクトに変換する。
    parser.add_argument(
        "file_path",
        type=Path,
        help="読み込むCSVファイルのパス"
    )

    # コマンドライン引数を解析して返す。
    return parser.parse_args()


def main() -> None:
    # コマンドライン引数を取得する。
    args = parse_args()

    # 取得したファイルパスをCSV読み込み関数に渡す。
    read_csv(args.file_path)


# このモジュールが直接実行された場合のみmain()を呼び出す。
# 他のモジュールからimportされた場合は実行されない。
if __name__ == "__main__":
    main()
