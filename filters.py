# Advertisement detection filters
import re

# Reklama so'zlar (istalgan tilga qo'shishingiz mumkin)
ad_keywords = [
    "reklama", "obuna bo‘ling", "kanalga a'zo", "subscribe", "join now", 
    "earn money", "pul ishlang", "bonus", "refer", "sotiladi", "aktsiya",
    "promo", "reklama uchun", "reklama narxi"
]

# Havolalar, linklar
ad_links = [
    "t.me", "telegram.me", "joinchat", "bit.ly", "http://", "https://",
    "youtube.com", "instagram.com", "facebook.com", "tg://", "tiktok.com"
]

# Regex patternlar (unicode linklar, noaniq havolalar va emoji spam)
ad_patterns = [
    r"(https?:\/\/[^\s]+)",  # har qanday link
    r"(t\.me\/[^\s]+)",
    r"(joinchat\/[^\s]+)",
    r"(instagram\.com\/[^\s]+)",
    r"(facebook\.com\/[^\s]+)",
    r"(youtube\.com\/[^\s]+)",
    r"([\U0001F4F1-\U0001F9FF]){5,}",  # 5+ emoji spam
]

# Reklamani aniqlovchi funksiya
def is_advertisement(msg):
    text = msg.text or msg.caption or ""

    # 1. Matnda kalit so'zlar
    for word in ad_keywords:
        if word.lower() in text.lower():
            return True

    # 2. Matnda linklar
    for link in ad_links:
        if link.lower() in text.lower():
            return True

    # 3. Regex patternlar bo‘yicha tekshirish
    for pattern in ad_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    # 4. Rasm yoki fayl mavjud bo‘lsa ham
    if msg.document or msg.photo:
        return True

    return False
