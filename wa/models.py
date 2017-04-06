# Models for word alignment


def cut_token(arg):
    n = 5

    if isinstance(arg, str):
        return arg[:n]
    elif isinstance(arg, list):
        return [cut_token(tok) for tok in arg]
    elif isinstance(arg, tuple):
        return (cut_token(tok) for tok in arg)
    else:
        return arg


def cut_tokens(func):

    def modified_function(*args, **kwargs):
        return func(*cut_token(args), **kwargs)
    return modified_function


class TranslationModel:
    "Models conditional distribution over trg words given a src word."

    def __init__(self, src_corpus, trg_corpus):
        self._src_trg_counts = {} # Statistics
        self._trg_given_src_probs = {} # Parameters

    @cut_tokens
    def get_conditional_prob(self, src_token, trg_token):
        "Return the conditional probability of trg_token(f_j) given src_token(e_i)."
        if src_token not in self._trg_given_src_probs:
            return 1.0
        if trg_token not in self._trg_given_src_probs[src_token]:
            return 1.0
        return self._trg_given_src_probs[src_token][trg_token]

    @cut_tokens
    def collect_statistics(self, src_tokens, trg_tokens, posterior_matrix):
        "Accumulate fractional alignment counts from posterior_matrix."
        assert len(posterior_matrix) == len(trg_tokens)
        for posterior in posterior_matrix:
            assert len(posterior) == len(src_tokens)
        for i, src in enumerate(src_tokens):
            self._src_trg_counts.setdefault(src, {})
            for j, trg in enumerate(trg_tokens):
                self._src_trg_counts[src][trg] = self._src_trg_counts[src].get(trg, 0) + posterior_matrix[j][i]

    def recompute_parameters(self):
        "Reestimate parameters from counts then reset counters"
        self._trg_given_src_probs = {}
        for src, trg_val in self._src_trg_counts.items():
            norm_const = sum(trg_val.values())
            self._trg_given_src_probs[src] = {trg: val / norm_const for trg, val in trg_val.items()}
        self._src_trg_counts = {}

class PriorModel:
    "Models the prior probability of an alignment given only the sentence lengths and token indices."

    def __init__(self, src_corpus, trg_corpus):
        "Add counters and parameters here for more sophisticated models."
        self._distance_counts = {}
        self._distance_probs = {}

    def get_prior_prob(self, src_index, trg_index, src_length, trg_length):
        "Returns a uniform prior probability."
        if (src_length, trg_length) not in self._distance_probs:
            return 1.0 / src_length
        self._distance_probs[(src_length, trg_length)].setdefault(trg_index, [1.0 / src_length] * src_length)
        return self._distance_probs[(src_length, trg_length)][trg_index][src_index]

    def collect_statistics(self, src_length, trg_length, posterior_matrix):
        "Extract the necessary statistics from this matrix if needed."
        assert len(posterior_matrix) == trg_length
        for posterior in posterior_matrix:
            assert len(posterior) == src_length
        current = self._distance_counts.setdefault((src_length, trg_length), {})
        for j in range(trg_length):
            prob = current.setdefault(j, [0] * src_length)
            for i in range(src_length):
                prob[i] += posterior_matrix[j][i]

    def recompute_parameters(self):
        "Reestimate the parameters and reset counters."
        self._distance_probs = {}
        for src_length, trg_length in self._distance_counts.keys():
            self._distance_probs[(src_length, trg_length)] = {}
            current = self._distance_counts[(src_length, trg_length)]
            for j in range(trg_length):
                prob = current[j]
                norm_const = sum(prob)
                self._distance_probs[(src_length, trg_length)][j] = [pr / norm_const for pr in prob]
        self._distance_counts = {}
