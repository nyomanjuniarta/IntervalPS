from fca.algorithms.cbo import CbO
from fca.defs import OnDiskPOSET, POSET, SetPattern
from fca.defs.patterns import IntervalPattern

lst2str = lambda lst: reduce(lambda x, y: str(x)+', '+str(y), lst+['']).strip()[:-1] if len(lst) > 0 else "[]"


def dict_printer(poset, **kwargs):  # print_support=False, transposed=False, indices=False):
    """
    Nicely print the concepts in the poset
    """
    template = kwargs.get('template', '{:4s}\t{:20s}\t{:20s}')
    transposed = kwargs.get('transposed', False)
    indices = kwargs.get('indices', False)
    extent_postproc = kwargs.get('extent_postproc', lst2str)
    intent_postproc = kwargs.get('intent_postproc', lst2str)

    ema = poset.EXTENT_MARK
    ima = poset.INTENT_MARK
    if transposed:
        ema = poset.INTENT_MARK
        ima = poset.EXTENT_MARK

    order = lambda s: (
        len(s[1][ema]), s[1][ima]
    )
    for i in range(1, len(poset.node)):
        for interval in poset[i][ima]:
            if interval[0] > -1000:
                print interval[0], interval[1], '|',
            else:
                print '* |',
        print len(poset[i][ema]), ':', list(poset[i][ema])


class PSCbO(CbO):
    """
    Implementation of Close-by-One for pattern structures,
    It is just a bottom-up enumeration and pattern structures
    are contained by extents, not intents
    """

    def derive_extent(self, descriptions):
        """
        Obtain next iteration extent
        """
        return reduce(self.e_pattern.intersection, descriptions)

    def derive_intent(self, *args):

        new_extent = args[0]
        result = set(
            [m for m, desc in self.ctx.m_prime.items() if m in args[1] or self.e_pattern.leq(new_extent, desc)]
        )
        return result

    def config(self):
        self.e_pattern = self.pattern
        self.pattern = SetPattern

        if not self.ondisk:
            self.poset = POSET(transformer=self.ctx.transformer)
        else:
            self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)

        map(self.e_pattern.top, self.ctx.g_prime.values())
        self.all_objects = self.e_pattern.top()
        self.poset.new_formal_concept(
            self.e_pattern.top(),
            self.pattern.bottom(),
            self.poset.supremum
        )
        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        self.ctx.n_attributes = len(self.ctx.g_prime)

        # THE NOTION OF MINIMUM SUPPORT SHOULD NOT BE APPLIED
        # DIRECTLY TO PATTERN STRUCTURE EXTENTS, SINCE THEY APPLY
        # ONLY TO SetPattern PATTERN STRUCTURES
        # IF YOU WANT TO FORCE THEM, UNCOMMENT NEXT LINES
        '''
        self.conditions.append(
            lambda new_extent: len(new_extent) >= self.min_sup * self.ctx.n_objects
        )
        '''

    def run(self, *args, **kwargs):
        self.cbo(self.poset.supremum, self.e_pattern.top(), self.pattern.bottom())


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
