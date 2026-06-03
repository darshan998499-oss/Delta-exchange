from typing import Dict, List, Optional
import pandas as pd

class PositionManagementAgent:
    """
    Manages all open positions
    - Tracks entry/exit points
    - Updates stop loss and take profit
    - Scales positions
    - Closes positions
    - Maintains position history
    """
    
    def __init__(self):
        self.name = "Position Management Agent"
        self.description = "Manages all open trading positions"
        self.positions: List[Dict] = []
        self.closed_positions: List[Dict] = []
    
    def open_position(self, symbol: str, direction: str, entry_price: float, quantity: float, 
                     stop_loss: float, take_profit: float, leverage: int = 1) -> Dict:
        """Open a new position"""
        
        position = {
            'id': len(self.positions) + 1,
            'symbol': symbol,
            'direction': direction,  # LONG or SHORT
            'entry_price': entry_price,
            'current_price': entry_price,
            'quantity': quantity,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'leverage': leverage,
            'opened_at': pd.Timestamp.now(),
            'status': 'OPEN',
            'pnl': 0,
            'pnl_percent': 0,
            'trade_history': []
        }
        
        self.positions.append(position)
        return position
    
    def update_position(self, position_id: int, current_price: float) -> Dict:
        """Update position with current price"""
        
        position = self._find_position(position_id)
        if not position:
            return None
        
        position['current_price'] = current_price
        
        # Calculate P&L
        if position['direction'] == 'LONG':
            pnl = (current_price - position['entry_price']) * position['quantity']
            pnl_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
        else:  # SHORT
            pnl = (position['entry_price'] - current_price) * position['quantity']
            pnl_percent = ((position['entry_price'] - current_price) / position['entry_price']) * 100
        
        position['pnl'] = pnl
        position['pnl_percent'] = pnl_percent
        
        return position
    
    def close_position(self, position_id: int, exit_price: float, exit_reason: str = "Manual Exit") -> Dict:
        """Close an open position"""
        
        position = self._find_position(position_id)
        if not position:
            return None
        
        # Calculate final P&L
        if position['direction'] == 'LONG':
            pnl = (exit_price - position['entry_price']) * position['quantity']
            pnl_percent = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        else:  # SHORT
            pnl = (position['entry_price'] - exit_price) * position['quantity']
            pnl_percent = ((position['entry_price'] - exit_price) / position['entry_price']) * 100
        
        closed_position = {
            **position,
            'exit_price': exit_price,
            'closed_at': pd.Timestamp.now(),
            'status': 'CLOSED',
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'exit_reason': exit_reason
        }
        
        self.closed_positions.append(closed_position)
        self.positions.remove(position)
        
        return closed_position
    
    def update_stop_loss(self, position_id: int, new_stop_loss: float) -> Dict:
        """Update stop loss for a position"""
        
        position = self._find_position(position_id)
        if not position:
            return None
        
        position['stop_loss'] = new_stop_loss
        position['trade_history'].append({
            'timestamp': pd.Timestamp.now(),
            'action': 'STOP_LOSS_UPDATE',
            'value': new_stop_loss
        })
        
        return position
    
    def update_take_profit(self, position_id: int, new_take_profit: float) -> Dict:
        """Update take profit for a position"""
        
        position = self._find_position(position_id)
        if not position:
            return None
        
        position['take_profit'] = new_take_profit
        position['trade_history'].append({
            'timestamp': pd.Timestamp.now(),
            'action': 'TAKE_PROFIT_UPDATE',
            'value': new_take_profit
        })
        
        return position
    
    def scale_out_position(self, position_id: int, scale_percent: float, exit_price: float) -> Dict:
        """Partially close a position (scale out)"""
        
        position = self._find_position(position_id)
        if not position:
            return None
        
        scale_quantity = position['quantity'] * (scale_percent / 100)
        remaining_quantity = position['quantity'] - scale_quantity
        
        # Calculate exit P&L
        if position['direction'] == 'LONG':
            exit_pnl = (exit_price - position['entry_price']) * scale_quantity
        else:
            exit_pnl = (position['entry_price'] - exit_price) * scale_quantity
        
        # Update position quantity
        position['quantity'] = remaining_quantity
        
        scale_record = {
            'timestamp': pd.Timestamp.now(),
            'action': 'SCALE_OUT',
            'scale_percent': scale_percent,
            'scale_quantity': scale_quantity,
            'exit_price': exit_price,
            'pnl': exit_pnl
        }
        
        position['trade_history'].append(scale_record)
        
        return position
    
    def get_open_positions(self) -> List[Dict]:
        """Get all open positions"""
        return self.positions
    
    def get_position_summary(self) -> Dict:
        """Get summary of all positions"""
        
        total_pnl = sum(p['pnl'] for p in self.positions)
        total_value = sum(p['current_price'] * p['quantity'] for p in self.positions)
        
        long_positions = [p for p in self.positions if p['direction'] == 'LONG']
        short_positions = [p for p in self.positions if p['direction'] == 'SHORT']
        
        return {
            'total_open_positions': len(self.positions),
            'long_positions': len(long_positions),
            'short_positions': len(short_positions),
            'total_position_value': total_value,
            'total_pnl': total_pnl,
            'total_pnl_percent': (total_pnl / total_value * 100) if total_value > 0 else 0,
            'closed_trades': len(self.closed_positions)
        }
    
    def _find_position(self, position_id: int) -> Optional[Dict]:
        """Find position by ID"""
        for position in self.positions:
            if position['id'] == position_id:
                return position
        return None
