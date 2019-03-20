from fca.defs.patterns import IntervalPattern
from fca.defs import Intent


'''class IntervalPattern(Intent):
    """
    Interval pattern as defined by Kaytoue
    CONVEX HULL: [a,b] \\cap [x,y] = [min(a,x),max(b,y)]
    """

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = []
        return cls._top

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = []
        if bot_rep is not None:
            if bool(cls._bottom):
                cls.meet(cls._bottom, bot_rep)
            else:
                for i in bot_rep:
                    cls._bottom.append(i)
        return cls._bottom

    @classmethod
    def meet(cls, desc1, desc2):
        for i, (j, k) in enumerate(zip(desc1, desc2)):
            desc1[i] = (min(j[0], k[0]), max(j[1], k[1]))

    @classmethod
    def intersection(cls, desc1, desc2):
        if desc2 == cls._top:
            return desc1
        interval = [(min(i[0], j[0]), max(i[1], j[1])) for i, j in zip(desc1, desc2)]
        return interval

    @classmethod
    def leq(cls, desc1, desc2):
        # print desc1, desc2,
        if desc1==cls._bottom:
            return True
        for i, j in zip(desc1, desc2):
            if i[0] > j[0] or i[1] < j[1]:
                return False
        return True

    @classmethod
    def is_equal(cls, desc1, desc2):
        if len(desc1) != len(desc2):
            return False
        for i, j in zip(desc1, desc2):
            if i[0] != j[0] or i[1] != j[1]:
                return False
        return True

    @classmethod
    def join(cls, desc1, desc2):
        if desc1 == cls._top:
            return True
        raise NotImplementedError

    @classmethod
    def union(cls, desc1, desc2):
        raise NotImplementedError

    @classmethod
    def is_empty(cls, desc):
        return False

    @classmethod
    def contains(cls, desc, key):
        return key in desc

    @classmethod
    def length(cls, desc):
        return len(desc)

    @classmethod
    def get_iterator(cls, desc):
        for interval in desc:
            yield interval'''


class MaxLengthIntervalPattern(IntervalPattern):
    """
    In this example we make a custom pattern structure by modifying
    an existing one
    Particularly, we modify the IntervalPattern intersection
    to allow for a similarity thresholding of each individual interval
    """
    THETA = 0

    @classmethod
    def intersection(cls, desc1, desc2):
        """
        Each interval should be at most of length THETA
        if not, put * in the interval > THETA
        """
        # print desc1, desc2,'::',
        print 'new_interval'
        if desc1 == cls._top:
            return desc2
        new_interval = []
        bottom = False
        for i, j in zip(desc1, desc2):
            #new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
            if max(i[1], j[1]) - min(i[0], j[0]) > MaxLengthIntervalPattern.THETA:
                #bottom = True
                new_interval.append((-1000, 1000))
            else:
                new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
        '''
        if bottom:
            bot = MaxLengthIntervalPattern.bottom(new_interval)
            # print bot,'<-', id(bot)
            return bot'''

        return new_interval

    '''@classmethod
    def leq(cls, desc1, desc2):
        return True'''
