"""Transparency label generation: maps an attribution category to the exact
plain-language text shown to a reader on the platform.
"""


def get_label(attribution):
    if attribution == "likely_ai":
        return "This content appears likely to have been generated or heavily assisted by AI. Because automated detection can be imperfect, creators may appeal this label."

    if attribution == "likely_human":
        return "This content appears likely to have been written by a human. No AI-generated attribution label is currently being applied."

    return "We could not confidently determine whether this content was AI-generated or human-written. This label is shown to avoid making an unfair or unsupported claim."