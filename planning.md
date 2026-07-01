# Project 4 Planning - Provenance Guard

## Project Idea

The goal of this project is to build an API that estimates whether submitted writing is more likely to be human written or AI generated. Instead of relying on one detector, the system will combine two different detection signals into one confidence score. It will also return a transparency label, store every result in an audit log, and allow creators to appeal a classification.

---

## Detection Signals

### Signal 1: Groq Language Model

The first signal will come from the Groq language model.

It will look at:

- writing style
- wording
- tone
- sentence flow
- overall coherence

This signal should do a good job understanding the writing as a whole, but it may mistake very polished human writing for AI generated writing.

---

### Signal 2: Stylometric Heuristics

The second signal will be calculated using Python.

The heuristics will include:

- vocabulary diversity
- average sentence length
- sentence length variation
- punctuation density

This signal focuses on writing structure instead of meaning. It may not work as well for poetry, creative writing, or very short submissions.

---

## Combining Signals

The final confidence score will combine both signals.

Current plan:

- Groq Score = 65%
- Stylometric Score = 35%

The Groq score receives more weight because it evaluates the overall writing, while the heuristic score provides a second opinion based on measurable writing patterns.

---

## Confidence Levels

The confidence score will be divided into three ranges.

| Score | Result |
|--------|--------|
| 0.00 – 0.35 | Likely Human |
| 0.36 – 0.69 | Uncertain |
| 0.70 – 1.00 | Likely AI |

Using ranges instead of a simple yes or no makes it easier to communicate uncertainty.

---

## Transparency Labels

### Likely AI

> "This content appears likely to have been generated or heavily assisted by AI. Because automated detection can be imperfect, creators may appeal this label."

### Likely Human

> "This content appears likely to have been written by a human. No AI generated attribution label is currently being applied."

### Uncertain

> "We could not confidently determine whether this content was AI generated or human written. This label is shown to avoid making an unfair or unsupported claim."

---

## Appeals Workflow

If a creator disagrees with a result, they can submit an appeal.

Planned workflow:

```
POST /appeal → Receive Content ID + Creator Reasoning → Find Submission → Update Status to under_review → Record Appeal → Return Confirmation
```

The original submission will stay in the audit log while the appeal is recorded as a separate event.

---

## Edge Cases

### Edge Case 1

A very short submission may not contain enough information for the heuristic calculations. In this case, the confidence score should stay lower instead of making a strong claim.

### Edge Case 2

A human writer may submit very formal writing that resembles AI generated text. Using two different signals helps reduce the chance of an incorrect classification, and the appeals workflow allows the creator to challenge the result.

---

## Audit Log

Each log entry should store:

- Timestamp
- Content ID
- Creator ID
- Attribution Result
- Confidence Score
- Groq Score
- Heuristic Score
- Status

Appeals will also be stored in the audit log so the complete history of a submission can be reviewed.

---

## API Endpoints

### POST /submit

Receives submitted text and returns:

- Attribution Result
- Confidence Score
- Transparency Label
- Individual Signal Scores

### POST /appeal

Receives a content ID and creator reasoning, updates the submission to **under_review**, and records the appeal.

### GET /log

Returns all audit log entries.

---

## AI Tool Plan

Claude will be used during implementation to help with the API connection and to fix issues for the functions required by the project.

Planned uses include:

- Creating the initial Flask API routes
- Connecting the Groq API
- Reviewing confidence score calculations
- Checking that the API responses match the project specification
