#!/usr/bin/env python3
"""
Convert PubMed MEDLINE TXT to structured JSON
Run once, use many times
"""

import json
import gzip
from pathlib import Path
from process_large_dataset import LargePubMedParser, GenderInferenceEngine


def txt_to_json(input_file, output_file, compress=True):
    """
    Convert MEDLINE TXT to JSON
    
    Args:
        input_file: Path to .txt file (e.g., pubmed_data.txt)
        output_file: Path to save JSON (e.g., pubmed_data.json)
        compress: Save as .json.gz to save space (recommended)
    """
    print(f"Converting {input_file} to JSON...")
    print("This will take ~15 minutes for 500MB file\n")
    
    parser = LargePubMedParser()
    gender_engine = GenderInferenceEngine()
    
    papers = []
    
    for pub in parser.parse_file_streaming(input_file):
        # Analyze team composition
        team = gender_engine.analyze_team(pub.authors)
        
        # Extract diseases
        diseases = [
            term.split('/')[0] 
            for term in pub.mesh_terms
            if term.split('/')[0] not in {
                'Female', 'Male', 'Humans', 'Adult', 'Aged', 
                'Comorbidity', 'Child', 'Adolescent'
            }
        ]
        
        # Create structured record
        paper = {
            'pmid': pub.pmid,
            'year': pub.year,
            'title': pub.title,
            'abstract': pub.abstract,
            'authors': pub.authors,
            'mesh_terms': pub.mesh_terms,
            'diseases': diseases,
            'team_analysis': {
                'team_type': team['team_type'],
                'female_count': team['female_count'],
                'male_count': team['male_count'],
                'unknown_count': team['unknown_count'],
                'total_authors': team['total'],
                'gender_balance': team['gender_balance'],
                'first_author_gender': team['first_author_gender'],
                'last_author_gender': team['last_author_gender']
            }
        }
        
        papers.append(paper)
        
        # Progress update
        if len(papers) % 5000 == 0:
            print(f"  Processed {len(papers):,} papers...")
    
    print(f"\n✓ Parsed {len(papers):,} papers")
    print(f"  Saving to {output_file}...")
    
    # Save JSON
    if compress:
        # Compressed: 500MB TXT → ~100MB JSON.gz
        with gzip.open(output_file, 'wt', encoding='utf-8') as f:
            json.dump(papers, f, indent=2)
        print(f"  ✓ Saved compressed JSON: {output_file}")
    else:
        # Uncompressed: 500MB TXT → ~200MB JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(papers, f, indent=2)
        print(f"  ✓ Saved JSON: {output_file}")
    
    # Print file sizes
    input_size = Path(input_file).stat().st_size / (1024**2)
    output_size = Path(output_file).stat().st_size / (1024**2)
    print(f"\n  File sizes:")
    print(f"    Input (TXT):  {input_size:.1f} MB")
    print(f"    Output (JSON): {output_size:.1f} MB")
    print(f"    Compression: {100*(1-output_size/input_size):.1f}% smaller")
    
    return papers


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parse_to_json.py <input.txt> [output.json.gz]")
        print("\nExample:")
        print("  python parse_to_json.py pubmed_data.txt pubmed_data.json.gz")
        return
    
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Auto-generate output name
        output_file = input_file.replace('.txt', '.json.gz')
    
    papers = txt_to_json(input_file, output_file, compress=True)
    
    print(f"\n{'='*70}")
    print("CONVERSION COMPLETE!")
    print(f"{'='*70}")
    print(f"\nYou can now:")
    print(f"  1. Delete {input_file} to save space (optional)")
    print(f"  2. Run fast analyses on {output_file}")
    print(f"  3. Share {output_file} with colleagues (smaller file)")


if __name__ == "__main__":
    main()