a = [['a', 'b', 'c', 'd'],['1', '2', '3', 'd']]
transposed =list(map(list,zip(*a)))
print(transposed)