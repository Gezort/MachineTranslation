#!/usr/bin/python
import os, sys
from math import log, isnan
import numpy as np
from random import random
from coins_example import generate_n_samples_size_m
from coins_example import read_user_input

def infer_posterior_probs_coin_r(samples, estimate_prob_coin_r,
                                 estimate_prob_head_r, estimate_prob_head_b):
    "Given the current model estimates, infer the probability of red coin for each sample."
    # TODO: Estimate these variables correctly
    samples = np.array(samples)
    n_heads = np.sum(samples == 'H', axis=1)
    n_traverses = np.sum(samples == 'T', axis=1)

    if isnan(estimate_prob_coin_r):
        raise Exception
    prob_coin_r = estimate_prob_coin_r * estimate_prob_head_r ** n_heads * (1 - estimate_prob_head_r) ** n_traverses
    prob_coin_b = (1 - estimate_prob_coin_r) * estimate_prob_head_b ** n_heads * (1 - estimate_prob_head_b) ** n_traverses
    posterior_probs_coin_r = prob_coin_r / (prob_coin_r + prob_coin_b)

    expected_log_likelihood = np.log(prob_coin_r) * posterior_probs_coin_r + np.log(prob_coin_b) * (1 - posterior_probs_coin_r)
    return posterior_probs_coin_r, np.sum(expected_log_likelihood)

def get_expected_statistics(posterior_probs_coin_r, samples):
    "Given the posterior probability of red coin for each sample, collect fractional counts."
    # TODO: Estimate these variables correctly
    samples = np.array(samples)
    n_samples, n_tosses = samples.shape
    n_heads = np.sum(samples == 'H', axis=1)

    expected_count_coin_r = n_tosses * np.sum(posterior_probs_coin_r)
    expected_count_coin_b = n_tosses * np.sum(1 - posterior_probs_coin_r)

    expected_count_head_r = np.sum(n_heads * posterior_probs_coin_r)
    expected_count_head_b = np.sum(n_heads * (1 - posterior_probs_coin_r))

    return expected_count_coin_r, expected_count_coin_b, expected_count_head_r, expected_count_head_b

def get_maximum_likelihood_estimates(expected_count_coin_r, expected_count_coin_b,
                                         expected_count_head_r, expected_count_head_b):
    estimate_prob_coin_r = 1. * expected_count_coin_r / (expected_count_coin_r + expected_count_coin_b)
    estimate_prob_head_r = (expected_count_head_r * 1. / expected_count_coin_r)
    estimate_prob_head_b = (expected_count_head_b * 1. / expected_count_coin_b)
    return estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b


def em(samples, estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b):
    "Perform one iteration of em: inter posterior, compute expected statistics, update estimates."
    posterior_probs_coin_r, expected_log_likelihood = infer_posterior_probs_coin_r(
        samples, estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b)
    expected_count_coin_r, expected_count_coin_b, expected_count_head_r, expected_count_head_b = (
        get_expected_statistics(posterior_probs_coin_r, samples))
    estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b = (
        get_maximum_likelihood_estimates(expected_count_coin_r, expected_count_coin_b,
        
        
                                         expected_count_head_r, expected_count_head_b))

    return estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b, expected_log_likelihood

if __name__ == "__main__":
    prob_coin_r, prob_head_r, prob_head_b, n, m = read_user_input(sys.argv[1:])
    samples, _ = generate_n_samples_size_m(
        n, m, prob_coin_r, prob_head_r, prob_head_b)
    estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b = 0.5, 0.51, 0.49
    previous_expected_log_likelihood = 0.0
    for i in range(1000):
        estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b, expected_log_likelihood = (
            em(samples, estimate_prob_coin_r, estimate_prob_head_r, estimate_prob_head_b))
        print("expected_log_likelihood = %1.4f" % (expected_log_likelihood / len(samples)))
        print("estimate_prob_coin_r = %1.4f (actual = %1.4f)" % (estimate_prob_coin_r, prob_coin_r))
        print("estimate_prob_head_r = %1.4f (actual = %1.4f)" % (estimate_prob_head_r, prob_head_r))
        print("estimate_prob_head_b = %1.4f (actual = %1.4f)" % (estimate_prob_head_b, prob_head_b))
        if i > 0:
            if expected_log_likelihood - previous_expected_log_likelihood < 0.0001:
                break
        previous_expected_log_likelihood = expected_log_likelihood
    print("number of iterations = %d" % i)
    print("number of coins = %d" % n)
    print("number of times each coin was flipped = %d" % m)
    print("total coin flips = %d" % (m * n))
    print("Note: To rerun use ./hidden_coins_example_hint.py %1.4f %1.4f %1.4f %d %d" % (
        prob_coin_r, prob_head_r, prob_head_b, n, m))
