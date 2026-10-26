"""
NBA Player Performance & Contract Valuation Analytics Engine
Author: Alexys Gomez
Focus: Sports Analytics, Salary Efficiency & Quantitative Valuation
"""

from datetime import datetime

class PlayerValuationModel:
    def __init__(self, league_year="2025-26"):
        self.league_year = league_year
        self.players = []

    def evaluate_player(self, player_name, team, position, ppg, rpg, apg, per, salary_millions):
        """
        Calculates a normalized Performance Index (PI) and computes 
        estimated market value vs actual cap hit.
        """
        # Composite productivity index weighted across primary box stats + PER
        productivity_index = round((ppg * 1.0) + (rpg * 1.2) + (apg * 1.5) + (per * 0.8), 2)
        
        # Benchmark valuation: Baseline expected production per $1M cap allocation
        fair_market_value = round((productivity_index / 58.0) * 32.5, 2)
        
        # Surplus contract value (positive = high-value bargain / negative = over-allocated cap)
        surplus_value = round(fair_market_value - salary_millions, 2)
        
        # Cost Efficiency Ratio
        cost_per_index_point = round((salary_millions * 1_000_000) / productivity_index, 0) if productivity_index > 0 else 0

        record = {
            "name": player_name,
            "team": team,
            "pos": position,
            "index": productivity_index,
            "salary": salary_millions,
            "fair_value": fair_market_value,
            "surplus": surplus_value,
            "efficiency": cost_per_index_point,
            "status": "High Surplus Value" if surplus_value > 4.0 else ("Cap Drag" if surplus_value < -4.0 else "Fairly Valued")
        }
        self.players.append(record)
        return record

    def print_executive_board(self):
        """Generates structured analytics leaderboard."""
        print("=" * 96)
        print(f"  QUANTITATIVE ROSTER ANALYTICS & CONTRACT SURPLUS BOARD ({self.league_year})")
        print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Metric: Composite Efficiency Index")
        print("=" * 96)
        print(f"{'Player Name':<22} | {'Team':<4} | {'Pos':<3} | {'Index':<6} | {'Cap ($M)':<8} | {'Model ($M)':<10} | {'Surplus':<8} | {'Status'}")
        print("-" * 96)

        # Sort by productivity index descending
        sorted_roster = sorted(self.players, key=lambda x: x["index"], reverse=True)

        for p in sorted_roster:
            surplus_str = f"+${p['surplus']:.1f}M" if p['surplus'] >= 0 else f"-${abs(p['surplus']):.1f}M"
            print(f"{p['name']:<22} | {p['team']:<4} | {p['pos']:<3} | {p['index']:>6.1f} | ${p['salary']:>6.1f}M | ${p['fair_value']:>8.1f}M | {surplus_str:>8} | {p['status']}")

        print("-" * 96)
        avg_surplus = round(sum(p["surplus"] for p in self.players) / len(self.players), 2)
        print(f"EVALUATION SUMMARY: {len(self.players)} Players Screened | Mean Portfolio Surplus: ${avg_surplus}M")
        print("=" * 96)

if __name__ == "__main__":
    model = PlayerValuationModel()

    # Screen sample roster allocations
    model.evaluate_player("Cam Thomas", "BKN", "SG", 24.2, 3.2, 3.7, 18.6, 4.0)
    model.evaluate_player("Jalen Brunson", "NYK", "PG", 27.9, 3.6, 6.7, 23.4, 26.3)
    model.evaluate_player("Nic Claxton", "BKN", "C",  11.8, 9.9, 2.1, 17.2, 19.5)
    model.evaluate_player("Mikal Bridges", "NYK", "SF", 19.6, 4.5, 3.6, 16.8, 23.3)
    model.evaluate_player("Tyrese Haliburton", "IND", "PG", 20.1, 3.9, 10.9, 21.5, 35.2)

    model.print_executive_board()
