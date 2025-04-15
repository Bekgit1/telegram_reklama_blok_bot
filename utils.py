# Utility functions: warnings, mutes, stats
from collections import defaultdict

# Statistika uchun
stats = {
    "deleted": 0,
    "warned": 0,
    "banned": 0
}

# Har bir foydalanuvchi uchun ogohlantirishlar soni
warned_users = defaultdict(int)

# Statistika yangilash funksiyasi
def update_stats(key):
    if key in stats:
        stats[key] += 1

# Statistika olish
def get_stats():
    return stats

# Foydalanuvchini ogohlantirish (1 - warning, 2 - mute, 3+ - ban)
def warn_user(user_id):
    warned_users[user_id] += 1
    return warned_users[user_id]

# Foydalanuvchi ogohlantirish sonini olish
def get_warn_count(user_id):
    return warned_users[user_id]
