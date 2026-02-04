# Quick Start Guide: Processing 500MB PubMed Data

## Overview
Process large-scale PubMed datasets (500MB = ~100,000-200,000 papers) to analyze gendered innovations in comorbidity research.

---

## Step 1: Prepare Your Data

### Download from PubMed
1. Go to: https://pubmed.ncbi.nlm.nih.gov/
2. Search: `"Comorbidity"[MeSH]`
3. Click "Send to" → "File" → Format: "MEDLINE"
4. Save as: `pubmed_comorbidity.txt`

### Verify Your File
```bash
# Check file size
ls -lh pubmed_comorbidity.txt

# Preview first few entries
head -n 50 pubmed_comorbidity.txt
```

Expected format:
```
PMID- 1234567
TI  - Study title here
AU  - Author Name
MH  - Comorbidity
...
```

---

## Step 2: Run the Main Analysis

### Basic Usage
```bash
python3 process_large_dataset.py pubmed_comorbidity.txt
```

### What Happens
1. **Parsing** (~5-10 min for 500MB)
   - Reads file line by line (memory efficient)
   - Identifies comorbidity papers
   - Progress updates every 1,000 entries

2. **Gender Inference** (automatic)
   - Extracts author first names
   - Matches against name database
   - Classifies teams: all-male, all-female, mixed, unknown

3. **Analysis** (automatic)
   - Temporal trends by team type
   - Novel disease combination detection
   - Team composition metrics

4. **Output** (saved to `./analysis_output/`)
   - `final_report.json` - Complete statistics
   - `checkpoint_*.pkl` - Recovery files (can delete after)

### Expected Console Output
```
==================================================================
GENDERED INNOVATIONS ANALYSIS - BATCH PROCESSING
==================================================================

Starting to parse pubmed_comorbidity.txt
This may take 5-10 minutes for 500MB file...
  Processed 1,000 entries, found 892 comorbidity papers...
  Processed 2,000 entries, found 1,784 comorbidity papers...
  ...
  Processed 100,000 entries, found 89,234 comorbidity papers...

✓ Parsing complete!
  Total entries: 100,000
  Comorbidity studies: 89,234

→ Processing batch 1 (1000 papers)...
  ✓ Batch 1 complete. Checkpoint saved.
...
→ Processing batch 89 (1000 papers)...
  ✓ Batch 89 complete. Checkpoint saved.

Generating final report...

==================================================================
FINAL RESULTS SUMMARY
==================================================================

Dataset Overview:
  Total papers analyzed: 89,234
  Year range: 1980 - 2024

Team Composition:
  All-male teams:       48,456 (54.3%)
  All-female teams:      8,923 (10.0%)
  Mixed-gender teams:   28,567 (32.0%)
  Unknown:               3,288 ( 3.7%)

Novelty Analysis:
  Total novel disease combinations discovered: 4,567
  Discoveries by team type:
    all_male       :  2,145 (47.0%)
    all_female     :    456 (10.0%)
    mixed          :  1,897 (41.5%)

  💡 Mixed-gender teams represent 32.0% of papers
     but discovered 41.5% of novel combinations
     → 1.30× enrichment in novel discoveries! ⭐

✓ Analysis complete!
  Results saved to: ./analysis_output/
```

---

## Step 3: Generate Visualizations

```bash
python3 generate_visualizations.py
```

### Output Files (in `./analysis_output/figures/`)
1. **team_composition.png** - Pie chart of team types
2. **temporal_trends.png** - Trends over time (2 panels)
3. **novelty_comparison.png** - Novel discoveries by team type
4. **top_combinations.png** - Heatmap of disease combinations
5. **summary_dashboard.png** - Comprehensive overview

---

## Understanding the Results

### Key Metrics to Look For

**1. Team Composition**
- What % are mixed-gender teams?
- How has this changed over time?

**2. Novelty Enrichment**
```
If mixed teams = X% of papers
but discover Y% of novel combinations
→ Enrichment = Y/X

Example: 32% of papers, 41.5% of discoveries → 1.30× enrichment
```

**3. Temporal Trends**
- When did mixed teams become more common?
- Does research diversification coincide with increased female participation?

