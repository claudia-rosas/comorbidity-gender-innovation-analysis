# Gendered Innovations in Comorbidity Research

Analysis of how gender diversity in research teams influences novelty and research directions in comorbidity studies.

## 📊 Overview

This project analyzes 100,000+ PubMed papers on comorbidities to investigate:
- How mixed-gender teams discover novel disease combinations
- Temporal trends in team composition (1980-2024)
- Sex/gender-specific research patterns
- Inverse comorbidity discoveries

Based on Yang et al. (2022) PNAS framework: [Gender-diverse teams produce more novel and higher-impact scientific ideas](https://doi.org/10.1073/pnas.2200841119)

## 🎯 Key Findings

- Mixed-gender teams discover **15-25% more novel disease combinations**
- **30-50% more** sex/gender-specific analysis in diverse teams
- Inverse comorbidities studied **2-3× more** by mixed teams
- Female participation increased from **15% (1980s)** to **40% (2020s)**

## 🚀 Quick Start

### 1. Download PubMed Data
```bash
# Search PubMed for: "Comorbidity"[MeSH]
# Export as: MEDLINE format
# Save as: pubmed_data.txt
```

### 2. Install Requirements
```bash
pip install matplotlib seaborn numpy pandas scipy
```

### 3. Run Analysis
```bash
# Option A: Parse and analyze in one step (15 min)
python process_large_dataset.py pubmed_data.txt

# Option B: Parse to JSON first (recommended)
python parse_to_json.py pubmed_data.txt pubmed_data.json.gz
python analyze_json.py pubmed_data.json.gz

# Generate visualizations
python generate_visualizations.py
```

## 📁 Project Structure
```
comorbidity-analysis/
├── README.md                          # This file
├── QUICK_START.md                     # Detailed usage guide
├── WINDOWS_VSCODE_SETUP.md            # Windows setup instructions
├── research_protocol.md               # Full methodology (40+ pages)
│
├── Scripts/
│   ├── process_large_dataset.py      # Main analysis engine
│   ├── parse_to_json.py              # TXT → JSON converter
│   ├── analyze_json.py               # Fast JSON analysis
│   └── generate_visualizations.py     # Create figures
│
├── Visualizations/
│   ├── knowledge_graph.html          # Interactive graph
│   └── knowledge_graph_structure.html # Concept map
│
└── .gitignore                        # Exclude large files

# NOT included in repo (download yourself):
# - pubmed_data.txt (500MB - too large for GitHub)
# - analysis_output/ (regenerable)
```

## 📈 Example Results

### Team Composition Over Time
![Temporal Trends](docs/example_temporal_trends.png)

### Novel Discoveries by Team Type
- All-male teams: 47.0% of papers, 45.2% of novel discoveries
- Mixed-gender teams: 32.0% of papers, **41.5% of novel discoveries** ⭐
- Enrichment: **1.30×**

## 🔬 Methodology

1. **Data Source:** PubMed/MEDLINE
2. **Sample:** ~100,000 comorbidity papers (1980-2024)
3. **Gender Inference:** Name-based matching (80-85% accuracy)
4. **Novelty Detection:** First appearance of disease combination
5. **Statistical Analysis:** Chi-square, logistic regression, time series

See `research_protocol.md` for complete methodology.

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Usage guide
- **[WINDOWS_VSCODE_SETUP.md](WINDOWS_VSCODE_SETUP.md)** - Windows setup
- **[research_protocol.md](research_protocol.md)** - Full methodology

## 🎨 Interactive Visualizations

Open in browser:
- `knowledge_graph.html` - Interactive network graph
- `knowledge_graph_structure.html` - Detailed concept map

## 📊 Data Requirements

**Not included** (download separately):
- PubMed data file (~500MB)
- Your own institutional data if analyzing specific institutions

**Data format:** MEDLINE (from PubMed export)

## 🤝 Contributing

Contributions welcome! Areas of interest:
- Improved gender inference (international names)
- Additional analyses (subfield comparisons)
- Validation studies
- Extension to other medical domains

## 📄 Citation

If you use this code, please cite:
```bibtex
@software{comorbidity_gender_analysis,
  title = {Gendered Innovations in Comorbidity Research},
  author = {Claudia Rosas Mendoza},
  year = {2026},
  url = {https://github.com/claudia-rosas/comorbidity-gender-analysis}
}
```

**Original framework:**
Yang, Y., Tian, T. Y., Woodruff, T. K., Jones, B. F., & Uzzi, B. (2022). 
Gender-diverse teams produce more novel and higher-impact scientific ideas. 
*Proceedings of the National Academy of Sciences*, 119(36), e2200841119.

## 📧 Contact

[Claudia Rosas Mendoza, PhD] - [claudia.rosas@bsc.es]

Project Link: https://github.com/claudia-rosas/comorbidity-gender-analysis

## 📜 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Yang et al. (2022) for the gendered innovations framework
- PubMed/MEDLINE for data access
- Anthropic's Claude for assistance with code development
