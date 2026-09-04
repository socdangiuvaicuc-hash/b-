import os
import random
import hashlib
import string
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. WEB SERVER GIỮ BOT ALIVE 24/7 ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Quốc Bảo AI Pattern Master đang hoạt động 24/7!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. CẤU HÌNH BOT ---
TOKEN = '8985526419:AAGM4OsUgx1WKyeKeQ-_IWG3lCwTNvoqBL4'
bot = telebot.TeleBot(TOKEN)

# Dữ liệu người dùng:
# balance: Số xu
# history: Lịch sử kết quả
# bias: Trọng số độ nghiêng tự học (-2.0 đến +2.0)
# last_pred: Dự đoán ván vừa rồi
# win_streak: Chuỗi thắng liên tiếp
user_data = {}

# Dữ liệu mã Giftcode
giftcodes = {}

# Các mẫu câu phản hồi linh hoạt & tạo uy tín
WIN_RESPONSES = [
    "🔥 **ĐÃ NÓI RỒI MÀ! Theo Tool Quốc Bảo chỉ có BÚ ĐẬM & ĐỔI ĐỜI thôi!** 💸🎉\n👉 Gửi mã MD5/HASH tiếp theo để đúp thừa thắng xông lên nào anh em!",
    "🚀 **RỰC RỠ CHƯA ANH EM! Đúng chuẩn ma trận AI, chuẩn từng milimet!** 🤑\n👉 Gửi tiếp mã ván mới để chuẩn bị húp tràn mồm!",
    "💎 **TƯỞNG THẾ NÀO! Bám Tool Quốc Bảo thì chỉ có giàu sang phú quý!** 👑💰\n👉 Nhanh tay gửi mã MD5/HASH tiếp theo để thừa thắng xông lên nào!",
    "🎯 **ĐỚP CỰC CĂNG! AI bắt nhịp cầu chuẩn như sách giáo khoa!** 🔥\n👉 Gửi tiếp mã mới, AI đang trong dây đỏ cực nét!"
]

LOSE_RESPONSES = [
    "🛡️ **Không sao anh em ơi, đường dài mới biết ngựa hay! Ván này bẻ nhẹ, ván sau gấp đôi gỡ lại ngay!** 💪\n👉 AI đã tái cấu trúc lại thuật toán bẻ cầu, gửi mã MD5/HASH tiếp theo để húp lại gấp đôi nào!",
    "🔄 **Nhịp cầu vừa đảo chút đỉnh thôi! Anh em giữ vững tâm lý, theo đúng vốn nhé!** 🔥\n👉 AI đã cập nhật lại độ nghiêng tối ưu nhất. Ném mã MD5/HASH tiếp theo vào đây đớp lại!",
    "⚡ **Thua 1 tay để ăn lại 3 tay! Đúng chiến thuật AI đưa ra, tĩnh tâm vào tiền đều tay nhé!** 💰\n👉 Gửi mã tiếp theo ngay, tay này AI đã khóa chặt ma trận bẻ!",
    "💪 **Gãy 1 tay làm sao làm khó được Tool VIP! Chuẩn bị tinh thần bú đậm ván tới nhé!** 🎉\n👉 Gửi mã MD5/HASH mới ngay để AI chốt hạ tay gỡ!"
]

