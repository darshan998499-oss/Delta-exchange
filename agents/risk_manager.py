import pandas as pd
from typing import Dict, List, Optional

class RiskManagementAgent:
    """
    Manages risk for trades
    - Position sizing
    - Stop loss calculation
    - Take profit levels
    - Portfolio risk monitoring
    - Risk/Reward ratio validation
    """
    
    def __init__(self, account_balance: float, max_risk_percent: float = 1.0):
        self.name = "Risk Management Agent"
        self.description = "Manages trading risk and position sizing"
        self.account_balance = account_balance
        self.max_risk_percent = max_risk_percent
    
    def calculate_position_size(self, entry_price: float, stop_loss_price: float) -> float:
        """Calculate position size based on risk management rules"""
        
        risk_amount = (self.account_balance * self.max_risk_percent) / 100
        price_diff = abs(entry_price - stop_loss_price)
        
        if price_diff == 0:
            return 0
        
        position_size = risk_amount / price_diff
        return position_size
    
    def calculate_stop_loss(self, entry_price: float, direction: str, atr: float) -> float:
        """Calculate stop loss level using ATR"""
        
        if direction == "BUY":
            stop_loss = entry_price - (2 * atr)
        else:  # SELL
            stop_loss = entry_price + (2 * atr)
        
        return stop_loss
    
    def calculate_take_profit(self, entry_price: float, direction: str, risk_reward_ratio: float = 2.0, atr: float = None) -> float:
        """Calculate take profit level"""
        
        if atr is None:
            # Default to 2% of entry price
            tp_percent = 2.0
            if direction == "BUY":
                take_profit = entry_price * (1 + tp_percent / 100)
            else:
                take_profit = entry_price * (1 - tp_percent / 100)
        else:
            if direction == "BUY":
                stop_loss = entry_price - (2 * atr)
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * risk_reward_ratio)
            else:
                stop_loss = entry_price + (2 * atr)
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * risk_reward_ratio)
        
        return take_profit
    
    def validate_risk_reward(self, entry_price: float, stop_loss: float, take_profit: float, min_ratio: float = 1.5) -> bool:
        """Validate risk/reward ratio"""
        
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        
        if risk == 0:
            return False
        
        ratio = reward / risk
        return ratio >= min_ratio
    
    def calculate_portfolio_risk(self, open_positions: List[Dict]) -> Dict:
        """Calculate total portfolio risk"""
        
        total_risk_amount = 0
        total_positions = len(open_positions)
        
        for position in open_positions:
            entry_price = position.get('entry_price', 0)
            stop_loss = position.get('stop_loss', 0)
            quantity = position.get('quantity', 0)
            
            position_risk = abs(entry_price - stop_loss) * quantity
            total_risk_amount += position_risk
        
        portfolio_risk_percent = (total_risk_amount / self.account_balance * 100) if self.account_balance > 0 else 0
        
        return {
            'total_risk_amount': total_risk_amount,
            'portfolio_risk_percent': portfolio_risk_percent,
            'open_positions': total_positions,
            'max_additional_risk': (self.account_balance * self.max_risk_percent) / 100
        }
    
    def can_open_position(self, required_risk: float) -> bool:
        """Check if new position can be opened based on risk limits"""
        
        max_risk = (self.account_balance * self.max_risk_percent) / 100
        return required_risk <= max_risk
    
    def apply_trailing_stop(self, current_price: float, entry_price: float, stop_loss: float, trailing_percent: float = 0.5) -> float:
        """Apply trailing stop"""
        
        trailing_amount = current_price * (trailing_percent / 100)
        
        if entry_price < current_price:  # Long position
            new_stop_loss = current_price - trailing_amount
            return max(stop_loss, new_stop_loss)
        else:  # Short position
            new_stop_loss = current_price + trailing_amount
            return min(stop_loss, new_stop_loss)
    
    def generate_risk_report(self, open_positions: List[Dict]) -> Dict:
        """Generate comprehensive risk report"""
        
        portfolio_risk = self.calculate_portfolio_risk(open_positions)
        
        report = {
            'timestamp': pd.Timestamp.now(),
            'account_balance': self.account_balance,
            'portfolio_risk': portfolio_risk,
            'max_risk_allowed': (self.account_balance * self.max_risk_percent) / 100,
            'risk_headroom': (self.account_balance * self.max_risk_percent) / 100 - portfolio_risk['total_risk_amount'],
            'open_positions': len(open_positions),
            'can_open_new_position': portfolio_risk['total_risk_amount'] < (self.account_balance * self.max_risk_percent) / 100
        }
        
        return report
