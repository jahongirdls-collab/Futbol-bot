import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# SOZLAMALAR
# =========================

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)

BOT_ENABLED = True


# =========================
# JAVOBLAR
# =========================

def get_reply(message_text: str) -> str:
    text = " ".join(message_text.lower().split())

    # SALOMLASHISH
    greeting_words = (
        "salom",
        "assalomu alaykum",
        "assalom",
        "hello",
        "hi",
        "привет",
    )

    how_are_you_words = (
        "qalaysiz",
        "qalesiz",
        "qalay",
        "yaxshimisiz",
        "ishlar qalay",
    )

    if any(word in text for word in how_are_you_words):
        return (
            "Va alaykum assalom! 👋 Xush kelibsiz!\n"
            "Yaxshiman, rahmat 😊 Siz-chi?"
        )

    if any(word in text for word in greeting_words):
        return "Va alaykum assalom! 👋 Xush kelibsiz!"

    # ADMIN
    if "admin" in text:
        return "👤 Admin: @Jax0n12"

    # LOGO
    logo_words = (
        "logo",
        "logotip",
        "logo kerak",
        "logo yasash",
        "logo qildirish",
        "logo buyurtma",
    )

    if any(word in text for word in logo_words):
        return (
            "🎨 Logo yasatmoqchi bo‘lsangiz, bemalol yozing.\n"
            "📩 Referens yoki namuna yuborishingiz mumkin."
        )

    # NARX
    price_words = (
        "narxi",
        "qancha turadi",
        "necha pul",
        "narxlar",
        "цена",
        "сколько стоит",
    )

    if any(word in text for word in price_words):
        return (
            "💰 Narx dizayn turiga qarab belgilanadi.\n"
            "📩 Qanday dizayn kerakligini yozing yoki namuna yuboring."
        )

    # NAMUNA VA REFERENS
    reference_words = (
        "namuna",
        "referens",
        "rasm yuboraman",
        "namuna bor",
        "пример",
    )

    if any(word in text for word in reference_words):
        return (
            "📩 Albatta! Namuna yoki referens rasmini yuboring.\n"
            "🎨 Sizga kerakli dizaynni aniqlab olamiz."
        )

    # BUYURTMA
    order_words = (
        "buyurtma",
        "zakaz",
        "buyurtma bermoqchiman",
        "zakaz bermoqchiman",
        "qildirmoqchiman",
        "olmoqchiman",
    )

    if any(word in text for word in order_words):
        return (
            "✅ Buyurtma berish mumkin.\n"
            "📩 Kerakli dizayn yoki referensni yuboring."
        )

    # RAHMAT
    thanks_words = (
        "rahmat",
        "raxmat",
        "tashakkur",
        "katta rahmat",
    )

    if any(word in text for word in thanks_words):
        return (
            "Arzimaydi! 😊 Yana savollaringiz bo‘lsa, "
            "bemalol yozing."
        )

    # YORDAM
    casual_words = (
        "yordam",
        "yordam kerak",
        "yordam bering",
        "savolim bor",
        "savol bor",
        "murojaat",
        "gaplashmoqchi",
        "yozmoqchi",
        "qiziq",
    )

    if any(word in text for word in casual_words):
        return (
            "Albatta 😊 Yozavering, yordam berishga "
            "harakat qilamiz."
        )

    # BOSHQA XABARLAR
    return (
        "✅ Xabaringiz qabul qilindi.\n"
        "Tez orada javob beramiz."
    )


# =========================
# KOMANDALAR
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message:
        await update.message.reply_text(
            "👋 Assalomu alaykum!\n"
            "Xush kelibsiz."
        )


async def on(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    global BOT_ENABLED
    BOT_ENABLED = True

    if update.message:
        await update.message.reply_text("✅ Bot yoqildi.")


async def off(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    global BOT_ENABLED
    BOT_ENABLED = False

    if update.message:
        await update.message.reply_text("🔕 Bot o‘chirildi.")


async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.message:
        if BOT_ENABLED:
            await update.message.reply_text("🟢 Bot ishlayapti.")
        else:
            await update.message.reply_text("🔴 Bot o‘chirilgan.")


# =========================
# ODDIY BOT XABARLARI
# =========================

async def normal_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not BOT_ENABLED or not update.message:
        return

    message = update.message
    text = message.text

    if not text or text.startswith("/"):
        return

    reply = get_reply(text)
    await message.reply_text(reply)


# =========================
# TELEGRAM BUSINESS
# =========================

async def business_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not BOT_ENABLED:
        return

    message = update.business_message

    if not message or not message.text:
        return

    sender = message.from_user
    connection_id = message.business_connection_id

    if sender is None or sender.is_bot or not connection_id:
        return

    try:
        connection = await context.bot.get_business_connection(
            connection_id
        )
    except Exception:
        logging.warning(
            "Business connection tekshiruvi bajarilmadi."
        )
        return

    if connection is None or connection.user is None:
        logging.warning(
            "Business connection egasi aniqlanmadi."
        )
        return

    # Egasi o‘ziga yuborgan xabarlarga javob bermaslik
    if sender.id == connection.user.id:
        return

    reply = get_reply(message.text)

    await context.bot.send_message(
        chat_id=message.chat.id,
        text=reply,
        business_connection_id=connection_id,
    )


# =========================
# XATOLIKLARNI QAYD ETISH
# =========================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logging.error(
        "Xabarni qayta ishlashda xatolik yuz berdi.",
        exc_info=(
            type(context.error),
            context.error,
            context.error.__traceback__,
        ) if context.error else None,
    )


# =========================
# ISHGA TUSHIRISH
# =========================

def main():
    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN maxfiy o‘zgaruvchisi sozlanmagan."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("on", on))
    app.add_handler(CommandHandler("off", off))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(
        MessageHandler(
            filters.UpdateType.BUSINESS_MESSAGE,
            business_message,
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            normal_message,
        )
    )

    app.add_error_handler(error_handler)

    logging.info("Bot ishga tushmoqda...")

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
