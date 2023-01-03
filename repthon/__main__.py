import sys

from aiohttp import web

from repthon import BOTLOG_CHATID, PM_LOGGER_GROUP_ID, tbot

from .Config import Config
from .core.logger import logging
from .core.server import web_server
from .core.session import sbb_b
from .utils import (
    add_bot_to_logger_group,
    load_plugins,
    mybot,
    saves,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("𝐑𝐄𝐏𝐓𝐇𝐎𝐍")

cmdhr = Config.COMMAND_HAND_LER


async def jmthons(session=None, client=None, session_name="Main"):
    if session:
        LOGS.info(f"••• جار بدأ الجلسة [{session_name}] •••")
        try:
            await client.start()
            return 1
        except:
            LOGS.error(f"خطأ في الجلسة {session_name}!! تأكد وحاول مجددا !")
            return 0
    else:
        return 0


# تأكد من تنصيب بعض الاكواد
async def jmthonstart(total):
    await setup_bot()
    await mybot()
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    await saves()


async def start_jmthon():
    try:
        tbot_id = await tbot.get_me()
        Config.TG_BOT_USERNAME = f"@{tbot_id.username}"
        sbb_b.tgbot = tbot
        LOGS.info("•••  جار بدا سورس ريبثون •••")
        CLIENTR = await jmthons(Config.STRING_SESSION, sbb_b, "STRING_SESSION")
        await tbot.start()
        total = CLIENTR
        await load_plugins("plugins")
        await load_plugins("assistant")
        LOGS.info(f"تم انتهاء عملية التنصيب بنجاح على موجنيس")
        LOGS.info(
            f"لمعرفة اوامر السورس ارسل {cmdhr}الاوامر\
        \nمجموعة قناة السورس  https://t.me/Repthon_support"
        )
        LOGS.info(f"» عدد جلسات التنصيب الحالية = {str(total)} «")
        await jmthonstart(total)
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


sbb_b.loop.run_until_complete(start_jmthon())

if len(sys.argv) not in (1, 3, 4):
    sbb_b.disconnect()
else:
    try:
        sbb_b.run_until_disconnected()
    except ConnectionError:
        pass
