import telebot
import os
import time
import requests
import json

# Bot token
bot_token = os.getenv('BOT_TOKEN', '7546565731:AAGbMnNVriBrHyAog4nYj32Pr1TJIt_681g')
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
            digit = digit * 2
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
    # Register user as owner
    registered_users.add(message.from_user.id)
    bot.send_message(message.chat.id, "You have been registered as an owner and can now use all commands.")

# Commands List
@bot.message_handler(commands=['cmds'])
def cmds_command(message):
    text = ("─ BITTU CHECKER COMMANDS ─\n\n"
            "➣ Check Info [✅]\nUsage: /info\n\n"
            "➣ Check BIN Info [✅]\nUsage: /bin xxxxxx\n\n"
            "➣ Scrape CCS [✅]\nUsage: /scr username limit\n\n"
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
        name = data.get("country", {}).get("name", "").upper()
        brand = data.get("brand", "").upper()
        emoji = data.get("country", {}).get("emoji", "")
        scheme = data.get("scheme", "").upper()
        type = data.get("type", "").upper()

        text = (f"⁕ ─ 𝗩𝗔𝗟𝗜𝗗 𝗕𝗜𝗡 ✅ ─ ⁕\n"
                f"BIN: {bin_number}\n"
                f"BANK: {bank}\n"
                f"𝙲𝙾𝚄𝙽𝚃𝚁𝚈: {name} ({emoji})\n"
                f"BRAND: {brand}\n"
                f"CARD: {scheme}\n"
                f"TYPE: {type}\n"
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

# ID Command
@bot.message_handler(commands=['id'])
def id_command(message):
    text = f"<b>Chat ID:</b> <code>{message.chat.id}</code>"
    bot.send_message(message.chat.id, text, parse_mode="HTML")

# Scraping Command
@bot.message_handler(commands=['scr'])
def scrape_ccs(message):
    if message.from_user.id not in registered_users:
        bot.reply_to(message, "You need to register as an owner to use this command. Use /register to register.")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Please provide both username and limit. Usage: /scr username limit")
        return

    username = args[1]
    limit = args[2]
    start_time = time.time()
    msg = bot.send_message(message.chat.id, 'Scraping...')
    try:
        response = requests.get(f'https://scrd-3c14ab273e76.herokuapp.com/scr', params={'username': username, 'limit': limit}, timeout=120)
        raw = response.json()
        if 'error' in raw:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"Error: {raw['error']}")
        else:
            cards = raw.get('cards', '')
            found = str(raw.get('found', '0'))
            file = f'Scraped_by_@Jukerhenapadega.txt'
            
            if cards:
                with open(file, "w") as f:
                    f.write(cards)
                with open(file, "rb") as f:
                    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
                    end_time = time.time()
                    time_taken = end_time - start_time
                    cap = (f'<b>Scraped Successfully ✅\n'
                           f'Target -» <code>{username}</code>\n'
                           f'Found -» <code>{found}</code>\n'
                           f'Time Taken -» <code>{time_taken:.2f} seconds</code>\n'
                           f'REQ BY -» <code>{message.from_user.first_name}</code></b>')
                    bot.send_document(chat_id=message.chat.id, document=f, caption=cap, parse_mode='HTML')
                try:
                    os.remove(file)
                except PermissionError as e:
                    bot.send_message(message.chat.id, f"Error deleting file: {e}")
            else:
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="No cards found.")
    except requests.exceptions.RequestException as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"Request error: {e}")
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"An error occurred: {e}")

# Website Analysis Commands
def check_captcha(url):
    response = requests.get(url).text
    return 'https://www.google.com/recaptcha/api' in response or 'captcha' in response

def check_credit_card_payment(url):
    response = requests.get(url)
    return any(payment_method in response.text for payment_method in ['stripe', 'Cybersource', 'paypal', 'authorize.net', 'Bluepay', 'Magento', 'woo', 'Shopify', 'adyan', 'Adyen', 'braintree', 'suqare', 'payflow'])

def check_cloud_in_website(url):
    response = requests.get(url)
    return 'cloud' in response.text.lower()

@bot.message_handler(func=lambda m: True)
def mess(message):
    url = message.text
    try:
        captcha = check_captcha(url)
    except:
        captcha = 'False'
    cloud = check_cloud_in_website(url)
    payment = check_credit_card_payment(url)
    msg = bot.reply_to(message, '<strong>[~]-Loading.... 🥸</strong>', parse_mode="HTML")
    time.sleep(1)
    results = [
    f"[~]- Captcha = {captcha}",
    f"[~]- Captcha = {captcha}\n\n[~]- Cloud = {cloud}",
    f"[~]- Captcha = {captcha}\n\n[~]- Cloud = {cloud}\n\n[~]- Payment = {payment}",
    f"[~]- Captcha = {captcha}\n\n[~]- Cloud = {cloud}\n\n[~]- Payment = {payment}\n\n[~]- Bot By = <a href='tg://openmessage?user_id=1316255100'>Jukerhenapadega</a>"
    ]
