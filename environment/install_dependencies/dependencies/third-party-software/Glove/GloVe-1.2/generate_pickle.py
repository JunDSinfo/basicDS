import pickle
import numpy as np
vectors_file = "vectors.txt"
with open(vectors_file, 'r') as f:
    vectors = {}
    for line in f:
        vals = line.rstrip().split(' ')
        vectors[vals[0]] = np.asarray(list(map(float, vals[1:])))

    pickle.dump(vectors, open("vectors.pkl", "wb"))