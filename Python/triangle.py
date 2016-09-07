def triangles():
    current_row = [1, 0]
    yield current_row[0:-1]
    while True:
        pre_row = current_row
        current_row[0:-1] = \
            [pre_row[i - 1] + pre_row[i] for i in range(0, len(pre_row))]
        yield pre_row[0:-1]

n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break
