import requests

def is_online():
    try:
        requests.get("https://www.google.com", timeout=1)
        return True
    except:
        return False
