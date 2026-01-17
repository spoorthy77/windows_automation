"""
Network Detection Module for Windows Automation Chatbot

This module automatically detects internet connectivity and enables
the chatbot to switch between online (Grok API) and offline (local NLP) modes.
"""

import socket
import requests
from typing import Tuple
import time


class NetworkDetector:
    """
    Detects and monitors internet connectivity for hybrid mode switching.
    """
    
    def __init__(self):
        self.last_check_time = 0
        self.cache_duration = 5  # Cache result for 5 seconds
        self.cached_status = None
    
    def is_online(self, use_cache: bool = True) -> bool:
        """
        Check if internet connection is available.
        
        Args:
            use_cache: If True, return cached result if within cache duration
            
        Returns:
            bool: True if online, False if offline
        """
        current_time = time.time()
        
        # Return cached result if still valid
        if use_cache and self.cached_status is not None:
            if current_time - self.last_check_time < self.cache_duration:
                return self.cached_status
        
        # Perform actual connectivity check
        online = self._check_connectivity()
        
        # Update cache
        self.cached_status = online
        self.last_check_time = current_time
        
        return online
    
    def _check_connectivity(self) -> bool:
        """
        Perform actual connectivity check using multiple methods.
        
        Returns:
            bool: True if online, False if offline
        """
        # Method 1: Try DNS resolution (fast)
        try:
            socket.setdefaulttimeout(2)
            socket.gethostbyname("www.google.com")
            return True
        except (socket.gaierror, socket.timeout):
            pass
        
        # Method 2: Try HTTP request to reliable endpoints
        try:
            response = requests.get(
                "https://www.google.com",
                timeout=3
            )
            if response.status_code == 200:
                return True
        except (requests.RequestException, requests.Timeout):
            pass
        
        # Method 3: Try alternative endpoint
        try:
            response = requests.get(
                "https://1.1.1.1",  # Cloudflare DNS
                timeout=3
            )
            if response.status_code in [200, 301, 302]:
                return True
        except (requests.RequestException, requests.Timeout):
            pass
        
        # All methods failed - we're offline
        return False
    
    def get_status_with_details(self) -> Tuple[bool, str]:
        """
        Get connectivity status with descriptive message.
        
        Returns:
            Tuple[bool, str]: (is_online, status_message)
        """
        is_online = self.is_online()
        
        if is_online:
            message = "🟢 Online Mode: Using Grok AI for intelligent responses"
        else:
            message = "🔴 Offline Mode: Using local NLP for command parsing"
        
        return is_online, message
    
    def force_check(self) -> bool:
        """
        Force a fresh connectivity check, bypassing cache.
        
        Returns:
            bool: True if online, False if offline
        """
        return self.is_online(use_cache=False)


# Global network detector instance
network_detector = NetworkDetector()


def check_internet() -> bool:
    """
    Quick function to check internet connectivity.
    
    Returns:
        bool: True if online, False if offline
    """
    return network_detector.is_online()


def get_connection_status() -> Tuple[bool, str]:
    """
    Get connection status with detailed message.
    
    Returns:
        Tuple[bool, str]: (is_online, status_message)
    """
    return network_detector.get_status_with_details()


if __name__ == "__main__":
    # Test the network detector
    print("🔍 Testing Network Detector...")
    print("=" * 50)
    
    is_online, message = get_connection_status()
    print(message)
    
    if is_online:
        print("✅ Internet connection detected!")
        print("📡 Chatbot will use Grok API for online mode")
    else:
        print("⚠️  No internet connection detected!")
        print("💾 Chatbot will use offline NLP mode")
    
    print("=" * 50)
