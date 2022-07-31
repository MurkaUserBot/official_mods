import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


class YourMod(loader.Module):
    """Description for module"""  # Translateable due to @loader.tds
    strings = {"name": "InlineMod"}

async def addbotcmd(self, message):
    await utils.answer(message, 'а нихера')
