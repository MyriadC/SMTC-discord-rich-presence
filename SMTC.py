import asyncio, time
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

class SMTC:

    def __init__(self, DRP):
        self.active = False
        self.DRP = DRP
        asyncio.run(self.loadSession())
        self.addEvents()

    async def loadSession(self):
        sessions = await MediaManager.request_async()
        self.current_session = sessions.get_current_session()

    def addEvents(self):
        self.current_session.add_media_properties_changed(self.mediaPropertiesChangedEvent)

    def mediaPropertiesChangedEvent(self, session, _):
        if not self.active:
            current_media_info = asyncio.run(self.getMediaInfo())
            if self.DRP is not None: 
                self.DRP.updatePresence(current_media_info)
            print(current_media_info)
        self.active = not self.active

    def getTimelineProperties(self):
        timelineInfo = self.current_session.get_timeline_properties()
        info_dict = self.attrToDict(timelineInfo)

        del info_dict['last_updated_time']
        for key in info_dict.keys():
            info_dict[key] = list(self.attrToDict(info_dict[key]).values())[0]
        return info_dict

    async def getMediaInfo(self):
        info = await self.current_session.try_get_media_properties_async()

        info_dict = self.attrToDict(info)

        info_dict['genres'] = list(info_dict['genres'])
        info_dict['app'] = self.current_session.source_app_user_model_id

        return info_dict

    def attrToDict(self, obj):
        return {attr: obj.__getattribute__(attr) for attr in dir(obj) if attr[0] != '_'}