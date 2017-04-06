#!/usr/bin/python
import os, sys
import numpy as np
from random import random

def choose_coin(prob_coin_r):
    "Choose red coin with probability prob_coin_r, otherwise choose blue."
    if random() < prob_coin_r:
        return "R"
    return "B"

def flip_coin(prob_head):
    "Return H (head) with probability prob_head, otherwise T (tail)."
    if random() < prob_head:
        return "H"
    return "T"

def flip_coin_m_times(m, prob_head):
    "Flip a coin m times and return the results."
    return [flip_coin(prob_head) for i in range(m)]

def generate_n_samples_size_m(n, m, prob_coin_r, prob_head_r, prob_head_b):
    "Choose n coins and flip each one m times."
    samples, labels = [], []
    for i in range(n):
        if choose_coin(prob_coin_r) == "R":
            labels.append("R")
            sample = flip_coin_m_times(m, prob_head_r)
        else:
            labels.append("B")
            sample = flip_coin_m_times(m, prob_head_b)
        samples.append(sample)
    return samples, labels

def get_maximum_likelihood_estimates(labels, samples):
    # TODO: Estimate the parameters from the labels and samples.
    labels = np.array(labels)
    samples = np.array(samples)

    red_coin = (labels == 'R')
    estimate_prob_coin_r = np.mean(red_coin)
    estimate_prob_head_r = np.mean(samples[red_coin] == 'H')
    estimate_prob_head_b = np.mean(samples[np.bool_(1 - red_coin)] == 'H')
    
    return estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b

def read_user_input(args):
    if len(args) != 5:
        prob_coin_r = eval(input("Enter probability of red coin: "))
        prob_head_r = eval(input("Enter probability of head for red coin: "))
        prob_head_b = eval(input("Enter probability of head for blue coin: "))
        n = eval(input("Enter number of coins to flip: "))
        m = eval(input("Enter number of times to flip each coin: "))
    else:
        prob_coin_r = float(args[0])
        prob_head_r = float(args[1])
        prob_head_b = float(args[2])
        n = int(args[3])
        m = int(args[4])
    assert prob_coin_r >=0 and prob_coin_r <= 1
    assert prob_head_r >=0 and prob_head_r <= 1
    assert prob_head_b >=0 and prob_head_b <= 1
    assert m > 0 and n > 0
    return prob_coin_r, prob_head_r, prob_head_b, n, m
    
if __name__ == "__main__":
    prob_coin_r, prob_head_r, prob_head_b, n, m = read_user_input(sys.argv[1:])
    samples, labels = generate_n_samples_size_m(
        n, m, prob_coin_r, prob_head_r, prob_head_b)
    for i, sample in enumerate(samples):
        print(labels[i], sample)

    estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b = (
        get_maximum_likelihood_estimates(labels, samples))

    print("Maximum likelihood estimates:")
    print("estimate_prob_coin_r = %1.4f (actual = %1.4f)" % (estimate_prob_coin_r, prob_coin_r))
    print("estimate_prob_head_r = %1.4f (actual = %1.4f)" % (estimate_prob_head_r, prob_head_r))
    print("estimate_prob_head_b = %1.4f (actual = %1.4f)" % (estimate_prob_head_b, prob_head_b))
    print("number of coins = %d" % n)
    print("number of times each coin was flipped = %d" % m)
    print("total coin flips = %d" % (m * n))
    print("Note: To rerun use ./coins_example.py %1.4f %1.4f %1.4f %d %d" % (
        prob_coin_r, prob_head_r, prob_head_b, n, m))
