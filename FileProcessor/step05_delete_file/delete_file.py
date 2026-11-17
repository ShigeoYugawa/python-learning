"""
使い方
--------------------------------------------------
■ 基本実行
    python delete_file.py input/sample.txt

■ 正常終了メッセージを非表示
    python delete_file.py input/sample.txt --quiet

■ ヘルプ表示
    python delete_file.py --help

■ オプション
    --quiet
        正常終了時のメッセージを表示しない。

    -h, --help
        ヘルプを表示する（自動登録）。

■ 終了コード
    0 : 正常終了（削除成功または対象なし）
    1 : 処理失敗
--------------------------------------------------
"""

import argparse
import sys
from pathlib import Path


# ファイルを削除し、処理結果を返す
def delete_file(file_path: Path) -> str:
    """ファイルを削除し、処理結果を返す。"""

    try:
        file_path.unlink()  # 指定されたファイルを削除
        return "deleted"

    except FileNotFoundError:  # 削除対象のファイルが存在しない場合
        return "not_found"


# コマンドライン引数を解析する
def parse_arguments() -> argparse.Namespace:
    # 引数解析用のArgumentParserオブジェクトを生成
    parser = argparse.ArgumentParser(
        description="指定したファイルを削除します。"
    )

    # 削除対象ファイルのパスを必須の位置引数として定義
    parser.add_argument(
        "file_path",
        type=Path,
        help="削除対象のファイルパス"
    )

    # 正常終了時のメッセージを非表示にするオプションを定義
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="正常終了時のメッセージを表示しません。"
    )

    # -h / --help はArgumentParserによって自動的に登録される

    return parser.parse_args()


# メイン処理を実行し、終了コードを返す
def main() -> int:
    args = parse_arguments()

    try:
        # ファイル削除処理を実行
        result = delete_file(args.file_path)

        # --quiet が指定されていない場合のみ処理結果を表示
        if not args.quiet:
            if result == "deleted":
                print(f"[SUCCESS] ファイルを削除しました: {args.file_path}")
            else:
                print(f"[SKIP] 削除対象が存在しません: {args.file_path}")

        return 0

    # ファイルへのアクセス権限が不足している場合
    except PermissionError:
        print(
            f"[ERROR] アクセス権限がありません: {args.file_path}",
            file=sys.stderr
        )
        return 1

    # その他のOS関連のファイル操作エラーが発生した場合
    except OSError as error:
        print(
            f"[ERROR] 削除に失敗しました: {error}",
            file=sys.stderr
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
