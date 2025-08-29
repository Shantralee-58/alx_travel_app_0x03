#!/usr/bin/env python3
"""
Simple script to test Chapa API connection and credentials.
Run this script to verify your Chapa setup is working correctly.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def validate_key_format():
    """Validate the format of Chapa API keys."""
    secret_key = os.getenv('CHAPA_SECRET_KEY')
    public_key = os.getenv('CHAPA_PUBLIC_KEY')

    print("\nValidating API Key Formats:")

    if secret_key:
        if secret_key.startswith('CHASECK_TEST-'):
            print("Secret Key: Valid TEST key format")
        elif secret_key.startswith('CHASECK_LIVE-'):
            print("Secret Key: Valid LIVE key format")
        else:
            print("Secret Key: Invalid format")
            return False
    else:
        print("Secret Key: Not found")
        return False

    if public_key:
        if public_key.startswith('CHAPUBK_TEST-'):
            print("Public Key: Valid TEST key format")
        elif public_key.startswith('CHAPUBK_LIVE-'):
            print("Public Key: Valid LIVE key format")
        else:
            print("Public Key: Invalid format")
            return False
    else:
        print("Public Key: Not found (optional for server-side integration)")

    return True

def test_chapa_connection():
    """Test connection to Chapa API."""
    secret_key = os.getenv('CHAPA_SECRET_KEY')
    base_url = os.getenv('CHAPA_BASE_URL', 'https://api.chapa.co/v1')

    if not secret_key:
        print("Error: CHAPA_SECRET_KEY not found in environment variables")
        return False

    print(f"Using Secret Key: {secret_key[:20]}...")
    print(f"Base URL: {base_url}")

    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }

    test_payload = {
        "amount": "100",
        "currency": "ETB",
        "email": "lindiwekhumalo833@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "tx_ref": "test-tx-ref-12345"
    }

    try:
        response = requests.post(
            f"{base_url}/transaction/initialize",
            json=test_payload,
            headers=headers,
            timeout=10
        )

        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            print("Success: Chapa API connection successful!")
            data = response.json()
            print(f"Response: {data}")
            return True
        elif response.status_code == 401:
            print("Error: Invalid API credentials (401 Unauthorized)")
            return False
        elif response.status_code == 403:
            print("Error: Access forbidden (403 Forbidden)")
            return False
        else:
            print(f"Warning: Unexpected response ({response.status_code})")
            print(f"Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error: Network request failed - {str(e)}")
        return False
    except Exception as e:
        print(f"Error: Unexpected error - {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Chapa API Setup...")
    print("=" * 50)

    # Validate API key formats
    if not validate_key_format():
        print("\nKey validation failed. Please check your API keys.")
        sys.exit(1)

    # Test Chapa API connection
    print("\nTesting API Connection...")
    if test_chapa_connection():
        print("\nAll tests passed! Your Chapa setup is ready.")
    else:
        print("\nConnection test failed. Please check your credentials and try again.")
        sys.exit(1)

