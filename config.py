import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Delta Exchange API
    DELTA_API_KEY = os.getenv("DELTA_API_KEY")
    DELTA_API_SECRET = os.getenv("DELTA_API_SECRET")
    DELTA_API_URL = "https://api.delta.exchange"
    
    # OpenAI API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # WhatsApp (via Twilio)
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_FROM = os.getenv("TWILIO_PHONE_FROM")
    TWILIO_PHONE_TO = os.getenv("TWILIO_PHONE_TO")
    
    # Trading Config
    SYMBOL = "BTCUSDT"
    LEVERAGE = 5
    POSITION_SIZE_USDT = 100
    MAX_POSITIONS = 3
    
    # Risk Management
    STOP_LOSS_PERCENT = 2.0
    TAKE_PROFIT_PERCENT = 5.0
    MAX_RISK_PER_TRADE = 1.0
    
    # Agent Config
    AGENT_UPDATE_INTERVAL = 300  # 5 minutes
    ANALYSIS_LOOKBACK = 100  # candles
