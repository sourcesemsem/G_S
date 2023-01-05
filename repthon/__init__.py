# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import sys

from .version import __version__

run_as_module = False

class ULTConfig:
    lang = "ar"

if sys.argv[0] == "-m":
    run_as_module = True

    import time

    from .Config import Var
    from utils import *
    from utils import sbb_b
    from utils.startup import jmthonclient
    from .core.session import sbb_b, tgbot
    from utils .pluginmanager import sbb_b
    from .version import repthon_version

    if not os.path.exists("plugins"):
        LOGS.error(
            "'plugins' folder not found!\nMake sure that, you are on correct path."
        )
        exit()

    start_time = time.time()
    _ult_cache = {}
    _ignore_eval = []

    udB = UltroidDB()
    update_envs()

    LOGS.info(f"Connecting to {udB.name}...")
    if udB.ping():
        LOGS.info(f"Connected to {udB.name} Successfully!")

    BOT_MODE = udB.get_key("BOTMODE")
    DUAL_MODE = udB.get_key("DUAL_MODE")

    if BOT_MODE:
        if DUAL_MODE:
            udB.del_key("DUAL_MODE")
            DUAL_MODE = False
        ultroid_bot = None

        if not udB.get_key("TG_BOT_TOKEN"):
            LOGS.critical(
                '"TG_BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"'
            )

            sys.exit()
    else:
        repthon_bot = JmthonClient(
            validate_session(Var.SESSION, LOGS),
            udB=udB,
            app_version=3.0.7,
            device_model="Repthon",
        )
        repthon_bot.run_in_loop(autobot())

    asst = JmthonClient(None, bot_token=udB.get_key("TG_BOT_TOKEN"), udB=udB)

    if BOT_MODE:
        ultroid_bot = asst
        if udB.get_key("OWNER_ID"):
            try:
                repthon_bot.me = repthon_bot.run_in_loop(
                    repthon_bot.get_entity(udB.get_key("OWNER_ID"))
                )
            except Exception as er:
                LOGS.exception(er)
    elif not asst.me.bot_inline_placeholder:
        repthon_bot.run_in_loop(enable_inline(repthon_bot, asst.me.username))

    vcClient = vc_connection(udB, repthon_bot)

    _version_changes(udB)

    HNDLR = udB.get_key("HNDLR") or "."
    DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
    SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR
else:
    print("Repthon 2022 © TeamRepthon")

    from logging import getLogger

    LOGS = getLogger("𝐑𝐄𝐏𝐓𝐇𝐎𝐍")

    repthon_bot = asst = udB = vcClient = None
