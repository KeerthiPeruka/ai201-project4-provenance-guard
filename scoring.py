"""Confidence scoring: combine the two signal scores into one confidence
value, and map that confidence to an attribution category.
"""


def combine_scores(groq_score, heuristic_score):
    return round((0.65 * groq_score) + (0.35 * heuristic_score), 2)


def get_attribution(confidence):
    if confidence >= 0.70:
        return "likely_ai"
    elif confidence <= 0.35:
        return "likely_human"
    else:
        return "uncertain"