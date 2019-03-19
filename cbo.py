import sys
from time import time
from IntervalPattern import Pattern, PatternConfig

patterns = []
L = []
G = set()


def process(A, g, concept):  # see thesis of Kaytoue
    #print 'process', concept
    C_minus_A = concept.objects - A
    less_than_g = set(filter(lambda x: x < g, C_minus_A))
    if len(less_than_g) == 0:
        L.append(concept)
        print 'something is added'
        G_minus_C = G - concept.objects
        more_than_g = set(filter(lambda x: x > g, G_minus_C))
        for f in more_than_g:
            z = set(concept.objects)
            z.add(f)
            new_candidate = concept.intersect(patterns[f])
            x = closure(new_candidate)
            new_candidate.objects = x
            process(z, f, new_candidate)
    return


def closure(input_pattern):
    objects = set()
    for p in patterns:
        if input_pattern <= p:
            objects.add(p.objects[0])
    return objects


if __name__ == "__main__":
    start_time = time()
    path = sys.argv[1]
    if len(sys.argv) > 2:  # theta = maximum interval
        theta = float(sys.argv[2])
    else:
        theta = 1
    cfg = PatternConfig(theta)
    with open(path, 'r') as f:
        for object_id, line in enumerate(f):
            #print 'line', object_id
            raw_entry = line.replace('\n', '').replace('\r', '')
            patterns.append(Pattern(instance=raw_entry, config=cfg, object=object_id))
            G.add(object_id)

    for i in patterns:
        print 'iter', i.objects[0]
        candidate_concept = Pattern(dirty=False, config=cfg)
        candidate_concept.intervals = list(i.intervals)
        candidate_concept.objects = closure(i)
        process(set(i.objects), i.objects[0], candidate_concept)

    with open('cbo_' + path + '_t' + str(theta) + '.txt', 'w') as f:
        for l in L:
            f.write(str(l) + ':' + str(len(l.objects)) + ':' + str(l.objects) + '\n')
    end_time = time()
    print(end_time - start_time)
