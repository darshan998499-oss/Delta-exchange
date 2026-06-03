from typing import Dict, List

class TraderSentimentAgent:
    """
    Analyzes professional trader sentiment and behavior
    - Tracks whale movements
    - Monitors liquidation data
    - Analyzes option flow
    - Tracks funding rates
    - Monitors large order placements
    """
    
    def __init__(self):
        self.name = "Trader Sentiment Agent"
        self.description = "Analyzes professional trader sentiment and on-chain data"
    
    def analyze_funding_rate(self, funding_rate: float, funding_rate_history: List[float]) -> str:
        """Analyze funding rate sentiment"""
        
        avg_funding_rate = sum(funding_rate_history[-10:]) / len(funding_rate_history[-10:]) if len(funding_rate_history) > 0 else 0
        
        if funding_rate > 0.001:
            return "BULLISH_EXTREME"
        elif funding_rate > 0.0005:
            return "BULLISH"
        elif funding_rate < -0.001:
            return "BEARISH_EXTREME"
        elif funding_rate < -0.0005:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def analyze_open_interest(self, current_oi: float, previous_oi: float) -> str:
        """Analyze open interest changes"""
        
        oi_change_percent = ((current_oi - previous_oi) / previous_oi * 100) if previous_oi > 0 else 0
        
        if oi_change_percent > 5:
            return "ACCUMULATING"
        elif oi_change_percent > 2:
            return "SLOWLY_ACCUMULATING"
        elif oi_change_percent < -5:
            return "LIQUIDATING"
        elif oi_change_percent < -2:
            return "SLOWLY_LIQUIDATING"
        else:
            return "STABLE"
    
    def analyze_liquidation_data(self, liquidation_data: Dict) -> str:
        """Analyze liquidation data sentiment"""
        
        long_liquidations = liquidation_data.get('long_liquidations', 0)
        short_liquidations = liquidation_data.get('short_liquidations', 0)
        
        total_liquidations = long_liquidations + short_liquidations
        
        if total_liquidations == 0:
            return "NEUTRAL"
        
        long_percent = (long_liquidations / total_liquidations * 100)
        
        if long_percent > 65:
            return "EXTREME_SHORT_LIQUIDATIONS"
        elif long_percent > 55:
            return "MORE_SHORT_LIQUIDATIONS"
        elif long_percent < 35:
            return "EXTREME_LONG_LIQUIDATIONS"
        elif long_percent < 45:
            return "MORE_LONG_LIQUIDATIONS"
        else:
            return "BALANCED"
    
    def analyze_option_flow(self, put_call_ratio: float) -> str:
        """Analyze options market sentiment (Put/Call ratio)"""
        
        if put_call_ratio > 1.2:
            return "VERY_BEARISH"
        elif put_call_ratio > 0.8:
            return "BEARISH"
        elif put_call_ratio < 0.6:
            return "VERY_BULLISH"
        elif put_call_ratio < 0.9:
            return "BULLISH"
        else:
            return "NEUTRAL"
    
    def analyze_whale_movements(self, large_orders: List[Dict]) -> str:
        """Analyze large whale order placements"""
        
        if not large_orders:
            return "NO_WHALE_ACTIVITY"
        
        buy_orders = sum(1 for order in large_orders if order['side'] == 'BUY')
        sell_orders = sum(1 for order in large_orders if order['side'] == 'SELL')
        
        total_orders = buy_orders + sell_orders
        
        if total_orders == 0:
            return "NO_WHALE_ACTIVITY"
        
        buy_percent = (buy_orders / total_orders * 100)
        
        if buy_percent > 70:
            return "WHALE_BUYING"
        elif buy_percent > 55:
            return "WHALE_BULLISH"
        elif buy_percent < 30:
            return "WHALE_SELLING"
        elif buy_percent < 45:
            return "WHALE_BEARISH"
        else:
            return "WHALE_BALANCED"
    
    def analyze_taker_volume(self, taker_buy_volume: float, taker_sell_volume: float) -> str:
        """Analyze taker buy vs sell volume"""
        
        total_volume = taker_buy_volume + taker_sell_volume
        
        if total_volume == 0:
            return "NEUTRAL"
        
        buy_percent = (taker_buy_volume / total_volume * 100)
        
        if buy_percent > 60:
            return "STRONG_BUYING_PRESSURE"
        elif buy_percent > 55:
            return "BUYING_PRESSURE"
        elif buy_percent < 40:
            return "STRONG_SELLING_PRESSURE"
        elif buy_percent < 45:
            return "SELLING_PRESSURE"
        else:
            return "BALANCED"
    
    def get_composite_sentiment(self, 
                               funding_rate_sentiment: str,
                               oi_sentiment: str,
                               liquidation_sentiment: str,
                               option_sentiment: str,
                               whale_sentiment: str) -> Dict:
        """Generate composite sentiment score"""
        
        sentiment_weights = {
            'funding_rate': 0.2,
            'open_interest': 0.2,
            'liquidations': 0.2,
            'options': 0.2,
            'whale_movements': 0.2
        }
        
        bullish_indicators = {
            'BULLISH_EXTREME': 1.0,
            'BULLISH': 0.7,
            'ACCUMULATING': 0.6,
            'SLOWLY_ACCUMULATING': 0.4,
            'EXTREME_SHORT_LIQUIDATIONS': 0.9,
            'MORE_SHORT_LIQUIDATIONS': 0.6,
            'VERY_BULLISH': 0.9,
            'WHALE_BUYING': 0.8,
            'WHALE_BULLISH': 0.6,
            'STRONG_BUYING_PRESSURE': 0.8
        }
        
        sentiments = {
            'funding_rate': funding_rate_sentiment,
            'open_interest': oi_sentiment,
            'liquidations': liquidation_sentiment,
            'options': option_sentiment,
            'whale_movements': whale_sentiment
        }
        
        composite_score = 0
        for key, sentiment in sentiments.items():
            score = bullish_indicators.get(sentiment, 0.5)
            composite_score += score * sentiment_weights[key]
        
        return {
            'composite_score': composite_score,
            'sentiment': 'BULLISH' if composite_score > 0.6 else 'BEARISH' if composite_score < 0.4 else 'NEUTRAL',
            'breakdown': sentiments,
            'confidence': 'HIGH' if abs(composite_score - 0.5) > 0.15 else 'MEDIUM'
        }