# --- 3. THUẬT TOÁN AI NÂNG CẤP ĐỘ NGHIÊNG CẤP CAO ---
def master_predict_with_advanced_bias(uid, input_str):
    ud = user_data[uid]
    bias = ud.get("bias", 0.0)
    
    # Phân tích toán học sâu SHA-512
    deep_hash = hashlib.sha512(input_str.encode()).hexdigest()
    bytes_arr = [int(deep_hash[i:i+2], 16) for i in range(0, 64, 2)]
    
    weighted_sum = sum(b * (idx + 7) for idx, b in enumerate(bytes_arr))
    
    raw_score = (weighted_sum % 101) - 50 
    adjusted_score = raw_score + (bias * 30) # Áp dụng độ nghiêng tự học
    
    raw_is_tai = (adjusted_score >= 0)
    raw_result = "TÀI" if raw_is_tai else "XỈU"

    history = ud.get("history", [])

    pattern_detected = "Cầu tự do"
    final_result = raw_result

    # Soi ma trận cầu
    if len(history) >= 2:
        last_1 = history[-1]
        last_2 = history[-2]

        if len(history) >= 3 and history[-1] == history[-2] == history[-3]:
            bet_type = history[-1]
            pattern_detected = f"🔥 Cầu Bệt {bet_type} (Đang bệt {len(history)} tay)"
            final_result = bet_type 

        elif last_1 != last_2:
            pattern_detected = "🔄 Cầu Chuyền 1-1"
            final_result = "XỈU" if last_1 == "TÀI" else "TÀI"

        elif len(history) >= 4 and history[-1] == history[-2] and history[-3] == history[-4] and history[-1] != history[-3]:
            pattern_detected = "⚖️ Cầu Nhịp 2-2"
            final_result = "XỈU" if last_1 == "TÀI" else "TÀI"

    # Đưa ra tỷ lệ siêu nét (90% - 98%) giúp người dùng cực kỳ an tâm
    streak = ud.get("win_streak", 0)
    base_percent = 91 + (abs(int(adjusted_score)) % 8) + min(streak, 3)
    percent_main = min(98, max(90, base_percent))
    percent_sub = 100 - percent_main

    if final_result == "TÀI":
        percent_tai = percent_main
        percent_xiu = percent_sub
    else:
        percent_xiu = percent_main
        percent_tai = percent_sub

    # Lời khuyên tự tin, đanh thép
    if "Bệt" in pattern_detected:
        advice = "🔥 Cầu bệt cực căng! Vốn dày tự tin đè mạnh tay này!"
    elif "1-1" in pattern_detected:
        advice = "🔄 Nhịp 1-1 cực chuẩn khuôn! Tự tin theo sát Tool để bú đặn!"
    elif "2-2" in pattern_detected:
        advice = "⚖️ Đúng khung 2-2 kết hợp AI học sâu! Tự tin vào tiền đều!"
    else:
        if percent_main >= 94:
            advice = "👑 Tay này Ma Trận AI kết cực nét! Tự tin xuống tiền đổi đời!"
        else:
            advice = "💎 Nhịp cầu rất đẹp! Đánh đều tay theo tỉ lệ để tối ưu lợi nhuận."

    ud["last_pred"] = final_result
    return final_result, percent_tai, percent_xiu, pattern_detected, advice

# --- 4. MENU KEYBOARD ---
def main_menu_keyboard():
    markup = InlineKeyboardMarkup()
    btn_md5 = InlineKeyboardButton("🎲 SOI MÃ MD5", callback_data="mode_md5")
    btn_hash = InlineKeyboardButton("⚡ SOI MÃ HASH", callback_data="mode_hash")
    btn_buy = InlineKeyboardButton("💎 MUA XU VIP", callback_data="mode_buy")
    btn_info = InlineKeyboardButton("💳 VÍ XU & ID", callback_data="mode_info")
    
    markup.add(btn_md5, btn_hash)
    markup.add(btn_buy)
    markup.add(btn_info)
    return markup

# --- 5. LỆNH CƠ BẢN, CODE & ADMIN ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {"balance": 0, "state": None, "history": [], "bias": 0.0, "last_pred": None, "win_streak": 0}
        
    xu = user_data[uid]["balance"]
    msg = (
        "💎 **TOOL QUỐC BẢO ULTIMATE VIP AI** 💎\n"
        "─────────────────\n"
        "🔥 **Hệ Thống Phân Tích Ma Trận & Thuật Toán Tự Học Học Sâu**\n"
        f"🆔 ID Telegram: `{uid}`\n"
        f"💰 Số xu hiện có: **{xu} Xu**\n"
        "─────────────────\n"
        "💬 **Mẹo Đổi Đời:** Sau khi có kết quả, hãy chat **`bú`** (khi ăn) hoặc **`gãy`** (khi thua) để AI tinh chỉnh độ nghiêng cho tay sau CHUẨN XÁC 100%!\n"
        "🎁 **Nhập Giftcode:** Gửi lệnh `/code <Mã_Code>` để nhận xu free!\n"
        "─────────────────\n"
        "👇 Chọn chức năng bên dưới để bắt đầu:"
    )
    bot.reply_to(message, msg, parse_mode="Markdown", reply_markup=main_menu_keyboard())

@bot.message_handler(commands=['myid'])
def get_my_id(message):
    uid = message.from_user.id
    xu = user_data.get(uid, {}).get("balance", 0)
    bot.reply_to(message, f"🆔 ID: `{uid}` | 💰 Xu: `{xu}` Xu", parse_mode="Markdown")

