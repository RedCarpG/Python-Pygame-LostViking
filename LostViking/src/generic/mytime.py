class TimeGroup(object):
    times = []

    @classmethod
    def append(cls, my_time):
        cls.times.append(my_time)

    @classmethod
    def tick(cls):
        for each in cls.times:
            each.tick()

    @classmethod
    def remove(cls, my_time):
        cls.times.remove(my_time)


class MyTime(object):
    def __init__(self, t=0, init_time=0, start_at_once=False):
        self.maxTime = t
        if start_at_once:
            self.Time = t
        else:
            self.Time = init_time
        TimeGroup.append(self)

    def set_max_time(self, t):
        self.maxTime = t

    def get_time(self):
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
        TimeGroup.remove(self)


class MyTime2(MyTime):
    def __init__(self, t=0, init_time=0, start_at_once=False):
        MyTime.__init__(self, t, init_time, start_at_once)
        self.count = 0

    def check(self):
        if self.Time >= self.maxTime:
            self.count += 1
            self.reset()
            return True
        return False

    def check_count(self, count):
        if self.count >= count:
            self.count = 0
            return True
        return False

    def reset_count(self):
        self.count = 0


def main():
    t = MyTime(10)
    t2 = MyTime(10)
    t.begin()
    print(t.get_time())
    print(TimeGroup.times)
    TimeGroup.tick()
    print(t.get_time())


if __name__ == "__main__":
    main()
