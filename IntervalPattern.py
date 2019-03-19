import itertools


def pattern_parser(line):
    numbers = line.split('\t')
    pattern = list()
    for number in numbers:
        pattern.append(tuple([float(number), float(number)]))
    return pattern


def pattern_parser_for_testing(line):
    intervals = line.split(' ')
    pattern = list()
    for interval in intervals:
        numbers = interval.split(',')
        pattern.append(tuple([float(numbers[0]), float(numbers[1])]))
    return pattern


class PatternConfig:
    def __init__(self, theta=1):
        self.theta = theta


class Pattern:
    def __init__(self, instance=None, dirty=True, config=None, object=-1):
        self.objects = []
        self.intervals = []
        if not config:
            self.cfg = PatternConfig(1)
        else:
            self.cfg = config

        if dirty:
            self.intervals = pattern_parser(instance)
            self.objects.append(object)

    def intersect(self, other):
        pi = Pattern(instance=None, config=self.cfg, dirty=False)
        interval_intersection = list()
        for i in range(len(self.intervals)):
            if len(self.intervals[i]) > 1 and len(other.intervals[i]) > 1:
                lower = min(self.intervals[i][0], other.intervals[i][0])
                upper = max(self.intervals[i][1], other.intervals[i][1])
                if upper - lower <= self.cfg.theta:
                    interval_intersection.append(tuple([lower, upper]))
                else:
                    interval_intersection.append(tuple(['*']))
            else:
                interval_intersection.append(tuple(['*']))
        pi.intervals = interval_intersection
        return pi

    def __eq__(self, other):
        if self.intervals == other.intervals:
            return True
        return False

    def __le__(self, other):
        if len(other.intervals) == 0:
            return False
        for i in range(len(self.intervals)):
            if len(other.intervals[i]) == 1:
                if len(self.intervals[i]) > 1:
                    return False
            elif len(self.intervals[i]) > 1:
                if self.intervals[i][0] > other.intervals[i][0] or self.intervals[i][1] < other.intervals[i][1]:
                    return False
        return True

    def size(self):
        return len(self.objects)

    def __repr__(self):
        output = ''
        for interval in self.intervals:
            if len(interval) > 1:
                output += '[' + str(interval[0]) + ',' + str(interval[1]) + ']'
            else:
                output += '[*]'
        return output
