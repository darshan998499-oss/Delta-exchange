# Smart Agentic AI Trading Bot for Delta Exchange

एक advanced AI-powered trading bot जो Delta Exchange पर automated trading करता है।

## Features

✅ **Multiple Intelligent Agents:**
- Market Analysis Agent
- Risk Management Agent
- Trader Sentiment Agent
- Entry/Exit Decision Agent
- Position Management Agent

✅ **Advanced Analysis:**
- BTCUSDT Futures Analysis
- Option Chain Analysis
- OI (Open Interest) Analysis
- Funding Rate Analysis
- Chart Pattern Recognition

✅ **Smart Notifications:**
- Telegram Alerts
- WhatsApp Alerts
- Real-time Trade Signals

## Installation

```bash
git clone https://github.com/darshan998499-oss/delta-exchange.git
cd delta-exchange
pip install -r requirements.txt
```

## Configuration

1. Create `.env` file:
```
DELTA_API_KEY=your_key
DELTA_API_SECRET=your_secret
OPENAI_API_KEY=your_openai_key
TELEGRAM_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

2. Configure strategies in `config/strategies.yaml`

## Usage

```bash
python main.py
```

## Project Structure

```
delta-exchange/
├── agents/                 # All AI Agents
│   ├── market_analysis.py
│   ├── risk_manager.py
│   ├── trader_sentiment.py
│   ├── entry_exit.py
│   └── position_manager.py
├── api/                    # Delta Exchange API
│   └── delta_client.py
├── analysis/              # Technical Analysis
│   ├── indicators.py
│   ├── patterns.py
│   └── sentiment.py
├── notifications/         # Alert System
│   ├── telegram.py
│   └── whatsapp.py
├── data/                  # Data Management
│   └── database.py
├── config/               # Configuration
│   └── strategies.yaml
├── main.py              # Main Bot
└── requirements.txt
```

## License

MIT License
