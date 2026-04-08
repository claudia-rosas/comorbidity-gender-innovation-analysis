#!/usr/bin/env python3
"""
Run BatchAnalyzer directly from comorbidity_all.json.gz
Skips re-parsing the MEDLINE txt — uses pre-structured data.
"""

import json
import gzip
import time
from pathlib import Path
from collections import defaultdict, Counter

from process_large_dataset import BatchAnalyzer, Publication


def load_json_gz(filepath: str):
    """Stream papers from json.gz one at a time to keep memory low"""
    print(f"Loading {filepath}...")
    with gzip.open(filepath, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data):,} papers\n")
    return data


def paper_to_publication(paper: dict) -> Publication:
    """Convert JSON record to Publication dataclass"""
    return Publication(
        pmid=paper.get('pmid', ''),
        year=paper.get('year', 0),
        authors=paper.get('authors', []),
        mesh_terms=paper.get('mesh_terms', []),
        title=paper.get('title', ''),
        abstract=paper.get('abstract', ''),
        journal=paper.get('journal', '')
    )


def run_analysis(json_gz_path: str, output_dir: str = './analysis_output', batch_size: int = 1000):
    start_time = time.time()

    print("\n" + "="*70)
    print("GENDERED INNOVATIONS ANALYSIS - FROM JSON.GZ")
    print("="*70 + "\n")

    papers = load_json_gz(json_gz_path)

    analyzer = BatchAnalyzer(output_dir=output_dir)

    batch = []
    batch_num = 0

    for i, paper in enumerate(papers):
        pub = paper_to_publication(paper)

        # If team_analysis is already in the JSON, use it directly
        team_data = paper.get('team_analysis')
        if team_data:
            team_type = team_data.get('team_type', 'unknown')
            gender_balance = team_data.get('gender_balance')

            # Update yearly stats directly
            year = pub.year
            analyzer.year_stats[year]['total'] += 1
            analyzer.year_stats[year][team_type] += 1

            # Track disease combinations
            diseases = analyzer._extract_diseases(pub.mesh_terms)
            if len(diseases) >= 2:
                combo = tuple(sorted(diseases[:3]))
                combo_str = ' + '.join(combo)

                analyzer.disease_combos[combo_str][team_type].append({
                    'pmid': pub.pmid,
                    'year': pub.year,
                    'title': pub.title[:100]
                })

                if combo_str not in analyzer.novel_combos:
                    analyzer.novel_combos[combo_str] = {
                        'year': pub.year,
                        'pmid': pub.pmid,
                        'team_type': team_type,
                        'gender_balance': gender_balance
                    }
        else:
            # Fallback: re-infer gender if team_analysis missing
            batch.append(pub)
            if len(batch) >= batch_size:
                batch_num += 1
                analyzer._process_batch(batch, batch_num)
                batch = []

        if (i + 1) % 5000 == 0:
            print(f"  Processed {i+1:,} papers...")

    # Process any remaining fallback batch
    if batch:
        batch_num += 1
        analyzer._process_batch(batch, batch_num)

    elapsed = time.time() - start_time
    print(f"\n{'='*70}")
    print(f"ANALYSIS COMPLETE in {elapsed/60:.1f} minutes")
    print(f"{'='*70}\n")

    analyzer._generate_final_report()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        json_gz_path = sys.argv[1]
    else:
        json_gz_path = 'data/comorbidity_all.json.gz'

    output_dir = sys.argv[2] if len(sys.argv) > 2 else './analysis_output'

    if not Path(json_gz_path).exists():
        print(f"Error: File not found: {json_gz_path}")
        sys.exit(1)

    run_analysis(json_gz_path, output_dir=output_dir)

    print("\nNext step:")
    print("  python code/generate_visualizations.py")
