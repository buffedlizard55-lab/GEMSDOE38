"""Locked CPU benchmark and deterministic sparse emission; no prior predictions as inputs."""

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier


def fit_model(X, y, train, columns, seed=38):
    rng = np.random.default_rng(seed)
    pos = train[y[train] == 1]
    neg = train[y[train] == 0]
    sel = np.concatenate(
        [pos, rng.choice(neg, size=min(200000, len(neg)), replace=False)]
    )
    rng.shuffle(sel)
    xx = np.asarray(X[sel][:, columns]).copy()
    median = np.nanmedian(xx, axis=0)
    if not np.isfinite(median).all():
        raise ValueError("Empty training band")
    xx = np.where(np.isfinite(xx), xx, median)
    model = HistGradientBoostingClassifier(
        max_iter=120,
        max_leaf_nodes=15,
        max_bins=127,
        min_samples_leaf=60,
        learning_rate=0.07,
        l2_regularization=10,
        early_stopping=False,
        random_state=seed,
    )
    model.fit(xx, y[sel])
    return (
        model,
        median,
        {
            "train_pool": len(train),
            "sampled_train": len(sel),
            "sampled_positive": len(pos),
            "negative_sampling": "uniform w/o replacement; probabilities not calibrated to true prevalence",
        },
    )


def predict(model, median, X, indices, columns):
    out = np.empty(len(indices), dtype=np.float32)
    for i in range(0, len(indices), 50000):
        xx = np.array(X[indices[i : i + 50000]][:, columns])
        xx = np.where(np.isfinite(xx), xx, median)
        out[i : i + len(xx)] = model.predict_proba(xx)[:, 1]
    return out


def thin(scores, ys, xs, shape, budget, separation=2.8):
    if budget < 0:
        raise ValueError("Negative budget")
    output = np.zeros(shape, dtype=np.float32)
    occupied = np.zeros(shape, dtype=bool)
    order = np.argsort(-scores, kind="stable")  # row-major tie-break, reproducible
    offsets = [
        (dy, dx)
        for dy in range(-3, 4)
        for dx in range(-3, 4)
        if dy * dy + dx * dx < separation**2
    ]
    count = 0
    if budget == 0:
        return output
    for k in order:
        if not np.isfinite(scores[k]) or scores[k] <= 0:
            continue
        y, x = int(ys[k]), int(xs[k])
        if occupied[y, x]:
            continue
        output[y, x] = 1
        count += 1
        for dy, dx in offsets:
            yy, xx = y + dy, x + dx
            if 0 <= yy < shape[0] and 0 <= xx < shape[1]:
                occupied[yy, xx] = True
        if count >= budget:
            break
    return output
