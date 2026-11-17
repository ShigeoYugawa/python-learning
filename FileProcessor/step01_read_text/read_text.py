from pathlib import Path

def run_step1():
    input_path = Path("input") / "sample.txt"

    with input_path.open(mode="r", encoding="utf-8") as file:
    #with input_path.open(mode="r") as file:

        #content = file.read()
        # ---------------------------
        # (utf-8)
        # Python
        # データ変換処理
        # ファイル操作
        # 文字コードの確認
        # ---------------------------
        # (none)
        # UnicodeDecodeError: 'cp932' codec can't decode byte 0x87 in position 10: illegal multibyte sequence 

        #content = file.readline()
        # ---------------------------
        # (utf-8)
        # Python
        # ---------------------------
        # (none)
        # UnicodeDecodeError: 'cp932' codec can't decode byte 0x87 in position 10: illegal multibyte sequence 

        #content = file.readlines()
        # ---------------------------
        # (utf-8)
        # ['Python\n', 'データ変換処理\n', 'ファイル操作\n', '文字コードの確認']
        # ---------------------------
        # (none)
        # UnicodeDecodeError: 'cp932' codec can't decode byte 0x87 in position 10: illegal multibyte sequence  

        for line in file:
            print(line, end="")
            # (utf-8)
            # ---------------------------
            # Python
            # データ変換処理
            # ファイル操作
            # 文字コードの確認

            # (none)
            # ---------------------------
            # UnicodeDecodeError: 'cp932' codec can't decode byte 0x87 in position 10: illegal multibyte sequence

    #print(content)


if __name__ == "__main__":
    run_step1()