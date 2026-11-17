
from pathlib import Path


def main():
    # 出力先パス
    output_path = Path("output") / "result.txt"

    # 追記するテキスト
    content = "追記されたテキストです。\n"

    # ファイルへ追記
    with output_path.open(mode="a", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    main()
