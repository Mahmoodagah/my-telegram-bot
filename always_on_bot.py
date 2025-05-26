import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

# --- ۱. پیکربندی لاگینگ (Logging Configuration) ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# --- ۲. توابع Handler ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پاسخ به دستور /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"سلام {user.mention_html()}! من ربات تست شما هستم."
    )
    logger.info(f"کاربر {user.first_name} دستور /start را صادر کرد.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پاسخ به دستور /help."""
    await update.message.reply_text("من می‌توانم به شما کمک کنم! فقط کافیه پیام بفرستید یا /start را بزنید.")
    logger.info(f"کاربر {update.effective_user.first_name} دستور /help را صادر کرد.")


async def send_random_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """این تابع یک عدد تصادفی بین ۱ تا ۱۰۰ ارسال می‌کند."""
    random_num = random.randint(1, 100)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"عدد تصادفی: {random_num}")
    logger.info(f"ارسال عدد تصادفی به {update.effective_user.first_name}.")


async def echo_args_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پیام‌های ارسالی بعد از دستور /echo را اکو می‌کند."""
    if not context.args:
        await update.message.reply_text("لطفاً بعد از /echo چیزی بنویسید (مثلاً /echo سلام دنیا).")
        return
    text_to_echo = " ".join(context.args)
    await update.message.reply_text(f"شما گفتید: {text_to_echo}")
    logger.info(f"کاربر {update.effective_user.first_name} دستور /echo {text_to_echo} را صادر کرد.")


async def send_media_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """این تابع انواع مختلف رسانه (عکس، فایل، استیکر) را ارسال می‌کند."""
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id, "در حال ارسال یک عکس...")
    await context.bot.send_photo(
        chat_id,
        photo="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
        caption="این یک عکس از یک لوگوی گوگل است."
    )

    await context.bot.send_message(chat_id, "در حال ارسال یک فایل متنی...")
    try:
        # مطمئن شوید فایل 'my_document.txt' در کنار main.py وجود دارد.
        with open("my_document.txt", "rb") as f:
            await context.bot.send_document(
                chat_id,
                document=f,
                filename="My_Text_File.txt",
                caption="این یک فایل متنی است."
            )
    except FileNotFoundError:
        await context.bot.send_message(chat_id, "فایل 'my_document.txt' پیدا نشد. لطفاً آن را ایجاد کنید.")
        logger.error("فایل 'my_document.txt' پیدا نشد.")

    await context.bot.send_message(chat_id, "در حال ارسال یک استیکر...")
    # !!! این File_ID یک مثال است و ممکن است برای شما کار نکند!
    # لطفاً آن را با File_ID واقعی یک استیکر جایگزین کنید که خودتان پیدا می‌کنید.
    sticker_file_id = "CAACAgIAAxkBAAIMPWg0PomjDmBIibNfXe9alhtUgZXSAAIVAAPANk8TzVamO2GeZOc2BA"
    try:
        await context.bot.send_sticker(chat_id, sticker=sticker_file_id)
        await context.bot.send_message(chat_id, "این یک استیکر با استفاده از File_ID است.")
    except Exception as e:
        await context.bot.send_message(chat_id, "مشکلی در ارسال استیکر پیش آمد. شاید File_ID اشتباه است؟")
        logger.error(f"خطا در ارسال استیکر: {e}")

    logger.info(f"دستور /send_media اجرا شد برای {update.effective_user.first_name}.")


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش یک Reply Keyboard."""
    keyboard = [
        [KeyboardButton("گزینه ۱"), KeyboardButton("گزینه ۲")],
        [KeyboardButton("کمک"), KeyboardButton("درباره ما")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup)
    logger.info(f"نمایش منو به {update.effective_user.first_name}.")


async def handle_menu_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پاسخ به گزینه‌های انتخاب شده از Reply Keyboard."""
    text = update.message.text
    if text == "گزینه ۱":
        await update.message.reply_text("شما گزینه ۱ را انتخاب کردید.")
    elif text == "گزینه ۲":
        await update.message.reply_text("شما گزینه ۲ را انتخاب کردید.")
    elif text == "کمک":
        await update.message.reply_text("برای کمک، /help را تایپ کنید.")
    elif text == "درباره ما":
        await update.message.reply_text("این ربات برای آموزش شما ساخته شده است.")
    else:
        await update.message.reply_text("متوجه نشدم. لطفاً از دکمه‌های کیبورد استفاده کنید یا /menu را بزنید.")
    logger.info(f"کاربر {update.effective_user.first_name} گزینه منو: '{text}' را انتخاب کرد.")


async def inline_menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """نمایش یک Inline Keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("✅ دکمه اول", callback_data="inline_button_1"),
            InlineKeyboardButton("❌ دکمه دوم", callback_data="inline_button_2")
        ],
        [
            InlineKeyboardButton("🌐 به گوگل برو", url="https://www.google.com")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("لطفاً یک گزینه را از دکمه‌های زیر انتخاب کنید:", reply_markup=reply_markup)
    logger.info(f"نمایش Inline Menu به {update.effective_user.first_name}.")


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پاسخ به Callback Query (وقتی کاربر روی دکمه Inline کلیک می‌کند)."""
    query = update.callback_query
    await query.answer() # بسیار مهم: به تلگرام بگویید که کوئری را دریافت کرده‌اید.

    if query.data == "inline_button_1":
        await query.edit_message_text(text="شما دکمه ✅ اول را زدید!")
    elif query.data == "inline_button_2":
        await query.edit_message_text(text="شما دکمه ❌ دوم را زدید!")

    logger.info(f"کاربر {update.effective_user.first_name} دکمه Inline: '{query.data}' را زد.")


async def handle_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """پاسخ به هر پیام متنی که توسط Handlers دیگر پردازش نشده است."""
    if update.message and update.message.text:
        await update.message.reply_text("متوجه نشدم منظورتان چیست. می‌توانید /help را امتحان کنید.")
        logger.info(f"پیام نامشخص از {update.effective_user.first_name}: {update.message.text}")


# --- Handlers برای ConversationHandler ---

# تعریف حالت‌ها (States)
ASKING_NAME, ASKING_AGE = range(2)

async def start_info_collection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """شروع مکالمه برای جمع‌آوری اطلاعات."""
    await update.message.reply_text(
        "سلام! برای شروع، لطفاً نام خود را وارد کنید.",
        reply_markup=ReplyKeyboardRemove() # Reply Keyboard قبلی را حذف می‌کنیم
    )
    logger.info(f"مکالمه جمع‌آوری اطلاعات برای {update.effective_user.first_name} شروع شد. حالت: ASKING_NAME")
    return ASKING_NAME # به حالت ASKING_NAME می‌رویم

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """دریافت نام از کاربر و پرسیدن سن."""
    user_name = update.message.text
    context.user_data["name"] = user_name
    await update.message.reply_text(f"اسم شما {user_name} است. حالا لطفاً سنتان را وارد کنید.")
    logger.info(f"نام {user_name} دریافت شد. حالت: ASKING_AGE")
    return ASKING_AGE # به حالت ASKING_AGE می‌رویم

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """دریافت سن از کاربر و پایان مکالمه."""
    user_age = update.message.text
    
    try:
        age_int = int(user_age)
        if not (0 < age_int < 120):
            await update.message.reply_text("لطفاً یک سن معتبر بین ۱ تا ۱۲۰ وارد کنید.")
            return ASKING_AGE # در همین حالت می‌مانیم
    except ValueError:
        await update.message.reply_text("لطفاً یک عدد معتبر برای سن وارد کنید.")
        return ASKING_AGE # در همین حالت می‌مانیم

    context.user_data["age"] = user_age
    
    final_message = (
        f"متشکرم، {context.user_data['name']}!\n"
        f"اطلاعات شما: نام: {context.user_data['name']}, سن: {context.user_data['age']}."
    )
    await update.message.reply_text(final_message)
    
    logger.info(f"سن {user_age} دریافت شد. مکالمه برای {update.effective_user.first_name} پایان یافت.")
    context.user_data.clear() # داده‌های موقت را پاک می‌کنیم
    return ConversationHandler.END # مکالمه را به پایان می‌رسانیم

async def cancel_info_collection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """پایان مکالمه اگر کاربر آن را لغو کند."""
    await update.message.reply_text("مکالمه جمع‌آوری اطلاعات لغو شد.", reply_markup=ReplyKeyboardRemove())
    logger.info(f"مکالمه جمع‌آوری اطلاعات برای {update.effective_user.first_name} لغو شد.")
    context.user_data.clear()
    return ConversationHandler.END


# --- ۳. تابع اصلی (main) برای راه‌اندازی ربات ---
def main() -> None:
    """برنامه را راه‌اندازی و اجرا می‌کند."""

    TOKEN = "8087013899:AAFGOSy1T4Q3EzTs9xihVQPJqamBBCVIo6Q" # <--- توکن واقعی رباتتون رو اینجا جایگزین کنید!

    application = Application.builder().token(TOKEN).build()

    # --- ۳.۳. اضافه کردن Handlers ---
    # ترتیب اضافه کردن Handlers مهم است! Handlers خاص‌تر باید قبل از عمومی‌تر اضافه شوند.
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("random", send_random_number))
    application.add_handler(CommandHandler("echo", echo_args_command))
    application.add_handler(CommandHandler("send_media", send_media_command))
    application.add_handler(CommandHandler("menu", menu_command))

    # Handlers مربوط به کیبوردها
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(گزینه ۱|گزینه ۲|کمک|درباره ما)$"), handle_menu_option))
    application.add_handler(CommandHandler("inline_menu", inline_menu_command))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # --- ConversationHandler ---
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start_info", start_info_collection)],

        states={
            ASKING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ASKING_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
        },

        fallbacks=[CommandHandler("cancel", cancel_info_collection)],
        # conversation_timeout را می‌توانید اضافه کنید اگر می‌خواهید مکالمه پس از مدتی عدم فعالیت لغو شود.
        # conversation_timeout=600, # 600 ثانیه = 10 دقیقه
        # و همچنین یک timeout_handler اگر این پارامتر را فعال کنید.
        # timeout_handler=[MessageHandler(filters.ALL, timeout_conversation)],
    )
    application.add_handler(conv_handler)

    # Handler نهایی برای پیام‌های متنی نامشخص.
    # این باید آخرین MessageHandler مربوط به filters.TEXT باشد.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_message))


    # --- ۳.۴. شروع نظارت بر پیام‌ها (Polling) ---
    application.run_polling(allowed_updates=Update.ALL_TYPES)


# --- ۴. نقطه شروع برنامه ---
if __name__ == "__main__":
    main()