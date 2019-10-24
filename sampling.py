import random
import math
import argparse
from time import time
from IntervalPattern import Pattern, PatternConfig

patterns = []
pattern_combination2 = []


def weighted_choice(choices, total):
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c, w
        upto += w


def get_objects(input_pattern):
    time1 = time()
    objects = []
    for p in patterns:
        if input_pattern <= p:
            objects.append(p.objects[0])
    time2 = time()
    # print len(check), 'compute closure', (time2 - time1)
    return objects


if __name__ == "__main__":
    start_time = time()
    __parser__ = argparse.ArgumentParser(description='Concept sampling Boley 2011')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=float, help='Maximal length for intervals [0,inf]', default=1)
    __parser__.add_argument('-m', '--weight_measure', metavar='weight_measure', type=str, help='f = frequency, a = area', default='f')
    __parser__.add_argument('-c', '--min_columns', metavar='min_columns', type=int, help='minimum number of columns', default=2)
    __parser__.add_argument('-r', '--min_rows', metavar='min_rows', type=int, help='minimum number of rows', default=3)
    __args__ = __parser__.parse_args()

    cfg = PatternConfig(__args__.theta)
    with open(__args__.context_path, 'r') as f:
        for object_id, line in enumerate(f):
            raw_entry = line.replace('\n', '').replace('\r', '')
            patterns.append(Pattern(instance=raw_entry, config=cfg, object=object_id))

    total_weight = 0
    counter = 0
    weights = []
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            new_pattern = patterns[i].intersect(patterns[j])
            if new_pattern.length_less_than_theta() < __args__.min_columns:
                continue
            if __args__.weight_measure == 'f':
                weight = math.pow(2, new_pattern.length_less_than_theta())
            elif __args__.weight_measure == 'a':
                weight = new_pattern.area()
            pattern_combination2.append(new_pattern)
            weights.append((counter, weight))
            total_weight += weight
            counter += 1

    print 'start drawing'
    stop = 10
    while stop > 0:
        end_time = time()
        if (end_time - start_time) > 300:
            break
        chosen_index, weight = weighted_choice(weights, total_weight)
        chosen_pattern = pattern_combination2[chosen_index]
        chosen_pattern.objects = get_objects(chosen_pattern)
        new_pattern = chosen_pattern.widen()
        new_pattern.objects = get_objects(new_pattern)
        if len(new_pattern.objects) < __args__.min_rows or new_pattern.length_less_than_theta() < __args__.min_columns:
            continue
        #print chosen_pattern, chosen_pattern.objects
        #print new_pattern
        print new_pattern.rows(), new_pattern.objects
        print '===='
        stop -= 1

    end_time = time()
    print(end_time - start_time)
