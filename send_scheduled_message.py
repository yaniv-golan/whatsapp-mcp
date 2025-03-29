#!/usr/bin/env python3
import argparse
import datetime
import time
import json
import os
from whatsapp_api import WhatsAppAPI

def parse_datetime(dt_str):
    """
    Parse a datetime string in the format YYYY-MM-DD HH:MM
    """
    try:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Date-time must be in format: YYYY-MM-DD HH:MM")

def schedule_message(phone, message, send_time, server_url="http://localhost:8080"):
    """
    Schedule a WhatsApp message to be sent at a specific time
    
    Args:
        phone (str): The phone number to send to
        message (str): The message content
        send_time (datetime): When to send the message
        server_url (str): The WhatsApp bridge server URL
    """
    # Initialize the WhatsApp API client
    client = WhatsAppAPI(server_url)
    
    # Calculate wait time
    now = datetime.datetime.now()
    if send_time < now:
        print("⚠️ The specified time is in the past. Sending immediately.")
        wait_seconds = 0
    else:
        wait_seconds = (send_time - now).total_seconds()
        
        # Format the wait time for display
        if wait_seconds < 60:
            wait_str = f"{int(wait_seconds)} seconds"
        elif wait_seconds < 3600:
            wait_str = f"{int(wait_seconds / 60)} minutes"
        else:
            hours = int(wait_seconds / 3600)
            minutes = int((wait_seconds % 3600) / 60)
            wait_str = f"{hours} hours, {minutes} minutes"
            
        print(f"⏰ Message scheduled to be sent in {wait_str}")
        print(f"📅 Scheduled time: {send_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save scheduled message info to file for tracking
    schedule_id = int(time.time())
    schedule_info = {
        "id": schedule_id,
        "phone": phone,
        "message": message,
        "scheduled_time": send_time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "scheduled"
    }
    
    # Create directory for storing scheduled messages if it doesn't exist
    os.makedirs("scheduled_messages", exist_ok=True)
    
    # Save schedule info to file
    with open(f"scheduled_messages/{schedule_id}.json", "w") as f:
        json.dump(schedule_info, f, indent=2)
    
    # Wait until the scheduled time
    if wait_seconds > 0:
        time.sleep(wait_seconds)
    
    # Send the message
    print(f"📤 Sending message to {phone}...")
    success, response = client.send_message(phone, message)
    
    # Update schedule info with result
    schedule_info["status"] = "sent" if success else "failed"
    schedule_info["result"] = response
    schedule_info["sent_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save updated info
    with open(f"scheduled_messages/{schedule_id}.json", "w") as f:
        json.dump(schedule_info, f, indent=2)
    
    # Print result
    if success:
        print(f"✓ Success: {response}")
        return True
    else:
        print(f"✗ Error: {response}")
        return False

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Schedule a WhatsApp message to be sent at a specific time")
    parser.add_argument("phone", help="Phone number to send message to (without + or spaces)")
    parser.add_argument("message", help="Message content to send")
    parser.add_argument("--time", required=True, help="When to send the message (format: YYYY-MM-DD HH:MM)")
    parser.add_argument("--server", default="http://localhost:8080", help="WhatsApp bridge server URL")
    
    args = parser.parse_args()
    
    try:
        # Parse the send time
        send_time = parse_datetime(args.time)
        
        # Schedule the message
        schedule_message(args.phone, args.message, send_time, args.server)
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 