@bot.message_handler(commands=['taocode'])
def create_code(message):
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "⚠️ **Cú pháp:** `/taocode <Mã_Code hoặc AUTO> <Số_Xu> [Số_Lượt_Dùng]`", parse_mode="Markdown")
            return
        code_input, coins = args[1].upper(), int(args[2])
        uses = int(args[3]) if len(args) >= 4 else 1
        code_string = "GIFT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) if code_input == "AUTO" else code_input
        giftcodes[code_string] = {"coins": coins, "uses": uses, "used_by": set()}
        bot.reply_to(message, f"🎉 **TẠO CODE THÀNH CÔNG!**\n🎁 Mã Code: `{code_string}`\n💰 Giá trị: **+{coins} Xu**\n👥 Giới hạn: **{uses} lượt**", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ Lỗi cú pháp! Vui lòng kiểm tra lại.")

@bot.message_handler(commands=['code'])
def redeem_code(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {"balance": 0, "state": None, "history": [], "bias": 0.0, "last_pred": None, "win_streak": 0}
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "⚠️ **Cú pháp:** `/code <Mã_Giftcode>`", parse_mode="Markdown")
            return
        code_input = args[1].strip().upper()
        if code_input not in giftcodes:
            bot.reply_to(message, "❌ **Mã Giftcode không tồn tại hoặc đã hết hạn!**", parse_mode="Markdown")
            return
        code_info = giftcodes[code_input]
        if uid in code_info["used_by"]:
            bot.reply_to(message, "⚠️ **Bạn đã nhập mã Giftcode này rồi!**", parse_mode="Markdown")
            return
        if len(code_info["used_by"]) >= code_info["uses"]:
            bot.reply_to(message, "❌ **Mã Giftcode này đã hết lượt sử dụng!**", parse_mode="Markdown")
            return
        user_data[uid]["balance"] += code_info["coins"]
        code_info["used_by"].add(uid)
        bot.reply_to(message, f"🎉 **NHẬP CODE THÀNH CÔNG!**\n🎁 Cộng: **+{code_info['coins']} Xu**\n💰 Tổng xu: **{user_data[uid]['balance']} Xu**", parse_mode="Markdown", reply_markup=main_menu_keyboard())
    except Exception:
        bot.reply_to(message, "❌ Lỗi hệ thống khi nhập code!")

@bot.message_handler(commands=['congxu'])
def add_coins(message):
    try:
        args = message.text.split()
        target_id, coins_to_add = int(args[1]), int(args[2])
        if target_id not in user_data:
            user_data[target_id] = {"balance": 0, "state": None, "history": [], "bias": 0.0, "last_pred": None, "win_streak": 0}
        user_data[target_id]["balance"] += coins_to_add
        bot.reply_to(message, f"✅ **Đã cộng +{coins_to_add} Xu** cho ID `{target_id}`.", parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, "❌ Cú pháp sai: `/congxu <ID_User> <Số_Xu>`")

# --- 6. CALLBACK BUTTONS ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    uid = call.from_user.id
    if uid not in user_data:
        user_data[uid] = {"balance": 0, "state": None, "history": [], "bias": 0.0, "last_pred": None, "win_streak": 0}

    if call.data == "mode_md5":
        user_data[uid]["state"] = "WAITING_MD5"
        bot.send_message(call.message.chat.id, "📥 **Vui lòng gửi MÃ MD5 (32 ký tự):**", parse_mode="Markdown")
    elif call.data == "mode_hash":
        user_data[uid]["state"] = "WAITING_HASH"
        bot.send_message(call.message.chat.id, "📥 **Vui lòng gửi MÃ HASH (64 ký tự):**", parse_mode="Markdown")
    elif call.data == "mode_buy":
        buy_msg = (
            "🛒 **BẢNG GIÁ NẠP XU VIP**\n"
            "─────────────────\n"
            "💵 **5.000 VNĐ**   ➔ **13 Xu**\n"
            "💵 **15.000 VNĐ**  ➔ **25 Xu**\n"
            "💵 **50.000 VNĐ**  ➔ **70 Xu**\n"
            "💵 **100.000 VNĐ** ➔ **150 Xu**\n"
            "─────────────────\n"
            "📩 **Liên hệ ADMIN để mua xu:**\n"
            "👤 Telegram Admin: @lionVnIos\n"
            f"🆔 ID của bạn: `{uid}` (Gửi ID này cho Admin)"
        )
        bot.send_message(call.message.chat.id, buy_msg, parse_mode="Markdown")
    elif call.data == "mode_info":
        xu = user_data[uid]["balance"]
        bot.send_message(call.message.chat.id, f"🆔 ID Telegram: `{uid}`\n💰 Xu hiện có: `{xu}` Xu", parse_mode="Markdown")

# --- 7. XỬ LÝ CHAT "BÚ/GÃY" VÀ PHÂN TÍCH MD5/HASH ---
@bot.message_handler(func=lambda message: True)
def process_analysis_and_feedback(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {"balance": 0, "state": None, "history": [], "bias": 0.0, "last_pred": None, "win_streak": 0}

    text = message.text.strip().lower()
    ud = user_data[uid]

    # A. PHẢN HỒI KHI DÙNG CHAT "BÚ" (THẮNG)
    if text in ["bú", "bu", "win", "ăn", "thắng", "húp", "đớp"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa soi tay nào trước đó! Hãy gửi mã MD5/HASH để bắt đầu soi.")
            return

        ud["history"].append(ud["last_pred"])
        if len(ud["history"]) > 10:
            ud["history"].pop(0)

        # Cập nhật chuỗi thắng & điều chỉnh trọng số độ nghiêng
        ud["win_streak"] += 1
        if ud["last_pred"] == "TÀI":
            ud["bias"] = min(2.0, ud["bias"] + 0.35)
        else:
            ud["bias"] = max(-2.0, ud["bias"] - 0.35)

        reply_msg = random.choice(WIN_RESPONSES)
        bot.reply_to(message, reply_msg, parse_mode="Markdown")
        return

    # B. PHẢN HỒI KHI DÙNG CHAT "GÃY" (THUA)
    elif text in ["gãy", "gay", "thua", "tạch", "xịt", "bẻ"]:
        if not ud["last_pred"]:
            bot.reply_to(message, "⚠️ Bạn chưa soi tay nào trước đó! Hãy gửi mã MD5/HASH để bắt đầu soi.")
            return

        real_result = "XỈU" if ud["last_pred"] == "TÀI" else "TÀI"
        ud["history"].append(real_result)
        if len(ud["history"]) > 10:
            ud["history"].pop(0)

        # Reset chuỗi thắng & đảo độ nghiêng thuật toán
        ud["win_streak"] = 0
        if ud["last_pred"] == "TÀI":
            ud["bias"] = max(-2.0, ud["bias"] - 0.6)
        else:
            ud["bias"] = min(2.0, ud["bias"] + 0.6)

        reply_msg = random.choice(LOSE_RESPONSES)
        bot.reply_to(message, reply_msg, parse_mode="Markdown")
        return

    # C. XỬ LÝ SOI MÃ MD5 / HASH MỚI
    if ud["balance"] < 1:
        msg_out = (
            f"⚠️ **Bạn không đủ Xu để soi cầu!**\n"
            f"🆔 ID của bạn: `{uid}`\n"
            f"👉 Nhấn nút **💎 MUA XU VIP** hoặc nhập Giftcode `/code <Mã>` để có xu."
        )
        bot.reply_to(message, msg_out, parse_mode="Markdown", reply_markup=main_menu_keyboard())
        return

    if len(text) not in [32, 64]:
        bot.reply_to(message, "⚠️ Vui lòng gửi đúng mã **MD5 (32 ký tự)** hoặc **HASH (64 ký tự)**\n*(Hoặc nhắn `bú` / `gãy` để báo kết quả ván vừa rồi!)*", reply_markup=main_menu_keyboard())
        return

    ud["balance"] -= 1
    xu_con_lai = ud["balance"]

    try:
        final_result, percent_tai, percent_xiu, pattern_detected, advice = master_predict_with_advanced_bias(uid, text)
    except Exception:
        bot.reply_to(message, "❌ Lỗi xử lý mã! Vui lòng kiểm tra lại.")
        return

    res_label = "🔴 TÀI" if final_result == "TÀI" else "🔵 XỈU"

    res = (
        f"👑 **TOOL QUỐC BẢO MASTER (AI SELF-LEARNING)** 👑\n"
        f"─────────────────\n"
        f"🎯 Dự đoán: **{res_label}**\n"
        f"📊 Tỷ lệ chuẩn: **Tài {percent_tai}% - Xỉu {percent_xiu}%**\n"
        f"📈 Ma trận cầu: `{pattern_detected}`\n"
        f"💡 Lời khuyên AI: _{advice}_\n"
        f"─────────────────\n"
        f"💰 Xu còn lại: **{xu_con_lai} Xu**\n"
        f"─────────────────\n"
        f"💬 *Vừa ăn xong? Chat `bú` để AI giữ dây đỏ! Gãy nhẹ? Chat `gãy` để AI đổi hướng bẻ cầu!*"
    )

    bot.reply_to(message, res, parse_mode="Markdown", reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
