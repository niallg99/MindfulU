from .base import *

DEBUG = True
CURRENT_IP = "0.0.0.0:8000"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", CURRENT_IP, "0.0.0.0", "0.0.0.0:8080", "81.99.202.105", "mindful-u.co.uk", "192.168.0.106"]
INTERNAL_IPS = ALLOWED_HOSTS
