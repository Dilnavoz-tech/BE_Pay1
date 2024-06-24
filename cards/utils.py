from random import randint
import requests

BOT_TOKEN = "7184502336:AAH2ULKNMJqcZfd_a8qnLGKEFzckV-FPxiQ"
CHAT_ID = "1806940376"
TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}"

def send_otp_telegram(otp):
    message = f"""Project: BePay\nphone_number {otp.phone_number}\ncode:{otp.otp_code}\notp_key": {otp.otp_key}"""
    requests.get(TELEGRAM_API_URL.format(BOT_TOKEN, message, CHAT_ID))

def generate_otp_code():
    return randint(10000, 99999)