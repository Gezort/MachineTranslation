# coding: utf8

import sys

import numpy as np

from embeddings import Vocab, WordEmbedding


def load_example_sets(path):
    # Loads list of pairs per line.
    return [[tuple(pair.split()) for pair in line.strip().split('\t')] for line in open(path)]

def load_labels(path):
    # Loads a label for each line (-1 indicates the pairs do not form a relation).
    return [int(label) for label in open(path)]

def cosine(x, y):
    # Cosine of angle between vectors x and y
    return x.dot(y) / np.linalg.norm(x) / np.linalg.norm(y)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "Usage ./detect_relations.py vocab_file embedding_file train_data train_labels test_data"
        sys.exit(0)

    # Load vocab and embedding (these are not used yet!)
    vocab = Vocab(sys.argv[1])
    embedding = WordEmbedding(vocab, sys.argv[2])

    # Loads training data and labels.
    training_examples = load_example_sets(sys.argv[3])
    training_labels = load_labels(sys.argv[4])

    assert len(training_examples) == len(training_labels), "Expected one label for each line in training data."

    # Load test examples and labels each set of pairs as 'not a relation' (-1)
    # This is not a good idea... You can definitely do better!
    test_examples = load_example_sets(sys.argv[5])


    # Store displacement between embeddings for each label in train
    training_displacements = {lbl: [] for lbl in training_labels}
    for i, lbl in enumerate(training_labels):
        for x,y in training_examples[i]:
            displ = embedding.Projection(y.decode('utf-8')) - embedding.Projection(x.decode('utf-8'))
            training_displacements[lbl].append(displ)

    with open('result.txt', 'w') as f:
        threshold = 0.2
        for j, row in enumerate(test_examples):
            labels = training_displacements.keys()
            mean_cosine_distances = []
            for lbl in labels:
                distances = []
                for x,y in row:
                    cur_displ = embedding.Projection(y.decode('utf-8')) - embedding.Projection(x.decode('utf-8'))
                    if  np.abs(cur_displ).max() == 0:
                        cur_displ += 1e-8
                    for displ in training_displacements[lbl]:
                        distances.append(cosine(cur_displ, displ))
                if distances:
                    mean_cosine_distances.append(np.mean(distances))
                else:
                    mean_cosine_distances.append(-1)
            ind = np.argsort(mean_cosine_distances)[::-1]
            predicted_label = labels[ind[0]] if mean_cosine_distances[ind[0]] >= threshold else -1
            f.write('%d\n' % predicted_label)
