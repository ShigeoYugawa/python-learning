
from pathlib import Path


def main():
    # 出力先パス
    output_path = Path("output") / "result.txt"

    # 書き込むテキスト
    content = "新規ファイルとして作成されました。\n"

    try:
        # 排他的に新規作成
        with output_path.open(mode="x", encoding="utf-8") as file:
            file.write(content)

        print("ファイルを作成しました。")

    except FileExistsError:
        print("ファイルが既に存在するため、作成できません。")


if __name__ == "__main__":
    main()
