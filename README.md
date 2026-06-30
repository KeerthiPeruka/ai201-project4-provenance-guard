# AI201 Project 4 - Provenance Guard

## Project Overview

Provenance Guard is a Flask API that analyzes submitted text and estimates whether it is more likely to be human written or AI generated. Instead of relying on a one detector, the project combines two different detection signals into one confidence score and returns a transparency label that explains the result. The project also includes an audit log, an appeals workflow, and rate limiting.

---

## Project Structure

```text
ai201-project4-provenance-guard/
│
├── .venv/
├── .env
├── .gitignore
├── app.py
├── detection.py
├── labels.py
├── planning.md
├── README.md
├── requirements.txt
├── scoring.py
└── storage.py
```

---

## System Workflow

### Content Submission

```text
POST /submit → Receive Text + Creator ID → Run Groq Detection → Run Stylometric Heuristics → Combine Scores → Calculate Confidence Score → Generate Transparency Label → Save to Audit Log → Return JSON Response
```

### Appeals Workflow

```text
POST /appeal → Receive Content ID + Creator Reasoning → Find Original Submission → Update Status to under_review → Save Appeal to Audit Log → Return Confirmation
```

---

## Detection Signals

### Groq Language Model

The Groq model looks at the writing as a whole. It considers the wording, tone, writing style, and how the ideas connect.

**Measures**
- Overall writing style
- Tone
- Language patterns
- Semantic coherence

**Limitations**
- Highly polished human writing can sometimes look AI generated.
- AI generated writing that has been heavily edited may appear more human.

### Stylometric Heuristics

The second signal is calculated using Python.

Features include:
- Vocabulary diversity
- Average sentence length
- Sentence length variation
- Punctuation density

**Measures**

This signal focuses on structural writing characteristics instead of meaning.

**Limitations**
- Poetry
- Very short submissions
- Repetitive creative writing

Using both signals provides a more balanced result than relying on only one detector.

---

## Confidence Scoring

The final confidence score is calculated using:

- 65% Groq score
- 35% Stylometric score

### Confidence Ranges

| Score | Result |
|--------|--------|
| 0.00 – 0.35 | Likely Human |
| 0.36 – 0.69 | Uncertain |
| 0.70 – 1.00 | Likely AI |

### Validation

Different writing samples were tested to verify that the scores changed appropriately.

Example 1
- Groq Score: 0.20
- Heuristic Score: 0.30
- Confidence Score: 0.23
- Result: Likely Human

Example 2
- Groq Score: 0.80
- Heuristic Score: 0.30
- Confidence Score: 0.62
- Result: Uncertain

---

## Transparency Labels

**Likely AI**

> "This content appears likely to have been generated or heavily assisted by AI. Because automated detection can be imperfect, creators may appeal this label."

**Likely Human**

> "This content appears likely to have been written by a human. No AI generated attribution label is currently being applied."

**Uncertain**

> "We could not confidently determine whether this content was AI generated or human written. This label is shown to avoid making an unfair or unsupported claim."

---

## Appeals Workflow

Creators can submit an appeal by providing a content ID and a short explanation. The API updates the submission status to `under_review` and records the appeal in the audit log.

---

## Rate Limiting

The `/submit` endpoint is limited to:

- 10 requests per minute
- 100 requests per day

These limits are intended to reflect normal usage while helping prevent spam or automated abuse.

### Test Results

```text
200
200
200
200
200
200
200
200
200
200
429
429
```

---

## Audit Log

Every submission and appeal is stored in a structured JSON audit log.

Each entry includes:
- Timestamp
- Content ID
- Creator ID
- Attribution Result
- Confidence Score
- Groq Score
- Heuristic Score
- Status

---

## API Endpoints

### POST /submit

Returns:
- Attribution result
- Confidence score
- Transparency label
- Individual signal scores
- Content ID

### POST /appeal

Accepts a content ID and creator reasoning, updates the status to `under_review`, and records the appeal.

### GET /log

Returns all audit log entries as structured JSON.

---

## Known Limitations

The system estimates whether content is AI generated, but it is not intended to provide perfect detection.

Possible misclassifications include:
- Highly polished human writing
- Poetry
- Very short submissions
- AI generated writing that has been heavily edited

Confidence scores and the appeals workflow help account for these limitations.

---

## Spec Reflection

The original plan considered using a database for storage. During implementation, in memory storage was used instead because it simplified development while still supporting the required submission, logging, and appeals workflow.

---

## AI Usage

Claude was used for generating the initial Flask routes and Groq integration. The generated code was then revised to match the planned API responses and confidence scoring.

A second use was brainstorming stylometric heuristics. The final implementation kept vocabulary diversity, sentence length, sentence length variation, and punctuation density while adjusting the confidence thresholds after testing.

---

## Installation

```bash
git clone <your-github-repository>

cd ai201-project4-provenance-guard

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
python app.py
```

---

## Technologies Used

- Python
- Flask
- Groq API
- Flask-Limiter
- Python Dotenv
- JSON
- UUID
