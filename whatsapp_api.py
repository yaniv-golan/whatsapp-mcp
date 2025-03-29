#!/usr/bin/env python3
import requests
import json
from typing import Tuple, Dict, Any, Optional

class WhatsAppAPI:
    """
    Client for the WhatsApp bridge REST API
    """
    
    def __init__(self, server_url: str = "http://localhost:8080"):
        """
        Initialize the WhatsApp API client
        
        Args:
            server_url (str): The base URL of the WhatsApp bridge server
        """
        self.server_url = server_url.rstrip('/')
        
    def send_message(self, phone: str, message: str) -> Tuple[bool, str]:
        """
        Send a WhatsApp message
        
        Args:
            phone (str): The phone number to send the message to (without any + or spaces)
            message (str): The message content to send
        
        Returns:
            tuple: (success (bool), response_message (str))
        """
        # Create the API endpoint URL
        url = f"{self.server_url}/api/send"
        
        # Create the request payload
        payload = {
            "phone": phone,
            "message": message
        }
        
        # Set headers for JSON content
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            # Make the POST request to the API
            response = requests.post(
                url, 
                data=json.dumps(payload),
                headers=headers
            )
            
            # Parse the response
            if response.status_code == 200:
                result = response.json()
                return True, result.get("message", "Message sent successfully")
            else:
                # Try to get error message from response
                try:
                    error_msg = response.json().get("message", response.text)
                except:
                    error_msg = f"HTTP Error: {response.status_code} - {response.text}"
                return False, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"

# Simple usage example
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python whatsapp_api.py <phone> <message>")
        sys.exit(1)
        
    phone = sys.argv[1]
    message = sys.argv[2]
    
    client = WhatsAppAPI()
    success, response = client.send_message(phone, message)
    
    if success:
        print(f"✓ Success: {response}")
    else:
        print(f"✗ Error: {response}")
        sys.exit(1) 