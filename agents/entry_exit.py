from typing import Dict
from enum import Enum

class TradeSignal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    EXIT = "EXIT"

class EntryExitAgent:
    """
    Decides entry and exit signals based on all agent inputs
    - Combines market analysis, sentiment, and risk management
    - Generates BUY, SELL, HOLD, EXIT signals
    - Manages entry/exit logic
    - Handles special conditions (breakouts, reversals, etc.)
    """
    
    def __init__(self):
        self.name = "Entry/Exit Decision Agent"
        self.description = "Generates entry and exit trading signals"
    
    def should_buy(self, market_signal: Dict, sentiment_signal: Dict, current_positions: int, max_positions: int) -> bool:
        """Determine if should enter BUY trade"""
        
        # Check position limit
        if current_positions >= max_positions:
            return False
        
        # Market conditions
        trend_bullish = market_signal.get('trend') in ['UPTREND', 'STRONG_UPTREND']
        rsi_not_overbought = market_signal.get('rsi') != 'OVERBOUGHT'
        macd_bullish = market_signal.get('macd') == 'BULLISH'
        volume_good = market_signal.get('volume') in ['HIGH_VOLUME', 'ABOVE_AVERAGE']
        
        # Sentiment conditions
        sentiment_bullish = sentiment_signal.get('sentiment') == 'BULLISH'
        
        # Buy signal: Trend + RSI + MACD + Volume + Sentiment
        buy_conditions = [trend_bullish, rsi_not_overbought, macd_bullish, volume_good, sentiment_bullish]
        
        # Require at least 4 out of 5 conditions
        return sum(buy_conditions) >= 4
    
    def should_sell(self, market_signal: Dict, sentiment_signal: Dict, current_price: float, entry_price: float) -> bool:
        """Determine if should enter SELL trade"""
        
        # Market conditions
        trend_bearish = market_signal.get('trend') in ['DOWNTREND', 'STRONG_DOWNTREND']
        rsi_not_oversold = market_signal.get('rsi') != 'OVERSOLD'
        macd_bearish = market_signal.get('macd') == 'BEARISH'
        volume_good = market_signal.get('volume') in ['HIGH_VOLUME', 'ABOVE_AVERAGE']
        
        # Sentiment conditions
        sentiment_bearish = sentiment_signal.get('sentiment') == 'BEARISH'
        
        # Sell signal: Trend + RSI + MACD + Volume + Sentiment
        sell_conditions = [trend_bearish, rsi_not_oversold, macd_bearish, volume_good, sentiment_bearish]
        
        # Require at least 4 out of 5 conditions
        return sum(sell_conditions) >= 4
    
    def should_exit_long(self, market_signal: Dict, current_price: float, entry_price: float, stop_loss: float, take_profit: float) -> bool:
        """Determine if should exit LONG position"""
        
        # Hard stops
        if current_price <= stop_loss:
            return True
        
        if current_price >= take_profit:
            return True
        
        # Market reversal
        if market_signal.get('trend') in ['DOWNTREND', 'STRONG_DOWNTREND']:
            if market_signal.get('rsi') == 'OVERBOUGHT':
                return True
        
        return False
    
    def should_exit_short(self, market_signal: Dict, current_price: float, entry_price: float, stop_loss: float, take_profit: float) -> bool:
        """Determine if should exit SHORT position"""
        
        # Hard stops
        if current_price >= stop_loss:
            return True
        
        if current_price <= take_profit:
            return True
        
        # Market reversal
        if market_signal.get('trend') in ['UPTREND', 'STRONG_UPTREND']:
            if market_signal.get('rsi') == 'OVERSOLD':
                return True
        
        return False
    
    def generate_buy_signal(self, market_signal: Dict, sentiment_signal: Dict, current_positions: int, max_positions: int) -> Dict:
        """Generate BUY signal with confidence score"""
        
        if not self.should_buy(market_signal, sentiment_signal, current_positions, max_positions):
            return {
                'signal': TradeSignal.HOLD,
                'confidence': 0,
                'reason': 'Buy conditions not met'
            }
        
        # Calculate confidence score
        confidence = self._calculate_signal_confidence(market_signal, sentiment_signal, 'BUY')
        
        return {
            'signal': TradeSignal.BUY,
            'confidence': confidence,
            'entry_level': market_signal.get('current_price'),
            'support': market_signal.get('support_resistance', {}).get('support'),
            'reason': 'All conditions aligned for entry'
        }
    
    def generate_sell_signal(self, market_signal: Dict, sentiment_signal: Dict) -> Dict:
        """Generate SELL signal with confidence score"""
        
        if not self.should_sell(market_signal, sentiment_signal, market_signal.get('current_price'), 0):
            return {
                'signal': TradeSignal.HOLD,
                'confidence': 0,
                'reason': 'Sell conditions not met'
            }
        
        # Calculate confidence score
        confidence = self._calculate_signal_confidence(market_signal, sentiment_signal, 'SELL')
        
        return {
            'signal': TradeSignal.SELL,
            'confidence': confidence,
            'entry_level': market_signal.get('current_price'),
            'resistance': market_signal.get('support_resistance', {}).get('resistance'),
            'reason': 'All conditions aligned for entry'
        }
    
    def generate_exit_signal(self, market_signal: Dict, position: Dict) -> Dict:
        """Generate EXIT signal for open position"""
        
        position_type = position.get('type')  # LONG or SHORT
        current_price = market_signal.get('current_price')
        entry_price = position.get('entry_price')
        stop_loss = position.get('stop_loss')
        take_profit = position.get('take_profit')
        
        should_exit = False
        exit_reason = ""
        
        if position_type == 'LONG':
            should_exit = self.should_exit_long(market_signal, current_price, entry_price, stop_loss, take_profit)
            if current_price <= stop_loss:
                exit_reason = "Stop loss hit"
            elif current_price >= take_profit:
                exit_reason = "Take profit hit"
            else:
                exit_reason = "Market reversal detected"
        
        elif position_type == 'SHORT':
            should_exit = self.should_exit_short(market_signal, current_price, entry_price, stop_loss, take_profit)
            if current_price >= stop_loss:
                exit_reason = "Stop loss hit"
            elif current_price <= take_profit:
                exit_reason = "Take profit hit"
            else:
                exit_reason = "Market reversal detected"
        
        return {
            'signal': TradeSignal.EXIT if should_exit else TradeSignal.HOLD,
            'reason': exit_reason if should_exit else "Position still valid",
            'pnl': ((current_price - entry_price) / entry_price * 100) if position_type == 'LONG' else ((entry_price - current_price) / entry_price * 100)
        }
    
    def _calculate_signal_confidence(self, market_signal: Dict, sentiment_signal: Dict, signal_type: str) -> float:
        """Calculate confidence score for a signal (0-1)"""
        
        confidence_factors = 0
        max_factors = 0
        
        # Trend confidence
        trend = market_signal.get('trend')
        if signal_type == 'BUY' and trend in ['STRONG_UPTREND']:
            confidence_factors += 1.0
        elif signal_type == 'BUY' and trend in ['UPTREND']:
            confidence_factors += 0.7
        elif signal_type == 'SELL' and trend in ['STRONG_DOWNTREND']:
            confidence_factors += 1.0
        elif signal_type == 'SELL' and trend in ['DOWNTREND']:
            confidence_factors += 0.7
        else:
            confidence_factors += 0.3
        max_factors += 1
        
        # MACD confidence
        macd = market_signal.get('macd')
        if (signal_type == 'BUY' and macd == 'BULLISH') or (signal_type == 'SELL' and macd == 'BEARISH'):
            confidence_factors += 1.0
        else:
            confidence_factors += 0.5
        max_factors += 1
        
        # Sentiment confidence
        sentiment_confidence = sentiment_signal.get('confidence')
        if sentiment_confidence == 'HIGH':
            confidence_factors += 1.0
        elif sentiment_confidence == 'MEDIUM':
            confidence_factors += 0.6
        else:
            confidence_factors += 0.3
        max_factors += 1
        
        return min(confidence_factors / max_factors, 1.0)
