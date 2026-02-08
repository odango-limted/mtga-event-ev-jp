import unittest
from core import calculation

class TestCalculation(unittest.TestCase):
    def test_match_win_rate_bo1(self):
        self.assertAlmostEqual(calculation.calculate_match_win_rate(0.5, "BO1"), 0.5)
        self.assertAlmostEqual(calculation.calculate_match_win_rate(0.6, "BO1"), 0.6)

    def test_match_win_rate_bo3(self):
        # 0.5 -> 0.5
        self.assertAlmostEqual(calculation.calculate_match_win_rate(0.5, "BO3"), 0.5)
        # 0% -> 0%
        self.assertAlmostEqual(calculation.calculate_match_win_rate(0.0, "BO3"), 0.0)
        # 100% -> 100%
        self.assertAlmostEqual(calculation.calculate_match_win_rate(1.0, "BO3"), 1.0)
       
    def test_simulate_event_total_prob(self):
        res = calculation.simulate_event(0.5, 7, 3)
        total_prob = sum(res.values())
        self.assertAlmostEqual(total_prob, 1.0)

    def test_simulate_event_perfect(self):
        res = calculation.simulate_event(1.0, 7, 3)
        self.assertAlmostEqual(res[7], 1.0)
        self.assertEqual(res.get(0, 0), 0.0)

    def test_simulate_event_zero(self):
        res = calculation.simulate_event(0.0, 7, 3)
        self.assertAlmostEqual(res[0], 1.0)

    def test_simulate_fixed_rounds_event_total_prob(self):
        """固定ラウンド形式: 確率の合計が1になることを確認"""
        res = calculation.simulate_fixed_rounds_event(0.5, 3)
        total_prob = sum(res.values())
        self.assertAlmostEqual(total_prob, 1.0, places=6)

    def test_simulate_fixed_rounds_event_binomial(self):
        """固定ラウンド形式: 二項分布の期待値と一致することを確認"""
        # 勝率50%で3ラウンドの場合
        # 0勝: C(3,0) * 0.5^3 = 0.125
        # 1勝: C(3,1) * 0.5^3 = 0.375
        # 2勝: C(3,2) * 0.5^3 = 0.375
        # 3勝: C(3,3) * 0.5^3 = 0.125
        res = calculation.simulate_fixed_rounds_event(0.5, 3)
        self.assertAlmostEqual(res[0], 0.125, places=6)
        self.assertAlmostEqual(res[1], 0.375, places=6)
        self.assertAlmostEqual(res[2], 0.375, places=6)
        self.assertAlmostEqual(res[3], 0.125, places=6)

    def test_simulate_fixed_rounds_event_perfect(self):
        """固定ラウンド形式: 勝率100%で全勝することを確認"""
        res = calculation.simulate_fixed_rounds_event(1.0, 3)
        self.assertAlmostEqual(res[3], 1.0)
        self.assertAlmostEqual(res[0], 0.0)

    def test_simulate_fixed_rounds_event_zero(self):
        """固定ラウンド形式: 勝率0%で全敗することを確認"""
        res = calculation.simulate_fixed_rounds_event(0.0, 3)
        self.assertAlmostEqual(res[0], 1.0)
        self.assertAlmostEqual(res[3], 0.0)

if __name__ == '__main__':
    unittest.main()
