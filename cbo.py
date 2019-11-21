import sys
from time import time
from IntervalPattern import Pattern, PatternConfig
import argparse

patterns = []
L = []
G = set()
f_out = 0
original_matrix = []
concept_count = 0
max_bic_count = 0

def process(A, g, concept, start_time):  # see thesis of Kaytoue
    #print 'process', A
    global concept_count
    global max_bic_count
    if concept_count == max_bic_count and max_bic_count > 0:
        return
    C_minus_A = set(concept.objects) - A
    less_than_g = set(filter(lambda x: x < g, C_minus_A))
    if len(less_than_g) == 0:
        if len(concept.objects) >= concept.cfg.min_row:
            f_out.write(str(concept) + '|' + str(len(concept.objects)) + '|' + str(concept.objects) + '\n')
            #mse = calculate_mse(concept.objects, concept.col_list())
            #f_out.write(str("{:.3f}".format(mse)) + ' ' + str(len(concept.objects)) + 'x' + str(len(concept.col_list())) + str(concept.objects) + ' ' + str(concept.col_list()) + '\n')
            concept_count += 1
            if concept_count == 10 or concept_count == 100 or concept_count == 500:
                f_out.write('check point ' + str(concept_count) + ' ' + str(time() - start_time) + '\n')
        G_minus_C = G - set(concept.objects)
        more_than_g = set(filter(lambda l: l > g, G_minus_C))
        for f in more_than_g:
            z = set(concept.objects)
            z.add(f)
            new_candidate = concept.intersect(patterns[f])
            if new_candidate.col_count < new_candidate.cfg.min_col:
                # kalau kolom yang nggak * jumlahnya kurang dari mincol, nggak usah dilanjutkan,
                # karena menurutku col_count nggak akan nambah, adanya berkurang
                continue
            if len(z) >= new_candidate.cfg.min_row:  # kalau len(extent) kurang dari min_row, ngitung closure nya nanti aja, setelah nemu len(extent) yang >= minrow
                x = closure(new_candidate, z)
            else:
                x = list(z)
            new_candidate.objects = x
            process(z, f, new_candidate, start_time)
    else:
        #print 'backtrack'
        pass
    return


def calculate_mse(objects, columns):
    submatrix = get_submatrix(objects, columns)
    means_row = []
    means_col = [0] * len(submatrix[0])
    means_all = 0
    for i2 in range(0, len(submatrix)):
        summation = 0
        for j in range(0, len(submatrix[0])):
            summation += submatrix[i2][j]
            means_col[j] += submatrix[i2][j]
            means_all += submatrix[i2][j]
        means_row.append(summation / len(submatrix[0]))
    means_all = means_all / (len(submatrix) * len(submatrix[0]))
    for m in range(0, len(means_col)):
        means_col[m] = means_col[m] / len(submatrix)
    error = 0
    for i2 in range(0, len(submatrix)):
        for j in range(0, len(submatrix[0])):
            error += (submatrix[i2][j] - means_col[j] - means_row[i2] + means_all) ** 2
    error = error / (len(submatrix) * len(submatrix[0]))
    return error


def get_submatrix(objects, columns):
    result = []
    for o in objects:
        row = []
        for c in columns:
            row.append(original_matrix[o][c])
        result.append(list(row))
    return result


def closure(input_pattern, no_check):
    #print 'closure', no_check
    if input_pattern.col_count == 0:
        return list(G)
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


def alignment(base_row, input_row, base_column_index, type):
    base_cells = base_row.split()
    input_cells = input_row.split()
    difference_a = float(input_cells[base_column_index]) - float(base_cells[base_column_index])
    if base_cells[base_column_index] == '0':
        difference_m = float(input_cells[base_column_index]) / 0.1
    else:
        difference_m = float(input_cells[base_column_index]) / float(base_cells[base_column_index])

    if difference_m == 0:
        difference_m = 0.1

    out = ''
    for cell in input_cells:
        if type == 'a':
            out += str(float(cell) - difference_a) + '\t'
        elif type == 'm':
            out += str(round(float(cell) / difference_m, 1)) + '\t'
    return out[:-1]


