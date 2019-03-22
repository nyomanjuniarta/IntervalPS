import random
row = 11000
col = 5
f_out = open('random' + str(row) + 'x' + str(col) + '.txt', 'w')
for i in range(row):
    result = ''
    for j in range(col):
        result += str(random.randint(0, 100)) + '\t'
    f_out.write(result[:-1] + '\n')
