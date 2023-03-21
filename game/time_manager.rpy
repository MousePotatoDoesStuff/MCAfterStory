init -15 python:
    import datetime


    class TimeManager:
        def getTime(self):
            raise NotImplementedError


    class RealTime(TimeManager):
        def __init__(self):
            return

        def getTime(self):
            return datetime.datetime.now()


    class OffsetRealTime(TimeManager):
        def __init__(self, startPoint=datetime.datetime.now(), timeAtStart=datetime.datetime.now(), speed=1):
            self.startPoint = startPoint
            self.timeAtStart = timeAtStart
            self.speed = speed
            return

        def getTime(self):
            curtime = datetime.datetime.now()
            timeSinceStart = curtime - self.timeAtStart
            if self.speed != 1.0:
                adjustedTimeSinceStart = timeSinceStart * self.speed
            else:
                adjustedTimeSinceStart = timeSinceStart
            resTime = self.startPoint + adjustedTimeSinceStart
            return resTime