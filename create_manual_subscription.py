#!/usr/bin/env python3
"""
Helper script to manually create a subscription file.
Usage: python create_manual_subscription.py username
"""

import base64
import sys
import os

def create_manual_subscription(username, server_urls):
    """
    Create a manual subscription file for a user.
    
    Args:
        username: The username (will create subscriptions/username.txt)
        server_urls: List of server URLs (V2Ray format)
    """
    subscription_dir = 'subscriptions'
    if not os.path.exists(subscription_dir):
        os.makedirs(subscription_dir)
    
    # Join server URLs with newlines
    subscription_content = '\n'.join(server_urls)
    
    # Base64 encode
    encoded_content = base64.b64encode(subscription_content.encode('utf-8')).decode('utf-8')
    
    # Write to file
    subscription_path = os.path.join(subscription_dir, f"{username}.txt")
    with open(subscription_path, 'w', encoding='utf-8') as f:
        f.write(encoded_content)
    
    try:
        print(f"✓ Created manual subscription: {subscription_path}")
    except UnicodeEncodeError:
        print(f"[OK] Created manual subscription: {subscription_path}")
    print(f"  Contains {len(server_urls)} server(s)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_manual_subscription.py <username> <server_url1> [server_url2] ...")
        print("\nExample:")
        print('  python create_manual_subscription.py manual_user "vless://..." "vless://..."')
        sys.exit(1)
    
    username = sys.argv[1]
    server_urls = sys.argv[2:]
    
    create_manual_subscription(username, server_urls)

