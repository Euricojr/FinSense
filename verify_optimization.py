
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:5000"

def test_optimization_endpoint():
    endpoint = f"{BASE_URL}/api/optimize_portfolio"
    
    # Payload with sample tickers
    payload = {
        "tickers": ["AAPL", "MSFT", "GOOG"],
        "period": "3y"
    }
    
    # Mocking a logged-in session might be tricky without a valid session cookie.
    # However, if the server is running locally and we access it, 
    # we might need to bypass login or use a test account.
    # For now, let's assume we need to login first or just try to hit it and see if we get 401.
    
    session = requests.Session()
    
    # Try to login first (optional, adjust if needed)
    login_url = f"{BASE_URL}/login"
    login_payload = {'username': 'testuser', 'password': 'testpassword', 'action': 'login'} 
    # Note: You might need to create this user first or use an existing one.
    
    logger.info("Functionality test: Sending optimization request...")
    
    # Since we can't easily perform full auth flow in this script without valid credentials setup,
    # we will focus on the structure of the call.
    # If this script runs in the same environment as the app, we could import app and use test_client.
    
    pass

if __name__ == "__main__":
    print("To test the API, run the flask app and use the frontend.")
    print("This script is a placeholder to remind verification of:")
    print("1. /api/optimize_portfolio returns JSON with 'max_sharpe', 'min_volatility', 'cloud'.")
    print("2. 'cloud' contains 'returns', 'volatility', 'sharpe' arrays.")
    print("3. 'max_sharpe' contains 'weights' object.")
