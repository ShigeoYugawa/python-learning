
"""
実装目的
- CSVファイルを読み込む。
- 年齢が30歳以上のレコードを抽出する。
- 抽出結果を別のCSVファイルに保存する。
- ファイルパスはコマンドライン引数で受け取る。
- 不正な年齢のレコードはスキップする。
- CSVの列数不一致はエラーとする。
- 出力途中のエラーから既存ファイルを保護する。
"""

import argparse
import csv
import operator
import os
import sys
import tempfile
from contextlib import suppress
from pathlib import Path


# 比較演算子と比較関数の対応
OPERATORS = {
    "gt": operator.gt,
    "ge": operator.ge,
    "eq": operator.eq,
    "le": operator.le,
    "lt": operator.lt,
    "ne": operator.ne,
}


def extract_csv(
        input_path: Path,
        output_path: Path,
        operator_type: str,
        value: int
) -> None:

    # 入力ファイルと出力ファイルが同一でないことを確認する（絶対パスで比較）
    if input_path.resolve() == output_path.resolve():
        raise ValueError("入力ファイルと出力ファイルに同じパスは指定できません。")

    # 入力パスがディレクトリでないことを確認する
    if input_path.is_dir():
        raise IsADirectoryError(f"入力パスがディレクトリです: {input_path}")

    # 演算子のキー（gt / ge / eq など）から対応する比較関数を取得する
    # 動作イメージ: operator_type が "ge" の場合、operator.ge を取得する
    comparison = OPERATORS[operator_type]

    # CSVファイルを読み込む
    with input_path.open(
        mode="r",
        encoding="utf-8",
        newline=""
    ) as input_file:

        # 余分な列を検出するための専用キー
        extra_fields_key = object()

        # CSVファイルを読み込む
        reader = csv.DictReader(
            input_file,
            restkey=extra_fields_key, # ヘッダーより余分な列を格納するキー
            restval=None,             # ヘッダーより不足している列に設定する値
            strict=True               # 不正なCSV構文を厳密に検査する
        )

        # ヘッダーの存在を確認する
        if not reader.fieldnames:
            raise ValueError(
                f"CSVファイルにヘッダーが存在しません: {input_path}"
            )

        # age列の存在を確認する
        if "age" not in reader.fieldnames:
            raise ValueError(
                f"CSVファイルにage列が存在しません: {input_path}"
            )

        # 出力先ディレクトリを作成する
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # 一時ファイルのパスを管理する
        temp_path = None

        try:
            # 出力先と同じディレクトリに一時ファイルを作成する
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",

                # CSVモジュール側で改行を制御するため空文字を指定
                # Windows環境で余分な空行が発生するのを防ぐ
                newline="",

                dir=output_path.parent,
                prefix=f".{output_path.name}.", # 一時ファイル名の接頭辞
                suffix=".tmp",                  # 一時ファイル名の拡張子

                # 自動削除を無効化
                # コンテキストマネージャー(with)を抜けてもファイルを残す
                delete=False

            ) as temp_file:

                temp_path = Path(temp_file.name)

                # CSV書き込みオブジェクトを作成する
                writer = csv.DictWriter(
                    temp_file,
                    fieldnames=reader.fieldnames
                )

                # ヘッダーを書き込む
                writer.writeheader()

                # CSVレコードを1行ずつ処理する
                for row in reader:

                    # 余分な列が存在する場合はエラー
                    if extra_fields_key in row:
                        raise ValueError(
                            f"CSVの列数がヘッダーと一致しません。"
                            f"行番号: {reader.line_num}"
                        )

                    # 列が不足している場合はエラー
                    # None  : CSVに列自体が存在しない（列数不足）
                    # ""    : 列は存在するが、値が空文字（空欄）
                    missing_fields = [
                        field
                        for field in reader.fieldnames
                        if row[field] is None
                    ]

                    if missing_fields:
                        raise ValueError(
                            f"CSVの列数がヘッダーと一致しません。"
                            f"行番号: {reader.line_num}"
                        )

                    try:
                        # 年齢を整数に変換する
                        age = int(row["age"].strip())

                    except (ValueError, TypeError):
                        # 整数に変換できない値（文字列・空欄・Noneなど）は対象外とする
                        continue

                    # 取得した比較関数に年齢と閾値を渡して比較する
                    # 動作イメージ: comparison(35, 30) は operator.ge(35, 30) と同じ
                    # 比較結果がFalseの場合、対象レコードをスキップする
                    if not comparison(age, value):
                        continue

                    # 条件に一致するレコードを書き込む
                    writer.writerow(row)

            # 一時ファイルを正式な出力ファイルに置き換える
            os.replace(temp_path, output_path)

            # 正常に置き換えたため一時ファイルの管理を終了する
            temp_path = None

        finally:
            # エラー発生時に残った一時ファイルを削除する
            if temp_path is not None:
                with suppress(OSError):
                    temp_path.unlink(missing_ok=True)


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

    parser.add_argument(
        "--operator",
        choices=OPERATORS.keys(),
        required=True,
        help="比較演算子（gt: より大きい / ge: 以上 / eq: 一致 / le: 以下 / lt: 未満 / ne: 不一致）"
    )

    parser.add_argument(
        "--value",
        type=int,
        required=True,
        help="比較する整数値"
    )

    return parser.parse_args()


def main() -> int:

    args = parse_args()

    try:
        extract_csv(
            args.input_path,
            args.output_path,
            args.operator,
            args.value
        )

    except (OSError, csv.Error, ValueError) as error:

        # エラーを標準エラー出力に表示する
        print(f"[ERROR] {error}", file=sys.stderr)

        return 1

    print("[SUCCESS] CSV抽出処理が完了しました。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