if __name__ == "__main__":
    __parser__ = argparse.ArgumentParser(description='CBO')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=float, help='Maximal length for intervals [0,inf]', default=1)
    __parser__.add_argument('-c', '--min_columns', metavar='min_columns', type=int, help='minimum number of columns', default=1)
    __parser__.add_argument('-r', '--min_rows', metavar='min_rows', type=int, help='minimum number of rows', default=1)
    __parser__.add_argument('-n', '--number_of_biclusters', metavar='number_of_biclusters', type=int, help='max number of biclusters', default=100)
    __parser__.add_argument('-type', '--bicluster_type', metavar='bicluster_type', type=str, help='c=constant, a=additive, m=multiplicative', default='c')
    __args__ = __parser__.parse_args()

    with open(__args__.context_path, 'r') as f_in:
        for object_id, line in enumerate(f_in):
            raw_entry = line.replace('\n', '').replace('\r', '')
            numbers = raw_entry.split('\t')
            original_matrix.append(list([float(i) for i in numbers]))

    start_time = time()
    cfg = PatternConfig(theta=__args__.theta, min_col=__args__.min_columns, min_row=__args__.min_rows)
    f_out = open('cbo_' + __args__.context_path + '_type-' + __args__.bicluster_type + '_t' + str(__args__.theta) + '_c' + str(__args__.min_columns) + '_r' + str(__args__.min_rows) + '.txt', 'w')

    if __args__.bicluster_type == 'c':
        with open(__args__.context_path, 'r') as f_in:
            for object_id, line in enumerate(f_in):
                #print 'line', object_id
                raw_entry = line.replace('\n', '').replace('\r', '')
                patterns.append(Pattern(instance=raw_entry, config=cfg, object=object_id))
                G.add(object_id)

        max_bic_count = __args__.number_of_biclusters
        for i in patterns:
            print 'iter', i.objects[0]
            start_iter = time()
            if concept_count == max_bic_count and max_bic_count > 0:
                break
            candidate_concept = Pattern(dirty=False, config=cfg)
            candidate_concept.intervals = list(i.intervals)
            candidate_concept.objects = closure(i, set(i.objects))
            process(set(i.objects), i.objects[0], candidate_concept, start_time)
            # print(time() - start_iter)

    else:
        column_count = 0
        max_bic_count = __args__.number_of_biclusters
        base_row = ''
        with open(__args__.context_path, 'r') as f_in:  # buat ngitung kolom
            for object_id, line in enumerate(f_in):
                base_row = line.replace('\n', '').replace('\r', '')
                cells = base_row.split('\t')
                column_count = len(cells)
                break

        enough_concept = False
        for column in range(0, column_count):
            G = set()
            patterns = []
            print 'column', column
            f_out.write('column ' + str(column) + '\n')
            with open(__args__.context_path, 'r') as f_in:
                for object_id, line in enumerate(f_in):
                    raw_entry = line.replace('\n', '').replace('\r', '')
                    aligned = alignment(base_row, raw_entry, column, __args__.bicluster_type)
                    #print 'aligned', aligned
                    patterns.append(Pattern(instance=aligned, config=cfg, object=object_id))
                    G.add(object_id)
            for i in patterns:
                #print 'iter', i.objects[0]
                start_iter = time()
                if concept_count == max_bic_count and max_bic_count > 0:
                    enough_concept = True
                    break
                candidate_concept = Pattern(dirty=False, config=cfg)
                candidate_concept.intervals = list(i.intervals)
                candidate_concept.objects = closure(i, set(i.objects))
                process(set(i.objects), i.objects[0], candidate_concept, start_time)
            if enough_concept:
                break


    end_time = time()
    print(end_time - start_time)
