import requests
import json
import hmac
import hashlib
import time
from typing import Dict, List, Optional
from datetime import datetime

class DeltaClient:
    """Delta Exchange API Client"""
    
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://api.delta.exchange"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_signature(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """Generate request signature for Delta Exchange"""
        message = f"{timestamp}\n{method}\n{path}\n{body}"
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Delta Exchange"""
        timestamp = str(int(time.time() * 1000))
        path = f"/v2{endpoint}"
        body = json.dumps(data) if data else ""
        
        signature = self._get_signature(timestamp, method, path, body)
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "X-API-SIGNATURE": signature,
            "X-REQUEST-TIMESTAMP": timestamp
        }
        
        url = f"{self.base_url}{path}"
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(url, headers=headers, data=body)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response.json()
        except Exception as e:
            print(f"Error making request: {e}")
            return {"error": str(e)}
    
    def get_ticker(self, symbol: str) -> Dict:
        """Get ticker data for symbol"""
        return self._make_request("GET", f"/tickers?symbol={symbol}")
    
    def get_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """Get order book for symbol"""
        return self._make_request("GET", f"/orderbook?symbol={symbol}&limit={limit}")
    
    def get_positions(self) -> List[Dict]:
        """Get open positions"""
        response = self._make_request("GET", "/positions")
        return response.get("result", [])
    
    def get_orders(self, symbol: str) -> List[Dict]:
        """Get open orders for symbol"""
        response = self._make_request("GET", f"/orders?symbol={symbol}")
        return response.get("result", [])
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None, leverage: int = 1) -> Dict:
        """Place a new order"""
        data = {
            "symbol": symbol,
            "side": side.upper(),
            "order_type": order_type.upper(),
            "size": quantity,
            "leverage": leverage
        }
        
        if price and order_type.upper() == "LIMIT":
            data["price"] = price
        
        return self._make_request("POST", "/orders", data)
    
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an order"""
        return self._make_request("POST", f"/orders/{order_id}/cancel")
    
    def get_funding_rate(self, symbol: str) -> Dict:
        """Get funding rate for symbol"""
        return self._make_request("GET", f"/funding-rates?symbol={symbol}")
    
    def get_open_interest(self, symbol: str) -> Dict:
        """Get open interest for symbol"""
        return self._make_request("GET", f"/open-interests?symbol={symbol}")
    
    def get_klines(self, symbol: str, resolution: str = "1m", limit: int = 100) -> List[Dict]:
        """Get candlestick data"""
        response = self._make_request("GET", f"/klines?symbol={symbol}&resolution={resolution}&limit={limit}")
        return response.get("result", [])
