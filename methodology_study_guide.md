# Methodology: Gendered Innovations in Comorbidity Research

## 1. Data Source
Papers are downloaded from **PubMed** in **MEDLINE format** — a structured plain-text format where each field has a 4-letter code (`TI` = title, `AU` = author, `MH` = MeSH term, etc.). The dataset targets comorbidity research by filtering papers that either:
- Have `Comorbidity` as a MeSH term, or
- Contain words like *comorbidity*, *multimorbidity* in title/abstract

---

## 2. Gender Inference
Since PubMed doesn't store author gender, it's **inferred from first names**:

1. Author names are in `LastName, FirstName` format
2. The first name is extracted and lowercased
3. Matched against curated lists of female/male names
4. Heuristic fallback: names ending in `'a'` (e.g. *Maria*, *Elena*) → classified Female
5. Result per author: `F`, `M`, or `U` (unknown)

**Limitation:** Works best for Western names. Non-Western names (Asian, Arabic, etc.) often return `U` (unknown).

---

## 3. Team Classification
Each paper's author list is classified into one of four **team types**:

| Team Type | Definition |
|-----------|-----------|
| `all_male` | Only male authors |
| `all_female` | Only female authors |
| `mixed` | At least one male + one female |
| `unknown` | All authors are gender-unknown |

Additional metrics per paper:
- **gender_balance**: `female_count / (female + male)` → ranges 0.0–1.0
- **first_author_gender**: proxy for who led the work
- **last_author_gender**: proxy for senior/PI authorship

---

## 4. Disease Combination Extraction
From each paper's MeSH terms, **disease combinations** are extracted by:
1. Removing demographic/methodological terms (`Female`, `Male`, `Humans`, `Adult`, `Comorbidity`, etc.)
2. Removing MeSH qualifiers (e.g. `Diabetes Mellitus/complications` → `Diabetes Mellitus`)
3. Taking up to 3 diseases and sorting them alphabetically → creates a **combo key**

Example: `Depression + Diabetes Mellitus + Hypertension`

---

## 5. Novelty Detection
A disease combination is **novel** the first time it appears in the dataset (chronologically by year). The script tracks:
- Which team type made the **first publication** on each combination
- The year of first discovery
- The gender balance of that pioneering team

This is the core innovation metric: *do mixed-gender teams disproportionately pioneer new disease combinations?*

---

## 6. Key Output Metrics

**Team composition** — overall and by year:
- What % of comorbidity research is done by mixed vs. all-male teams?
- Has this changed over time (1980s → 2020s)?

**Novelty enrichment** — the main finding:
```
Enrichment = (% of novel discoveries by mixed teams)
           / (% of all papers by mixed teams)

Enrichment > 1.0 → mixed teams discover more than expected
```

**Top disease combinations** — which pairs/triplets are most studied, and by which team type.

---

## 7. Theoretical Framework
Based on **Yang et al. (2022)** (*PNAS*), which found that gender-diverse teams produce more novel and higher-impact science. This project applies that framework specifically to **comorbidity research** in medicine.

The hypothesis: mixed-gender teams bring broader perspectives → more likely to identify unexpected disease connections that single-gender teams miss.
