
class Time_Group():
    times = []
    @classmethod
    def append(cls,mytime):
        cls.times.append(mytime)
    @classmethod
    def tick(cls):
        for each in cls.times:
            each.tick()
    @classmethod
    def remove(cls,mytime):
        cls.times.remove(mytime)

class MYTIME():
    def __init__(self,T=0, initTime=0, StartAtOnce=False):
        self.maxTime = T
        if StartAtOnce:
            self.Time = T
        else: 
            self.Time = initTime
        Time_Group.append(self)

    def setMaxTime(self,T):
        self.maxTime = T

    def getTime(self):
        return self.Time
        
    def tick(self):
        self.Time += 1
        return self.Time

    def check(self):
        if self.Time >= self.maxTime:
            self.reset()
            return True
        return False

    def reset(self):
        self.Time = 0

    def __del__(self):
        Time_Group.remove(self)

class MYTIME2(MYTIME):
    def __init__(self,T=0, initTime=0, StartAtOnce=False):
        MYTIME.__init__(self,T,initTime,StartAtOnce)
        self.count = 0
    def check(self):
        if self.Time >= self.maxTime:
            self.count+=1
            self.reset()
            return True
        return False
    def checkCount(self,count):
        if self.count >= count:
            self.count = 0
            return True
        return False
    def resetCount(self):
        self.count = 0

def main():
    t = MYTIME(10)
    t2 = MYTIME(10)
    t.begin()
    print(t.getTime())
    print(Time_Group.times)
    Time_Group.tick()
    print(t.getTime())
if __name__ == "__main__":
    main()
