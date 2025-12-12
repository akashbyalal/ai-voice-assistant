import requests
import socket

def internet_available(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def is_online():
    try:
        requests.get("https://www.google.com", timeout=1)
        return True
    except:
        return False
