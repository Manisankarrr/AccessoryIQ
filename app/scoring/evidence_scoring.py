def score_accessory(spec_ok, review_hits, complaints):
    if not spec_ok:
        return 0.0

    score = (review_hits * 0.3) + 0.5
    score -= complaints * 0.4
    return max(0.0, min(score, 1.0))
