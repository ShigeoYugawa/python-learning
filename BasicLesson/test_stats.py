import unittest

# テスト対象の関数（平均値を計算する）
def average(values):
    return sum(values) / len(values)

# テスト用のクラス（unittest.TestCaseを継承する）
class TestStatisticalFunctions(unittest.TestCase):

    # メソッド名は必ず「test_」から始める
    def test_average(self):
        # 計算結果が期待通りかチェック
        self.assertEqual(average([20, 30, 70]), 40.0)
        self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
        
        # 特定のエラー（例外）が正しく発生するかチェック
        with self.assertRaises(ZeroDivisionError):
            average([])
        with self.assertRaises(TypeError):
            average(20, 30, 70)

# コマンドラインから直接実行されたときにテストを走らせる
if __name__ == '__main__':
    unittest.main()