**4. Disease Combinations**
- Which combinations are dominated by which team types?
- Are certain categories (women's health, mental health) more studied by diverse teams?

---

## Advanced Analysis

### Check Specific Years
```python
import json

with open('./analysis_output/final_report.json', 'r') as f:
    report = json.load(f)

# Look at 2020 data
year_2020 = report['temporal_trends']['2020']
print(f"2020 Papers: {year_2020['total']}")
print(f"Mixed teams: {year_2020['mixed']}")
print(f"Percentage: {100*year_2020['mixed']/year_2020['total']:.1f}%")
```

### Extract Novel Combinations
```python
# Find combinations first discovered by mixed teams
mixed_discoveries = [
    combo for combo, data in report['novelty_analysis']['first_discoveries'].items()
    if data['team_type'] == 'mixed'
]

print(f"Mixed teams discovered {len(mixed_discoveries)} novel combinations")
```

### Export for Further Analysis
```python
import pandas as pd

# Convert to DataFrame for statistical analysis
temporal_data = []
for year, data in report['temporal_trends'].items():
    temporal_data.append({
        'year': int(year),
        'total': data['total'],
        'mixed': data['mixed'],
        'mixed_pct': 100 * data['mixed'] / data['total'] if data['total'] > 0 else 0
    })

df = pd.DataFrame(temporal_data)
df.to_csv('temporal_analysis.csv', index=False)

# Now you can do:
# - Regression analysis
# - Trend detection
# - Correlation studies
```

---

## Performance Tips

### For Very Large Files (>500MB)
1. **Increase batch size** for faster processing:
   ```python
   analyzer.process_dataset(filepath, batch_size=5000)  # default is 1000
   ```

2. **Use PyPy** for 2-3× speedup:
   ```bash
   pypy3 process_large_dataset.py pubmed_comorbidity.txt
   ```

3. **Process in chunks** if memory limited:
   ```bash
   # Split file first
   split -l 50000 pubmed_comorbidity.txt chunk_
   
   # Process each chunk
   python3 process_large_dataset.py chunk_aa
   python3 process_large_dataset.py chunk_ab
   # ... merge results after
   ```

### Recovery from Crashes
If processing crashes:
1. Check `./analysis_output/` for checkpoint files
2. Last checkpoint shows how far you got
3. Can resume by modifying code to skip processed batches

---

## Common Issues

### Issue: "File not found"
**Solution:** Provide full path
```bash
python3 process_large_dataset.py /Users/yourname/Downloads/pubmed_comorbidity.txt
```

### Issue: "Memory error"
**Solution:** Increase batch size or process in chunks (see above)

### Issue: "Gender inference is poor"
**Solution:** The built-in name database covers common Western names. For better accuracy:
1. Use external API (genderize.io) - requires modification
2. Add names to `_load_female_names()` and `_load_male_names()`
3. Manual verification of high-impact papers

### Issue: "Too many 'unknown' teams"
**Reasons:**
- Authors using initials only (common in older papers)
- Non-Western names not in database
- Ambiguous names

**Not necessarily a problem:** Focus on known-gender papers for main analysis

---

## Expected Results (Hypotheses)

Based on Yang et al. (2022), expect to find:

✓ **Mixed teams discover 10-25% more novel combinations** (relative to their proportion)

✓ **Temporal increase:** Mixed teams growing from 15% (1980s) to 35-40% (2020s)

✓ **Specific patterns:**
  - Women's health comorbidities increase post-2000
  - Mental health + physical disease more studied by mixed teams
  - Inverse comorbidities (protective effects) 2-3× more in mixed teams

---

## Next Steps After Analysis

### 1. Statistical Testing
- Chi-square: Team type × Novelty
- Logistic regression: Predict novelty from gender balance
- Time series: Trend analysis

### 2. Deep Dives
- Pick top 10 novel discoveries by mixed teams
- Review abstracts for qualitative insights
- Identify breakthrough papers

### 3. Comparison to Other Fields
- Run same analysis on different MeSH terms
- Compare comorbidity to cardiovascular, oncology, etc.
- Test if patterns generalize

### 4. Publication
- Write up methods and results
- Compare to Yang et al. (2022) findings
- Submit to journals focusing on meta-research

---

## Files Summary

**Processing:**
- `process_large_dataset.py` - Main analysis engine (USE THIS FIRST)

**Visualization:**
- `generate_visualizations.py` - Creates all figures (RUN AFTER PROCESSING)

**Reference:**
- `research_protocol.md` - Detailed methodology (40+ pages)
- `README.md` - Overview and context

**Interactive:**
- `knowledge_graph.html` - Interactive visualization (open in browser)
- `knowledge_graph_structure.html` - Detailed concept map (open in browser)

---

## Time Estimates

| Dataset Size | Entries | Processing Time | Memory Usage |
|-------------|---------|-----------------|--------------|
| 100 MB      | ~20,000 | 2-3 minutes     | <1 GB        |
| 500 MB      | ~100,000| 10-15 minutes   | ~2 GB        |
| 1 GB        | ~200,000| 20-30 minutes   | ~3 GB        |

*Times on standard laptop (2020+), varies by CPU*

---

## Support

If you encounter issues:
1. Check file format matches MEDLINE expected format
2. Verify Python 3.7+ installed
3. Review error messages carefully
4. Check `./analysis_output/` for partial results

---

## Citation

If you use this analysis in your research:

**Original Framework:**
Yang, Y., Tian, T. Y., Woodruff, T. K., Jones, B. F., & Uzzi, B. (2022). 
Gender-diverse teams produce more novel and higher-impact scientific ideas. 
Proceedings of the National Academy of Sciences, 119(36), e2200841119.

**Your Analysis:**
[Your name]. (2026). Gendered innovations in comorbidity research: 
An analysis of 100,000+ PubMed papers. [Details]

---

**Ready to discover how gender diversity drives innovation in comorbidity research!** 🚀
