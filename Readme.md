# Gendered Innovations in Comorbidity Research

## Research Question

> When a woman enters a research group, does innovation change?  
> Do new topics arise? Do new combinations of comorbidities appear?

This project analyzes 135,688 PubMed comorbidity papers to test whether the addition of women to previously all-male research groups is associated with increased novelty in disease combination discovery.

Theoretical framework: Yang et al. (2022), *PNAS* — gender-diverse teams produce more novel and higher-impact scientific ideas.

---

## Pipeline

### Step 1 — Data Conversion
Convert raw PubMed MEDLINE `.txt` to structured `.json.gz`.

```bash
python code/parse_to_json.py data/comorbidity_all.txt data/comorbidity_all.json.gz
```

**Output:** `data/comorbidity_all.json.gz` (100MB, 135,688 papers)

---

### Step 2 — Name Enrichment *(in development)*
~51% of authors appear with initials only (e.g. `Smith J`). PubMed XML records store full `ForeName` fields — this step queries PubMed by PMID to recover full names, then matches them back using Jaro-Winkler similarity on last name + neighboring author context.

```bash
python code/enrich_author_names.py
```

**Dependencies:** `biopython`, `jellyfish`

> **Constraint:** To be documented after testing.

---

### Step 3 — Gender Inference *(in development)*
Infer gender from recovered full names using a multi-stage approach:
1. `gender-guesser` — free, covers ~45,000 names, reliable for Western names
2. NamSor API (free tier, 2,500/month) — fallback for ambiguous cases

```bash
python code/infer_gender.py
```

> **Constraint:** To be documented after testing.

---

### Step 4 — Analysis from JSON
Run team composition, novelty, and comorbidity analysis directly from `.json.gz`.

```bash
python code/analyze_from_json.py data/comorbidity_all.json.gz
```

**Output:** `analysis_output/final_report.json`

---

### Step 5 — Research Group Detection *(in development)*
Cluster recurring co-authors into stable research groups using co-authorship networks. Groups are defined as connected components across a sliding time window (minimum 3 papers together).

```bash
python code/detect_research_groups.py
```

> **Constraint:** To be documented after testing.

---

### Step 6 — Event Detection *(in development)*
Identify "treatment events": research groups that were all-male for ≥3 years before a woman joined.

```bash
python code/detect_entry_events.py
```

> **Constraint:** To be documented after testing.

---

### Step 7 — Innovation Measurement *(in development)*
For each group, compare output before vs. after the entry event:
- New MeSH combinations never used by that group before
- New comorbidity pairs/triplets
- Breadth of disease topics

```bash
python code/measure_innovation.py
```

> **Constraint:** To be documented after testing.

---

### Step 8 — Statistical Analysis *(in development)*
Difference-in-differences design:
- **Treatment group:** groups that added a woman
- **Control group:** all-male groups that never added a woman
- **Test:** do treated groups show more innovation post-entry, controlling for group size?

```bash
python code/statistical_analysis.py
```

> **Constraint:** To be documented after testing.

---

### Step 9 — Visualizations
Generate all figures from `final_report.json`.

```bash
python code/generate_visualizations.py
```

**Output:** `analysis_output/figures/` — 5 publication-quality figures.

---

## Known Constraints

> This section will be populated with validated limitations as each pipeline step is tested.

- [ ] Step 2: Name enrichment coverage rate (% of initials resolved)
- [ ] Step 3: Gender inference accuracy and unknown rate after enrichment
- [ ] Step 5: Research group detection — minimum group size threshold
- [ ] Step 6: Event detection — number of qualifying treatment events found
- [ ] Step 7: Innovation measurement — baseline novelty rate
- [ ] Step 8: Statistical power — sample size of treatment vs. control groups

---

## Repository Structure

```
ComorbidityAnalysis/
├── code/
│   ├── parse_to_json.py            # Step 1: MEDLINE → JSON.gz
│   ├── analyze_from_json.py        # Step 4: Analysis from JSON
│   ├── generate_visualizations.py  # Step 9: Figures
│   ├── process_large_dataset.py    # Core analysis engine
│   ├── inspect_json.py             # Dataset inspection utility
│   └── debug_json.py               # Debugging utility
├── data/
│   └── comorbidity_all.json.gz     # Main dataset (not tracked in git)
├── analysis_output/
│   ├── final_report.json           # Analysis results
│   └── figures/                    # Generated visualizations
├── methodology_study_guide.md      # Methodology explained for study
└── README.md                       # This file
```

---

## Data

- **Source:** PubMed MEDLINE, search term `"Comorbidity"[MeSH]`
- **Size:** 135,688 papers, 862,962 unique authors
- **Year range:** to be confirmed after analysis
- **Format:** `.json.gz` (structured, compressed)
- **Not tracked in git:** raw `.txt`, `.json.gz`, `.7z` files (see `.gitignore`)

---

## Dependencies

```bash
pip install biopython gender-guesser jellyfish matplotlib seaborn numpy
```

---

## Reference

Yang, Y., Tian, T. Y., Woodruff, T. K., Jones, B. F., & Uzzi, B. (2022).
Gender-diverse teams produce more novel and higher-impact scientific ideas.
*Proceedings of the National Academy of Sciences*, 119(36), e2200841119.

---

## Contact

Claudia Rosas Mendoza — claudia.rosas@bsc.es
