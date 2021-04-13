import asyncio
from SMTC import SMTC
from DiscordRP import DiscordRP

if __name__ == '__main__':
    DRP = DiscordRP()
    smtc = SMTC(DRP)
    current_media_info = asyncio.run(smtc.getMediaInfo())
    DRP.updatePresence(current_media_info)
    print(current_media_info)
    input()