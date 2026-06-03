import pandas as pd
import numpy as np
from typing import Dict, List
import ta

class MarketAnalysisAgent:
    """
    Analyzes market data using technical indicators and patterns
    - RSI, MACD, Bollinger Bands
    - Support/Resistance levels
    - Trend analysis
    - Volume analysis
    """
    
    def __init__(self):
        self.name = "Market Analysis Agent"
        self.description = "Analyzes market data and technical indicators"
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        
        # RSI (Relative Strength Index)
        df['RSI'] = ta.momentum.rsi(df['close'], window=14)
        
        # MACD
        macd = ta.trend.MACD(df['close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()
        
        # Bollinger Bands
        bbands = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
        df['BB_upper'] = bbands.bollinger_hband()
        df['BB_middle'] = bbands.bollinger_mavg()
        df['BB_lower'] = bbands.bollinger_lband()
        
        # Moving Averages
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean()
        df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # ATR (Average True Range)
        df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
        
        # Volume Analysis
        df['Volume_MA'] = df['volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['volume'] / df['Volume_MA']
        
        return df
    
    def detect_support_resistance(self, df: pd.DataFrame, lookback: int = 20) -> Dict:
        """Detect support and resistance levels"""
        recent_data = df.tail(lookback)
        
        resistance = recent_data['high'].max()
        support = recent_data['low'].min()
        
        return {
            'support': support,
            'resistance': resistance,
            'middle': (support + resistance) / 2
        }
    
    def analyze_trend(self, df: pd.DataFrame) -> str:
        """Determine market trend"""
        sma_20 = df['SMA_20'].iloc[-1]
        sma_50 = df['SMA_50'].iloc[-1]
        current_price = df['close'].iloc[-1]
        
        if current_price > sma_20 > sma_50:
            return "STRONG_UPTREND"
        elif current_price > sma_20:
            return "UPTREND"
        elif current_price < sma_20 < sma_50:
            return "STRONG_DOWNTREND"
        elif current_price < sma_20:
            return "DOWNTREND"
        else:
            return "NEUTRAL"
    
    def analyze_rsi(self, df: pd.DataFrame) -> str:
        """Analyze RSI signal"""
        rsi = df['RSI'].iloc[-1]
        
        if rsi > 70:
            return "OVERBOUGHT"
        elif rsi < 30:
            return "OVERSOLD"
        else:
            return "NEUTRAL"
    
    def analyze_macd(self, df: pd.DataFrame) -> str:
        """Analyze MACD signal"""
        macd = df['MACD'].iloc[-1]
        signal = df['MACD_signal'].iloc[-1]
        
        if macd > signal:
            return "BULLISH"
        elif macd < signal:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def detect_bollinger_bands_signal(self, df: pd.DataFrame) -> str:
        """Detect Bollinger Bands signals"""
        close = df['close'].iloc[-1]
        upper = df['BB_upper'].iloc[-1]
        lower = df['BB_lower'].iloc[-1]
        middle = df['BB_middle'].iloc[-1]
        
        if close > upper:
            return "OVERBOUGHT"
        elif close < lower:
            return "OVERSOLD"
        elif close > middle:
            return "BULLISH"
        else:
            return "BEARISH"
    
    def analyze_volume(self, df: pd.DataFrame) -> str:
        """Analyze volume signal"""
        volume_ratio = df['Volume_Ratio'].iloc[-1]
        
        if volume_ratio > 1.5:
            return "HIGH_VOLUME"
        elif volume_ratio > 1.2:
            return "ABOVE_AVERAGE"
        else:
            return "NORMAL"
    
    def generate_signal(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive market signal"""
        
        df = self.calculate_indicators(df)
        
        signal = {
            'timestamp': pd.Timestamp.now(),
            'trend': self.analyze_trend(df),
            'rsi': self.analyze_rsi(df),
            'macd': self.analyze_macd(df),
            'bollinger_bands': self.detect_bollinger_bands_signal(df),
            'volume': self.analyze_volume(df),
            'support_resistance': self.detect_support_resistance(df),
            'current_price': df['close'].iloc[-1],
            'atr': df['ATR'].iloc[-1]
        }
        
        return signal
