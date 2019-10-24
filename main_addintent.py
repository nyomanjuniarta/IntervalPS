import sys
import argparse
from time import time
from IntervalPattern import Pattern, PatternConfig
from diagram import init_diagram, add_intent, add_object, clean_flags, print_lattice

if __name__ == "__main__":
    start_time = time()
    __parser__ = argparse.ArgumentParser(description='Concept sampling Boley 2011')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=float, help='Maximal length for intervals [0,inf]', default=1)
    __parser__.add_argument('-c', '--min_columns', metavar='min_columns', type=int, help='minimum number of columns', default=1)
    __parser__.add_argument('-r', '--min_rows', metavar='min_rows', type=int, help='minimum number of rows', default=1)
    __args__ = __parser__.parse_args()

    cfg = PatternConfig(theta=__args__.theta, min_col=__args__.min_columns)

    with open(__args__.context_path, 'r') as f:
        L = init_diagram()
        # print_lattice(L, path + '_lattice.txt')
        print L.node[-1]
        for object_id, line in enumerate(f):
            print 'line', object_id
            raw_entry = line.replace('\n', '').replace('\r', '')
            pattern = Pattern(instance=raw_entry, config=cfg, object=object_id)
            # print 'interval', pattern
            object_concept_id = add_intent(pattern, -1, L, 0, max)
            add_object(object_concept_id, object_id, L)
            clean_flags(L, object_concept_id)
    L = L.reverse()
    print_lattice(L, __args__.context_path + '_t' + str(__args__.theta) + '_lattice.txt')
    end_time = time()
    print(end_time - start_time)
