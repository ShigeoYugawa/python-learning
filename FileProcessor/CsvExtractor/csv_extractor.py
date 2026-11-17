"""
実装目的
- CSVファイルを読み込む。
- 年齢が30歳以上のレコードを抽出する。
- 抽出結果を別のCSVファイルに保存する。
- ファイルパスはコマンドライン引数で受け取る。
"""
import argparse
import csv
from pathlib import Path


def extract_csv(input_path: Path, output_path: Path) -> None:

    # 一時格納用リスト
    filtered_rows = []

    with input_path.open(mode="r", encoding="utf-8", newline="") as input_file:
        # CSVファイルを読み込む。
        reader = csv.DictReader(input_file)
        for row in reader:
            # 年齢が30歳以上のレコードを抽出する。
            age = int(row["age"])
            if age >= 30:
                # print(row)
                filtered_rows.append(row)

        # 出力先ディレクトリを作成する
        output_path.parent.mkdir(
            # 必要な親ディレクトリもまとめて作成する
            parents=True,
            # ディレクトリが既に存在していても例外にしない
            exist_ok=True 
        )

        # CSVファイルを書き込む
        with output_path.open(mode="w", encoding="utf-8", newline="") as output_file:

            """
            DictReader は、最初の行をヘッダーとして扱うので、その値をそのまま流用する
            """
            writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)

            # ヘッダーを書き込む（writeオブジェクト生成時にヘッダーは指定済）
            writer.writeheader()

            # 抽出したレコードを書き込む
            writer.writerows(filtered_rows)
            

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="CSVファイルから30歳以上のレコードを抽出して保存します。"
    )

    parser.add_argument(
        "input_path",
        type=Path,
        help="読み込むCSVファイルのパス"
    )

    parser.add_argument(
        "output_path",
        type=Path,
        help="書き込むCSVファイルのパス"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    extract_csv(args.input_path, args.output_path)


if __name__ == "__main__":
    main()