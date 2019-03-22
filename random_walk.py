import random
import math
import argparse
from time import time
from IntervalPattern import Pattern, PatternConfig

patterns = []


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
    __parser__.add_argument('-c', '--min_columns', metavar='min_columns', type=int, help='minimum number of columns', default=2)
    __parser__.add_argument('-r', '--min_rows', metavar='min_rows', type=int, help='minimum number of rows', default=3)
    __args__ = __parser__.parse_args()

    cfg = PatternConfig(theta=__args__.theta, min_col=__args__.min_columns)
    with open(__args__.context_path, 'r') as f:
        for object_id, line in enumerate(f):
            raw_entry = line.replace('\n', '').replace('\r', '')
            patterns.append(Pattern(instance=raw_entry, config=cfg, object=object_id))

    g = random.randint(0, len(patterns))
    current = ([g], patterns[g])
    while True:
        if len(current[0]) < __args__.min_rows:
            g2 = random.randint(0, len(patterns))
            print 'add', g2
            new_intent = current[1].intersect(patterns[g2])
            new_extent = get_objects(new_intent)
            current = (new_extent, new_intent)
            print current
        elif current[1].length_less_than_theta() < __args__.min_columns:
            new_extent = list(current[0])
            popped = new_extent.pop(random.randint(0, len(new_extent) - 1))
            #print 'delete', popped
            new_intent = patterns[new_extent[0]]
            for g in new_extent:
                new_intent = new_intent.intersect(patterns[g])
            current = (new_extent, new_intent)
        else:
            break


