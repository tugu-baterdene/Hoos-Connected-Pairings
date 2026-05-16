# Hoos Connected Pairing System

An intelligent facilitator pairing platform built for Hoos Connected @ UVA.

This system automates facilitator pairings using optimization algorithms that account for:

- Shared availability
- Facilitation experience
- Confidence balancing
- Weighted compatibility scoring

The goal is to reduce the manual overhead of pairing facilitators while creating stronger and more balanced teams.

---

# Features

- CSV upload interface
- FastAPI web dashboard
- Maximum-weight matching algorithm using graph optimization
- Configurable optimization weights
- Pairing explainability
- Shared availability detection
- CSV export of generated pairings
- Modern responsive UI

---

# Pairing Logic

The system computes compatibility scores between every possible pair of facilitators.

Compatibility is based on:

| Factor | Description |
|---|---|
| Availability Overlap | Number of shared time slots |
| Experience Balance | Rewards pairing experienced facilitators with newer ones |
| Confidence Difference | Encourages balancing high-confidence facilitators with lower-confidence facilitators |

The algorithm then uses:

```text
Maximum Weight Matching
```

to compute globally optimal pairings across all facilitators.

This ensures the best overall pairing configuration rather than greedy local matches.

---

# Tech Stack

- Python
- FastAPI
- Jinja2
- NetworkX
- SQLite database
- HTML/CSS
- CSV-based data pipeline

---

# Project Structure

```text
Hoos-Connected-Pairings/
│
├── app/
|   ├── __init__.py
│   ├── main.py
│   ├── pairing_logic.py
|   ├── config.py
|   ├── database.py
│   ├── csv_loader.py
│   └── csv_writer.py
│
├── data/
|   └── facilitators.db
|
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
│   ├── style.css
│   └── hero.png
│
├── uploads/
├── output/
├── tests/
│   └── test_pairing.py
│
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd Hoos-Connected-Pairings
```

Install dependencies:

```bash
pip install fastapi uvicorn jinja2 python-multipart networkx
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open in browser:

```text
http://127.0.0.1:8000
```

---

# CSV Format

Input CSV files should follow this structure:

```csv
student_id,name,facilitated_before,confidence,Monday,Tuesday,Wednesday,Thursday,Friday
a,Alice,True,9,"6PM;7PM","6PM","7PM","6PM;8PM","5PM"
b,Bob,False,3,"7PM","6PM;7PM","7PM","8PM","5PM;6PM"
```

---

# Optimization Weights

Users can dynamically adjust:
- Availability Weight
- Experience Weight
- Confidence Weight

This allows the pairing strategy to be customized depending on program goals.

---

# Explainability Features

Each generated pairing includes:
- Shared meeting times
- Experience balancing details
- Confidence gap
- Score breakdown

This improves transparency and trust in the pairing process.

---

# Future Improvements

Planned features include:

- Google Sheets/API integration
- Real-time schedule updates
- Hard pairing constraints
- Unpaired facilitator analysis
- Graph visualizations
- Pairing history tracking
- Admin dashboard
- Authentication system

---

# Motivation

Hoos Connected historically handled pairings manually, which became difficult as:
- schedules changed frequently
- facilitator counts increased
- balancing experience became more important

This project aims to create a scalable and intelligent solution that improves both efficiency and pairing quality.

---

# Author

Built by Tugu Baterdene for Hoos Connected @ UVA.