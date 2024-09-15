import telebot
import os
import time
import requests
import json
from faker import Faker

# Initialize Faker for generating fake details
fake = Faker()

# Bot token
bot_token = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')  # replace with your token
bot = telebot.TeleBot(bot_token)

# In-memory storage for registered users
registered_users = set()

# Luhn Algorithm for Credit Card Validation
def luhn_check(card_number):
    num_digits = len(card_number)
    sum_digits = 0
    is_second = False
    for i in range(num_digits - 1, -1, -1):
        digit = int(card_number[i])
        if is_second:
            digit *= 2
            if digit > 9:
                digit -= 9
        sum_digits += digit
        is_second = not is_second
    return (sum_digits % 10 == 0)

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    text = (f"─ BITTU CHECKER PANEL ─\n"
            f"⁕ Registered as ➞ @{message.from_user.username}\n"
            f"⁕ Use ➞ /cmds to show available commands.\n"
            f"⁕ Owner ➞ @Jukerhenapadega")
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# Register Command
@bot.message_handler(commands=['register'])
def register(message):
    registered_users.add(message.from_user.id)
    bot.send_message(message.chat.id, "You have been registered as an owner and can now use all commands.")

# Commands List
@bot.message_handler(commands=['cmds'])
def cmds_command(message):
    text = ("─ BITTU CHECKER COMMANDS ─\n\n"
            "➣ Check Info [✅]\nUsage: /info\n\n"
            "➣ Check BIN Info [✅]\nUsage: /bin xxxxxx\n\n"
            "➣ Scrape CCS [✅]\nUsage: /scr username limit\n\n"
            "➣ Generate Fake Details [✅]\nUsage: /fake\n\n"
            "Contact → @Jukerhenapadega")
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# Bin Check Command
@bot.message_handler(commands=['bin'])
def bin_command(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Please provide a BIN number. Usage: /bin xxxxxx")
        return

    bin_number = args[1][:6]
    url = f"https://lookup.binlist.net/{bin_number}"
    headers = {
        "Host": "lookup.binlist.net",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        bank = data.get("bank", {}).get("name", "").upper()
        country_name = data.get("country", {}).get("name", "").upper()
        brand = data.get("brand", "").upper()
        emoji = data.get("country", {}).get("emoji", "")
        scheme = data.get("scheme", "").upper()
        card_type = data.get("type", "").upper()

        text = (f"⁕ ─ 𝗩𝗔𝗟𝗜𝗗 𝗕𝗜𝗡 ✅ ─ ⁕\n"
                f"BIN: {bin_number}\n"
                f"BANK: {bank}\n"
                f"𝙲𝙾𝚄𝙽𝚃𝚁𝚈: {country_name} ({emoji})\n"
                f"BRAND: {brand}\n"
                f"CARD: {scheme}\n"
                f"TYPE: {card_type}\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"CHECKED BY: @{message.from_user.username}")
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Info Command
@bot.message_handler(commands=['info'])
def info_command(message):
    text = (f"⁕ ─ 𝗜𝗡𝗙𝗢𝗥𝗠𝗔𝗧𝗜𝗢𝗡 ─ ⁕\n"
            f"Chat ID: {message.chat.id}\n"
            f"Name: {message.from_user.first_name}\n"
            f"Username: @{message.from_user.username}")
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# Generate Fake Details Command
@bot.message_handler(commands=['fake'])
def fake_command(message):
    fake_name = fake.name()
    fake_address = fake.address().replace("\n", ", ")
    fake_phone = fake.phone_number()
    fake_email = fake.email()

    text = (f"⁕ ─ 𝗙𝗔𝗞𝗘 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 ─ ⁕\n"
            f"Name: {fake_name}\n"
            f"Address: {fake_address}\n"
            f"Phone: {fake_phone}\n"
            f"Email: {fake_email}")
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# Website Analysis (with Fixes)
def check_captcha(url):
    response = requests.get(url).text
    return 'https://www.google.com/recaptcha/api' in response or 'captcha' in response

def check_credit_card_payment(url):
    response = requests.get(url)
    return any(payment_method in response.text for payment_method in ['stripe', 'Cybersource', 'paypal', 'authorize.net', 'Bluepay', 'Magento', 'woo', 'Shopify', 'adyan', 'Adyen', 'braintree', 'square', 'payflow'])

def check_cloud_in_website(url):
    response = requests.get(url)
    return 'cloud' in response.text.lower()

@bot.message_handler(func=lambda m: True)
def mess(message):
    url = message.text
    try:
        captcha = check_captcha(url)
        cloud = check_cloud_in_website(url)
        payment = check_credit_card_payment(url)
        result = (f"⁕ ─ 𝗪𝗲𝗯𝘀𝗶𝘁𝗲 𝗔𝗻𝗮𝗹𝘆𝘀𝗶𝘀 ─ ⁕\n"
                  f"Captcha: {captcha}\n"
                  f"Cloud Usage: {cloud}\n"
                  f"Payment Gateways Detected: {payment}\n"
                  f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                  f"CHECKED BY: @{message.from_user.username}")
        bot.send_message(message.chat.id, result, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Run the bot
if __name__ == '__main__':
    bot.infinity_polling()
