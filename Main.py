
def get_reply(message_text: str) -> str:
    text = " ".join(message_text.lower().split())
    text = text.strip("!?.,:; ")

    # HOL-AHVAL
    if any(x in text for x in (
        "qalaysiz", "qalesiz", "qalay", "yaxshimisiz",
        "ishlar qalay", "ahvolingiz"
    )):
        return "Yaxshiman, rahmat 😊 Siz-chi?"

    # SALOMLASHISH
    if any(x in text for x in (
        "salom", "assalomu alaykum", "assalom",
        "hello", "hi", "привет"
    )):
        return "Va alaykum assalom! 👋 Xush kelibsiz!"

    # KAYFIYAT
    if any(x in text for x in (
        "nima gap", "nima yangilik", "yangiliklar"
    )):
        return "Hammasi joyida 😊 Sizda qanday yangiliklar?"

    if any(x in text for x in (
        "nima qilyapsiz", "nima bilan bandsiz"
    )):
        return "Hozir siz bilan suhbatlashyapman 😁"

    if any(x in text for x in (
        "yaxshi", "zo'r", "zor", "a'lo"
    )):
        return "Zo'r-ku! 😊 Kayfiyatingiz doim shunday bo'lsin!"

    # RAHMAT
    if any(x in text for x in (
        "rahmat sizga", "katta rahmat"
    )):
        return "Doim xizmatingizga tayyorman! 🤝"

    if any(x in text for x in (
        "rahmat", "raxmat", "tashakkur"
    )):
        return "Arzimaydi! 😊 Yana bemalol yozing."

    # XAYRLASHISH
    if any(x in text for x in (
        "xayr", "ko'rishguncha", "hayr"
    )):
        return "Xayr! Yana kutib qolamiz 👋"

    # SAVOLLAR
    if any(x in text for x in (
        "kimsiz", "kim siz", "bu kim"
    )):
        return "Men avtomatik yordamchiman 🤖 Sizga qanday yordam beray?"

    if any(x in text for x in (
        "yordam", "savolim bor", "yordam kerak"
    )):
        return "Albatta! 😊 Savolingizni yozavering."

    if any(x in text for x in (
        "zerikdim", "zerikayapman"
    )):
        return "Unda suhbatlashamizmi? 😁"

    if any(x in text for x in (
        "tinchlikmi", "tinchmisiz"
    )):
        return "Ha, hammasi tinch 😊 Sizda-chi?"

    # BOSHQA XABARLAR
    return "Xabaringizni oldim 😊 Yana nima haqida suhbatlashamiz?"

