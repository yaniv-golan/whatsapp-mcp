#!/usr/bin/env python3
import requests
import json
import argparse

def send_whatsapp_message(phone, message, server_url="http://localhost:8080"):
    """
    Send a WhatsApp message using the bridge API
    
    Args:
        phone (str): The phone number to send the message to (without any + or spaces)
        message (str): The message content to send
        server_url (str): The URL of the WhatsApp bridge server
        
    Returns:
        tuple: (success (bool), response_message (str))
    """
    # Create the API endpoint URL
    url = f"{server_url}/api/send"
    
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

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Send WhatsApp messages via bridge API")
    parser.add_argument("phone", help="Phone number to send message to (without + or spaces)")
    parser.add_argument("message", help="Message content to send")
    parser.add_argument("--server", default="http://localhost:8080", help="WhatsApp bridge server URL")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Send the message
    success, message = send_whatsapp_message(args.phone, args.message, args.server)
    
    # Print the result
    if success:
        print(f"✓ Success: {message}")
    else:
        print(f"✗ Error: {message}")
        exit(1)

if __name__ == "__main__":
    main() 