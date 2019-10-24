import random


def pattern_parser(line):
    numbers = line.split('\t')
    pattern = list()
    for number in numbers:
        pattern.append((float(number), float(number)))
    return pattern


def pattern_parser_for_testing(line):
    intervals = line.split(' ')
    pattern = list()
    for interval in intervals:
        numbers = interval.split(',')
        pattern.append((float(numbers[0]), float(numbers[1])))
    return pattern


class PatternConfig:
    def __init__(self, theta=1, min_col=2, min_row=1, range_min=-1000, range_max=1000):
        self.theta = theta
        self.min_col = min_col
        self.min_row = min_row
        self.range_min = range_min
        self.range_max = range_max


class Pattern:
    def __init__(self, instance=None, dirty=True, config=None, object=-1):
        self.objects = []
        self.intervals = []
        self.col_count = 0
        if not config:
            self.cfg = PatternConfig(1)
        else:
            self.cfg = config

        if dirty:
            self.intervals = pattern_parser(instance)
            self.col_count = len(self.intervals)
            self.objects.append(object)

    def intersect(self, other):
        pi = Pattern(instance=None, config=self.cfg, dirty=False)
        pi.objects = self.objects + other.objects
        if self.cfg.min_col > 1:
            interval_intersection = []
            pi.col_count = 0
            for i in range(len(self.intervals)):
                if self.intervals[i][0] == self.cfg.range_min or other.intervals[i][0] == self.cfg.range_min:
                    interval_intersection.append((self.cfg.range_min, self.cfg.range_max))
                    continue

                lower = min(self.intervals[i][0], other.intervals[i][0])
                upper = max(self.intervals[i][1], other.intervals[i][1])
                if upper - lower <= self.cfg.theta:
                    pi.col_count += 1
                    interval_intersection.append((lower, upper))
                else:
                    interval_intersection.append((self.cfg.range_min, self.cfg.range_max))
            if pi.col_count >= self.cfg.min_col:
                pi.intervals = interval_intersection
            else:
                interval_intersection = []
                for i in range(len(self.intervals)):
                    interval_intersection.append((self.cfg.range_min, self.cfg.range_max))
                pi.intervals = interval_intersection
        else:
            pi.col_count = 0
            for i in range(len(self.intervals)):
                lower = min(self.intervals[i][0], other.intervals[i][0])
                upper = max(self.intervals[i][1], other.intervals[i][1])
                if upper - lower <= self.cfg.theta:
                    pi.intervals.append((lower, upper))
                    pi.col_count += 1
                else:
                    pi.intervals.append((self.cfg.range_min, self.cfg.range_max))
        return pi

    def __eq__(self, other):
        if self.intervals == other.intervals:
            return True
        return False

    def __le__(self, other):
        if len(other.intervals) < 1:
            return False
        for i in range(len(self.intervals)):
            if self.intervals[i][0] > other.intervals[i][0] or self.intervals[i][1] < other.intervals[i][1]:
                return False
        return True

    def size(self):
        return len(self.objects)

    def length_less_than_theta(self):
        length = 0
        for interval in self.intervals:
            if interval[0] > self.cfg.range_min:
                length += 1
        return length

    def area(self):
        area = 0
        for interval in self.intervals:
            if interval[0] > -1000:
                area += interval[1] - interval[0]
        return area

    def widen(self):
        p = Pattern(instance=None, config=self.cfg, dirty=False)
        p.objects = list(self.objects)
        for interval in self.intervals:
            x = random.randint(0, 1)
            if interval[0] == self.cfg.range_min:
                p.intervals.append(interval)
            elif x == 0:
                p.intervals.append((self.cfg.range_min, self.cfg.range_max))
            else:
                lower = interval[0]
                upper = interval[1]
                available = self.cfg.theta * 2 - (upper - lower)
                y = random.randint(0, 2)
                #if x == 1:
                new_lower = lower - (available/2)
                new_upper = upper + (available/2)
                p.intervals.append((new_lower, new_upper))
                '''elif y == 0:
                    new_lower = interval[0] - available
                    p.intervals.append((new_lower, upper))
                elif y == 2:
                    new_upper = interval[1] + available
                    p.intervals.append((lower, new_upper))'''
        return p

    def rows(self):
        output = ''
        counter = 0
        for interval in self.intervals:
            if interval[0] > self.cfg.range_min:
                output += str(counter) + ', '
            counter += 1
        return output[:-2]

    def col_list(self):
        result = []
        column_counter = 0
        for interval in self.intervals:
            if interval[0] > self.cfg.range_min:
                result.append(column_counter)
            column_counter += 1
        return result

    def __repr__(self):
        output = ''
        for interval in self.intervals:
            if interval[0] > self.cfg.range_min:
                output += str(interval[0]) + ',' + str(interval[1]) + '|'
            else:
                output += '*|'
        return output[:-1]
