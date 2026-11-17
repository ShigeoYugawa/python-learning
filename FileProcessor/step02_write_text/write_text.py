""" input.py 
> python write_text.py で実行
"""

from pathlib import Path

def run_step2():
    # ファイル出力先パスの指定
    output_path = Path("output") / "result.txt"

    # UTF8の書き込みモードでファイルを開く
    with output_path.open(mode="w", encoding="utf-8") as file:
        file.write("Hello, Python!\n")
        file.write("テキストファイルへの書き込み\n")


if __name__ == "__main__":
    run_step2()


""" 出力結果
Hello, Python!
テキストファイルへの書き込み
"""