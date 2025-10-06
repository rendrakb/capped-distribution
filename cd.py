from pprint import pprint

def cap_and_redistribute(weights, cap=0.09):
    import numpy as np
    weights = np.array(weights, dtype=float)
    total = weights.sum()
    if not np.isclose(total, 1.0):
        weights /= total

    indexed = list(enumerate(weights))
    indexed.sort(key=lambda x: x[1], reverse=True)

    capped = dict()

    i = 0
    while i < len(indexed):
        idx, w = indexed[i]
        if w <= cap:
            break

        capped[idx] = cap
        excess = w - cap
        remaining = indexed[i+1:]
        if not remaining:
            break
        total_remaining = sum(wt for _, wt in remaining)
        redistributed = [(j, wt + excess * (wt / total_remaining)) for j, wt in remaining]
        indexed = indexed[:i+1] + redistributed
        indexed[i+1:] = sorted(indexed[i+1:], key=lambda x: x[1], reverse=True)
        i += 1

    final = np.zeros(len(weights))
    for idx, w in indexed:
        if idx not in capped:
            capped[idx] = w
    for idx, w in capped.items():
        final[idx] = w
    final /= final.sum()
    return final.tolist()

weights = [ #example
    0.15, 0.12, 0.11,
    0.08, 0.07, 0.06, 0.05, 0.04, 0.03,
    0.025, 0.025, 0.02, 0.02, 0.02,
    0.015, 0.015, 0.015,
    0.01, 0.01, 0.01,
    0.008, 0.008, 0.008, 0.008, 0.008,
    0.007, 0.007, 0.007, 0.007,
    0.006, 0.006, 0.006, 0.006, 0.006,
    0.005, 0.005, 0.005, 0.005, 0.005,
    0.004, 0.004, 0.004, 0.004, 0.004,
    0.003, 0.003, 0.003, 0.003, 0.003,
    0.002, 0.002, 0.002, 0.002, 0.002,
    0.001, 0.001, 0.001, 0.001, 0.001,
    0.0008, 0.0008, 0.0008, 0.0008,
    0.0006, 0.0006, 0.0006,
    0.0005, 0.0005, 0.0005, 0.0005,
    0.0004, 0.0004, 0.0004, 0.0004,
    0.0003, 0.0003, 0.0003, 0.0003
]
total = sum(weights)
weights = [w/total for w in weights]

capped_weights = cap_and_redistribute(weights, cap=0.09)

pprint([round(w, 4) for w in capped_weights])
