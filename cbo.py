import sys
from time import time
from IntervalPattern import Pattern, PatternConfig
import argparse

patterns = []
L = []
G = set()
f_out = 0

def process(A, g, concept):  # see thesis of Kaytoue
    C_minus_A = set(concept.objects) - A
    less_than_g = set(filter(lambda x: x < g, C_minus_A))
    if len(less_than_g) == 0:
        f_out.write(str(concept) + '|' + str(len(concept.objects)) + '|' + str(concept.objects) + '\n')
        G_minus_C = G - set(concept.objects)
        more_than_g = set(filter(lambda l: l > g, G_minus_C))
        for f in more_than_g:
            z = set(concept.objects)
            z.add(f)
            new_candidate = concept.intersect(patterns[f])
            if new_candidate.length_less_than_theta() < 0:
                continue
            x = closure(new_candidate, z)
            new_candidate.objects = x
            process(z, f, new_candidate)
    else:
        #print 'backtrack'
        pass
    return


def closure(input_pattern, no_check):
    time1 = time()
    objects = list(no_check)
    check = G - no_check
    for c in check:
        if input_pattern <= patterns[c]:
            objects.append(patterns[c].objects[0])
    '''
    for p in patterns:
        if input_pattern <= p:
            objects.append(p.objects[0])'''
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
    f_out = open('cbo_' + __args__.context_path + '_t' + str(__args__.theta) + '.txt', 'w')
    with open(__args__.context_path, 'r') as f_in:
        for object_id, line in enumerate(f_in):
            #print 'line', object_id
            raw_entry = line.replace('\n', '').replace('\r', '')
            patterns.append(Pattern(instance=raw_entry, config=cfg, object=object_id))
            G.add(object_id)

    for i in patterns:
        print 'iter', i.objects[0]
        candidate_concept = Pattern(dirty=False, config=cfg)
        candidate_concept.intervals = list(i.intervals)
        candidate_concept.objects = closure(i, set(i.objects))
        process(set(i.objects), i.objects[0], candidate_concept)

    end_time = time()
    print(end_time - start_time)
