import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DemoDashboard:
    """
    Live Dashboard for Demo Trading
    - Shows real-time statistics
    - Displays charts and metrics
    - Tracks P&L in real-time
    """
    
    def __init__(self, demo_engine):
        self.demo_engine = demo_engine
    
    def display_live_stats(self):
        """Display live statistics"""
        
        stats = self.demo_engine.get_demo_stats()
        
        print("\n" + "="*70)
        print("📊 DEMO TRADING - LIVE STATISTICS")
        print("="*70)
        print(f"\n💰 Account:")
        print(f"   Starting Balance:    ${stats['starting_balance']:,.2f}")
        print(f"   Current Balance:     ${stats['current_balance']:,.2f}")
        print(f"   Total P&L:           ${stats['total_pnl']:,.2f}")
        print(f"   Return:              {stats['return_percent']:.2f}%")
        
        print(f"\n📈 Trades:")
        print(f"   Total Trades:        {stats['total_trades']}")
        print(f"   Winning Trades:      {stats['winning_trades']}")
        print(f"   Losing Trades:       {stats['losing_trades']}")
        print(f"   Win Rate:            {stats['win_rate']:.2f}%")
        
        print(f"\n🔄 Open Positions:")
        open_positions = self.demo_engine.position_manager.get_open_positions()
        print(f"   Total Open:          {len(open_positions)}")
        
        for i, position in enumerate(open_positions, 1):
            print(f"\n   Position #{i}:")
            print(f"      Type:            {position['direction']}")
            print(f"      Entry:           ${position['entry_price']:.2f}")
            print(f"      Current:         ${position['current_price']:.2f}")
            print(f"      P&L:             ${position['pnl']:.2f} ({position['pnl_percent']:.2f}%)")
            print(f"      SL:              ${position['stop_loss']:.2f}")
            print(f"      TP:              ${position['take_profit']:.2f}")
        
        print("\n" + "="*70 + "\n")
    
    def plot_equity_curve(self, filename: str = 'demo_equity_curve.png'):
        """Plot equity curve"""
        
        if not self.demo_engine.equity_history:
            logger.warning("No equity history to plot")
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        equity = self.demo_engine.equity_history
        ax.plot(range(len(equity)), equity, linewidth=2, color='#2E86AB', marker='o', markersize=3)
        
        # Add starting balance line
        ax.axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5, label='Starting Balance')
        
        # Fill area
        ax.fill_between(range(len(equity)), equity, equity[0],
                        where=[e >= equity[0] for e in equity],
                        alpha=0.3, color='green', label='Profit')
        ax.fill_between(range(len(equity)), equity, equity[0],
                        where=[e < equity[0] for e in equity],
                        alpha=0.3, color='red', label='Loss')
        
        ax.set_title('Demo Trading - Equity Curve', fontsize=14, fontweight='bold')
        ax.set_xlabel('Update Cycle', fontsize=12)
        ax.set_ylabel('Equity ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"Equity curve saved to {filename}")
        plt.close()
    
    def plot_price_history(self, filename: str = 'demo_price_history.png'):
        """Plot price history"""
        
        if not self.demo_engine.price_history:
            logger.warning("No price history to plot")
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        prices = self.demo_engine.price_history
        ax.plot(range(len(prices)), prices, linewidth=2, color='#06A77D', marker='o', markersize=3)
        
        ax.set_title('BTCUSDT - Live Price History', fontsize=14, fontweight='bold')
        ax.set_xlabel('Update Cycle', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"Price history saved to {filename}")
        plt.close()
    
    def generate_demo_report(self, filename: str = 'demo_trading_report.txt'):
        """Generate detailed demo trading report"""
        
        stats = self.demo_engine.get_demo_stats()
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║        SMART AGENTIC AI BOT - DEMO TRADING REPORT             ║
╚════════════════════════════════════════════════════════════════╝

📊 ACCOUNT SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting Balance:       ${stats['starting_balance']:,.2f}
Current Balance:        ${stats['current_balance']:,.2f}
Total P&L:              ${stats['total_pnl']:,.2f}
Total Return:           {stats['return_percent']:.2f}%

📈 TRADE STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Trades:           {stats['total_trades']}
Winning Trades:         {stats['winning_trades']}
Losing Trades:          {stats['losing_trades']}
Win Rate:               {stats['win_rate']:.2f}%

✅ DEMO TRADING COMPLETED SUCCESSFULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Files:
  - demo_equity_curve.png
  - demo_price_history.png
  - demo_trading_report.txt

Next Steps:
  1. Review the generated charts
  2. Analyze the trading signals
  3. Adjust parameters if needed
  4. Consider Live Trading when comfortable

⚠️  DISCLAIMER:
This is a demo/paper trading system. No real money was used.
Results are for educational purposes only.
"""
        
        with open(filename, 'w') as f:
            f.write(report)
        
        logger.info(f"Report saved to {filename}")
        return report
    
    def print_welcome_message(self):
        """Print welcome message"""
        print("\n" + "="*70)
        print("🤖 SMART AGENTIC AI BOT - DEMO TRADING SYSTEM")
        print("="*70)
        print("\n✨ Features:")
        print("   ✅ Real-time market data (Live)")
        print("   ✅ AI-powered trading signals")
        print("   ✅ Automated position management")
        print("   ✅ Risk management (SL/TP)")
        print("   ✅ Paper trading (no real money)")
        print("   ✅ Real-time statistics")
        print("\n⚠️  DISCLAIMER:")
        print("   This is a DEMO/PAPER trading system.")
        print("   No real money is used or at risk.")
        print("   Results are for educational purposes only.")
        print("\n" + "="*70 + "\n")
