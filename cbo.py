import sys
from time import time
from IntervalPattern import Pattern, PatternConfig

patterns = []
L = []
G = set()
f_out = 0

def process(A, g, concept):  # see thesis of Kaytoue
    C_minus_A = set(concept.objects) - A
    less_than_g = set(filter(lambda x: x < g, C_minus_A))
    #print 'process', concept.objects
    if len(less_than_g) == 0:
        f_out.write(str(concept) + '|' + str(len(concept.objects)) + '|' + str(concept.objects) + '\n')
        #print 'adding', concept
        G_minus_C = G - set(concept.objects)
        more_than_g = set(filter(lambda l: l > g, G_minus_C))
        for f in more_than_g:
            z = set(concept.objects)
            z.add(f)
            new_candidate = concept.intersect(patterns[f])
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
    path = sys.argv[1]
    if len(sys.argv) > 2:  # theta = maximum interval
        theta = float(sys.argv[2])
    else:
        theta = 1
    cfg = PatternConfig(theta)
    f_out = open('cbo_' + path + '_t' + str(theta) + '.txt', 'w')
    with open(path, 'r') as f_in:
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
