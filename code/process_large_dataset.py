#!/usr/bin/env python3
"""
Large-Scale PubMed Data Processor for Gendered Innovations Analysis
Optimized for 500MB+ datasets (~100,000-200,000 papers)
"""

import re
import json
import pickle
from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Iterator
from dataclasses import dataclass, asdict
import time
from pathlib import Path


@dataclass
class Publication:
    """Lightweight publication data structure"""
    pmid: str
    year: int
    authors: List[str]
    mesh_terms: List[str]
    title: str = ""
    abstract: str = ""
    journal: str = ""
    
    def to_dict(self):
        return asdict(self)


class LargePubMedParser:
    """Memory-efficient parser for large MEDLINE files"""
    
    def __init__(self):
        self.entries_processed = 0
        self.comorbidity_count = 0
        
    def parse_file_streaming(self, filepath: str) -> Iterator[Publication]:
        """
        Stream parse large file without loading everything into memory
        Yields one publication at a time
        """
        print(f"Starting to parse {filepath}")
        print("This may take 5-10 minutes for 500MB file...")
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            current_entry = []
            
            for line in f:
                # Check if we're starting a new entry
                if line.startswith('PMID-') and current_entry:
                    # Process the accumulated entry
                    entry_text = '\n'.join(current_entry)
                    pub = self._parse_single_entry(entry_text)
                    
                    if pub:
                        self.entries_processed += 1
                        if self._is_comorbidity_study(pub):
                            self.comorbidity_count += 1
                            yield pub
                        
                        # Progress update every 1000 entries
                        if self.entries_processed % 1000 == 0:
                            print(f"  Processed {self.entries_processed:,} entries, "
                                  f"found {self.comorbidity_count:,} comorbidity papers...")
                    
                    current_entry = [line]
                else:
                    current_entry.append(line)
            
            # Process last entry
            if current_entry:
                entry_text = '\n'.join(current_entry)
                pub = self._parse_single_entry(entry_text)
                if pub and self._is_comorbidity_study(pub):
                    self.comorbidity_count += 1
                    yield pub
        
        print(f"\n✓ Parsing complete!")
        print(f"  Total entries: {self.entries_processed:,}")
        print(f"  Comorbidity studies: {self.comorbidity_count:,}")
    
    def _parse_single_entry(self, entry_text: str) -> Publication:
        """Parse a single MEDLINE entry"""
        pmid = ""
        year = 0
        authors = []
        mesh_terms = []
        title = ""
        abstract = ""
        
        lines = entry_text.split('\n')
        current_field = None
        current_value = ""
        
        for line in lines:
            if not line.strip():
                continue
            
            # New field
            if len(line) > 5 and line[4] == '-':
                # Save previous field
                if current_field:
                    pmid, year, authors, mesh_terms, title, abstract = self._save_field(
                        current_field, current_value.strip(),
                        pmid, year, authors, mesh_terms, title, abstract
                    )
                
                current_field = line[:4].strip()
                current_value = line[6:].strip()
            else:
                # Continuation
                current_value += " " + line.strip()
        
        # Save last field
        if current_field:
            pmid, year, authors, mesh_terms, title, abstract = self._save_field(
                current_field, current_value.strip(),
                pmid, year, authors, mesh_terms, title, abstract
            )
        
        if not pmid:
            return None
        
        # Extract year from date string
        if isinstance(year, str):
            year_match = re.search(r'(\d{4})', year)
            year = int(year_match.group(1)) if year_match else 0
        
        return Publication(
            pmid=pmid,
            year=year,
            authors=authors,
            mesh_terms=mesh_terms,
            title=title,
            abstract=abstract
        )
    
    def _save_field(self, field, value, pmid, year, authors, mesh_terms, title, abstract):
        """Update variables based on field type"""
        if field == 'PMID':
            pmid = value
        elif field == 'DP':
            year = value
        elif field in ['FAU', 'AU']:
            authors.append(value)
        elif field == 'MH':
            mesh_terms.append(value)
        elif field == 'TI':
            title = value
        elif field in ['AB', 'OAB']:
            abstract = value if not abstract else abstract + " " + value
        
        return pmid, year, authors, mesh_terms, title, abstract
    
    def _is_comorbidity_study(self, pub: Publication) -> bool:
        """Check if paper is about comorbidity"""
        # Check MeSH terms
        if any('Comorbidity' in term for term in pub.mesh_terms):
            return True
        
        # Check title/abstract
        text = (pub.title + " " + pub.abstract).lower()
        keywords = ['comorbidity', 'comorbidities', 'co-morbidity', 'multimorbidity']
        return any(kw in text for kw in keywords)


class GenderInferenceEngine:
    """Fast gender inference with caching"""
    
    def __init__(self):
        self.cache = {}
        self.female_names = self._load_female_names()
        self.male_names = self._load_male_names()
        
    def _load_female_names(self) -> Set[str]:
        """Load common female names"""
        return {
            'mary', 'maria', 'patricia', 'jennifer', 'linda', 'elizabeth', 'barbara',
            'susan', 'jessica', 'sarah', 'karen', 'nancy', 'betty', 'helen', 'sandra',
            'donna', 'carol', 'ruth', 'sharon', 'michelle', 'laura', 'dorothy', 'lisa',
            'teresa', 'anna', 'christine', 'catherine', 'margaret', 'frances', 'janet',
            'diane', 'alice', 'julie', 'joyce', 'virginia', 'kathleen', 'deborah',
            'angela', 'brenda', 'pamela', 'emma', 'stephanie', 'carolyn', 'rachel',
            'marie', 'heather', 'nicole', 'amy', 'melissa', 'rebecca', 'kimberly',
            'debra', 'sophia', 'olivia', 'isabella', 'mia', 'charlotte', 'amelia',
            'harper', 'evelyn', 'abigail', 'emily', 'ella', 'madison', 'grace',
            'elena', 'clara', 'rosa', 'carmen', 'lucia', 'ana', 'andrea', 'monica',
            'rita', 'jane', 'alexandra', 'natalie', 'victoria', 'hannah', 'claire',
            'julia', 'allison', 'katherine', 'samantha', 'amanda', 'christina'
        }
    
    def _load_male_names(self) -> Set[str]:
        """Load common male names"""
        return {
            'james', 'john', 'robert', 'michael', 'william', 'david', 'richard',
            'joseph', 'thomas', 'charles', 'christopher', 'daniel', 'matthew',
            'anthony', 'donald', 'mark', 'paul', 'steven', 'andrew', 'kenneth',
            'joshua', 'george', 'kevin', 'brian', 'edward', 'ronald', 'timothy',
            'jason', 'jeffrey', 'ryan', 'jacob', 'gary', 'nicholas', 'eric',
            'stephen', 'jonathan', 'larry', 'justin', 'scott', 'brandon', 'frank',
            'benjamin', 'gregory', 'samuel', 'raymond', 'patrick', 'alexander',
            'jack', 'dennis', 'jerry', 'tyler', 'aaron', 'henry', 'douglas',
            'peter', 'adam', 'nathan', 'zachary', 'walter', 'kyle', 'harold',
            'carl', 'jeremy', 'keith', 'roger', 'gerald', 'ethan', 'arthur',
            'jose', 'juan', 'luis', 'carlos', 'antonio', 'francisco', 'miguel',
            'manuel', 'pedro', 'alejandro', 'fernando', 'ricardo', 'martin'
        }
    
    def infer_gender_batch(self, authors: List[str]) -> List[str]:
        """
        Infer gender for list of authors
        Returns: ['F', 'M', 'U', ...] for each author
        """
        genders = []
        for author in authors:
            if author in self.cache:
                genders.append(self.cache[author])
            else:
                gender = self._infer_single(author)
                self.cache[author] = gender
                genders.append(gender)
        return genders
    
    def _infer_single(self, name: str) -> str:
        """Infer gender from single name"""
        # Extract first name
        parts = name.lower().replace(',', ' ').split()
        if len(parts) < 2:
            return 'U'
        
        # Try second part first (after comma format)
        first_name = parts[1] if ',' in name else parts[0]
        first_name = first_name.strip('.')
        
        if first_name in self.female_names:
            return 'F'
        elif first_name in self.male_names:
            return 'M'
        
        # Heuristic: names ending in 'a' often female
        if first_name.endswith('a') and len(first_name) > 3:
            return 'F'
        
        return 'U'
    
    def analyze_team(self, authors: List[str]) -> Dict:
        """Analyze gender composition of team"""
        genders = self.infer_gender_batch(authors)
        
        female_count = genders.count('F')
        male_count = genders.count('M')
        unknown_count = genders.count('U')
        
        if female_count == 0 and male_count == 0:
            team_type = 'unknown'
            gender_balance = None
        elif female_count == 0:
            team_type = 'all_male'
            gender_balance = 0.0
        elif male_count == 0:
            team_type = 'all_female'
            gender_balance = 1.0
        else:
            team_type = 'mixed'
            gender_balance = female_count / (female_count + male_count)
        
        return {
            'team_type': team_type,
            'female_count': female_count,
            'male_count': male_count,
            'unknown_count': unknown_count,
            'total': len(authors),
            'gender_balance': gender_balance,
            'first_author_gender': genders[0] if genders else 'U',
            'last_author_gender': genders[-1] if genders else 'U',
            'genders': genders
        }


class BatchAnalyzer:
    """Process large dataset in batches"""
    
    def __init__(self, output_dir: str = './analysis_output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.gender_engine = GenderInferenceEngine()
        
        # Storage for incremental results
        self.year_stats = defaultdict(lambda: {
            'total': 0,
            'all_male': 0,
            'all_female': 0,
            'mixed': 0,
            'unknown': 0
        })
        
        self.disease_combos = defaultdict(lambda: {
            'all_male': [],
            'all_female': [],
            'mixed': [],
            'unknown': []
        })
        
        self.novel_combos = {}  # First appearance tracker
        
    def process_dataset(self, filepath: str, batch_size: int = 1000):
        """
        Process entire dataset in batches
        Saves progress every batch for crash recovery
        """
        parser = LargePubMedParser()
        
        batch = []
        batch_num = 0
        start_time = time.time()
        
        print("\n" + "="*70)
        print("GENDERED INNOVATIONS ANALYSIS - BATCH PROCESSING")
        print("="*70 + "\n")
        
        for pub in parser.parse_file_streaming(filepath):
            batch.append(pub)
            
            if len(batch) >= batch_size:
                batch_num += 1
                self._process_batch(batch, batch_num)
                batch = []
        
        # Process remaining
        if batch:
            batch_num += 1
            self._process_batch(batch, batch_num)
        
        # Generate final report
        elapsed = time.time() - start_time
        print(f"\n{'='*70}")
        print(f"ANALYSIS COMPLETE in {elapsed/60:.1f} minutes")
        print(f"{'='*70}\n")
        
        self._generate_final_report()
        
    def _process_batch(self, batch: List[Publication], batch_num: int):
        """Process one batch of publications"""
        print(f"\n→ Processing batch {batch_num} ({len(batch)} papers)...")
        
        for pub in batch:
            # Analyze team composition
            team = self.gender_engine.analyze_team(pub.authors)
            
            # Update yearly stats
            self.year_stats[pub.year]['total'] += 1
            self.year_stats[pub.year][team['team_type']] += 1
            
            # Track disease combinations
            diseases = self._extract_diseases(pub.mesh_terms)
            if len(diseases) >= 2:
                combo = tuple(sorted(diseases[:3]))  # Top 3
                combo_str = ' + '.join(combo)
                
                self.disease_combos[combo_str][team['team_type']].append({
                    'pmid': pub.pmid,
                    'year': pub.year,
                    'title': pub.title[:100]
                })
                
                # Track if novel
                if combo_str not in self.novel_combos:
                    self.novel_combos[combo_str] = {
                        'year': pub.year,
                        'pmid': pub.pmid,
                        'team_type': team['team_type'],
                        'gender_balance': team['gender_balance']
                    }
        
        # Save checkpoint
        self._save_checkpoint(batch_num)
        print(f"  ✓ Batch {batch_num} complete. Checkpoint saved.")
    
    def _extract_diseases(self, mesh_terms: List[str]) -> List[str]:
        """Extract disease names from MeSH terms"""
        exclude = {'Female', 'Male', 'Humans', 'Adult', 'Aged', 'Middle Aged',
                   'Comorbidity', 'Child', 'Adolescent', 'Infant', 'Young Adult'}
        
        diseases = []
        for term in mesh_terms:
            # Remove qualifiers
            main_term = term.split('/')[0]
            if main_term not in exclude and len(main_term) > 3:
                diseases.append(main_term)
        
        return diseases
    
    def _save_checkpoint(self, batch_num: int):
        """Save progress checkpoint"""
        checkpoint = {
            'batch_num': batch_num,
            'year_stats': dict(self.year_stats),
            'novel_combos': self.novel_combos
        }
        
        checkpoint_file = self.output_dir / f'checkpoint_batch_{batch_num}.pkl'
        with open(checkpoint_file, 'wb') as f:
            pickle.dump(checkpoint, f)
    
    def _generate_final_report(self):
        """Generate comprehensive final report"""
        print("\nGenerating final report...")
        
        # Calculate summary statistics
        total_papers = sum(year_data['total'] for year_data in self.year_stats.values())
        
        team_totals = Counter()
        for year_data in self.year_stats.values():
            team_totals['all_male'] += year_data['all_male']
            team_totals['all_female'] += year_data['all_female']
            team_totals['mixed'] += year_data['mixed']
            team_totals['unknown'] += year_data['unknown']
        
        # Novelty analysis
        novelty_by_team = Counter()
        for combo_data in self.novel_combos.values():
            novelty_by_team[combo_data['team_type']] += 1
        
        # Create report
        report = {
            'summary': {
                'total_papers': total_papers,
                'year_range': (min(self.year_stats.keys()), max(self.year_stats.keys())),
                'team_composition': {
                    'all_male': team_totals['all_male'],
                    'all_female': team_totals['all_female'],
                    'mixed': team_totals['mixed'],
                    'unknown': team_totals['unknown']
                },
                'percentages': {
                    'all_male_pct': 100 * team_totals['all_male'] / total_papers,
                    'all_female_pct': 100 * team_totals['all_female'] / total_papers,
                    'mixed_pct': 100 * team_totals['mixed'] / total_papers,
                    'unknown_pct': 100 * team_totals['unknown'] / total_papers
                }
            },
            'novelty_analysis': {
                'total_novel_combinations': len(self.novel_combos),
                'by_team_type': dict(novelty_by_team),
                'percentages': {
                    team: 100 * count / sum(novelty_by_team.values())
                    for team, count in novelty_by_team.items()
                }
            },
            'temporal_trends': dict(self.year_stats),
            'top_disease_combinations': self._get_top_combinations(20)
        }
        
        # Save report
        report_file = self.output_dir / 'final_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        self._print_summary(report)
        
        print(f"\n✓ Report saved to: {report_file}")
        
    def _get_top_combinations(self, n: int) -> List[Dict]:
        """Get top N disease combinations by frequency"""
        combo_counts = []
        for combo, team_data in self.disease_combos.items():
            total = sum(len(papers) for papers in team_data.values())
            combo_counts.append({
                'combination': combo,
                'total_papers': total,
                'by_team': {
                    team: len(papers) for team, papers in team_data.items()
                }
            })
        
        combo_counts.sort(key=lambda x: x['total_papers'], reverse=True)
        return combo_counts[:n]
    
    def _print_summary(self, report: Dict):
        """Print formatted summary to console"""
        s = report['summary']
        n = report['novelty_analysis']
        
        print("\n" + "="*70)
        print("FINAL RESULTS SUMMARY")
        print("="*70)
        
        print(f"\nDataset Overview:")
        print(f"  Total papers analyzed: {s['total_papers']:,}")
        print(f"  Year range: {s['year_range'][0]} - {s['year_range'][1]}")
        
        print(f"\nTeam Composition:")
        print(f"  All-male teams:    {s['team_composition']['all_male']:>7,} ({s['percentages']['all_male_pct']:>5.1f}%)")
        print(f"  All-female teams:  {s['team_composition']['all_female']:>7,} ({s['percentages']['all_female_pct']:>5.1f}%)")
        print(f"  Mixed-gender teams:{s['team_composition']['mixed']:>7,} ({s['percentages']['mixed_pct']:>5.1f}%)")
        print(f"  Unknown:           {s['team_composition']['unknown']:>7,} ({s['percentages']['unknown_pct']:>5.1f}%)")
        
        print(f"\nNovelty Analysis:")
        print(f"  Total novel disease combinations discovered: {n['total_novel_combinations']:,}")
        print(f"  Discoveries by team type:")
        for team, count in n['by_team_type'].items():
            pct = n['percentages'].get(team, 0)
            print(f"    {team:15s}: {count:>5,} ({pct:>5.1f}%)")
        
        if s['team_composition']['mixed'] > 0 and s['team_composition']['all_male'] > 0:
            mixed_pct = s['percentages']['mixed_pct']
            mixed_novel_pct = n['percentages'].get('mixed', 0)
            enrichment = mixed_novel_pct / mixed_pct if mixed_pct > 0 else 0
            
            print(f"\n  💡 Mixed-gender teams represent {mixed_pct:.1f}% of papers")
            print(f"     but discovered {mixed_novel_pct:.1f}% of novel combinations")
            if enrichment > 1:
                print(f"     → {enrichment:.2f}× enrichment in novel discoveries! ⭐")


def main():
    """Main execution function"""
    import sys
    
    print("\n" + "="*70)
    print("GENDERED INNOVATIONS IN COMORBIDITY RESEARCH")
    print("Large-Scale PubMed Data Processor")
    print("="*70 + "\n")
    
    # Get file path
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        print("Usage: python3 process_large_dataset.py <path_to_pubmed_file>")
        print("\nOr enter path now:")
        filepath = input("Path to PubMed file: ").strip()
    
    if not Path(filepath).exists():
        print(f"❌ Error: File not found: {filepath}")
        return
    
    # Get file size
    size_mb = Path(filepath).stat().st_size / (1024 * 1024)
    print(f"Input file: {filepath}")
    print(f"File size: {size_mb:.1f} MB")
    print(f"Estimated time: {size_mb/100 * 5:.0f}-{size_mb/100 * 10:.0f} minutes\n")
    
    proceed = input("Proceed with analysis? (yes/no): ").strip().lower()
    if proceed != 'yes':
        print("Analysis cancelled.")
        return
    
    # Run analysis
    analyzer = BatchAnalyzer(output_dir='./analysis_output')
    analyzer.process_dataset(filepath, batch_size=1000)
    
    print("\n✓ Analysis complete!")
    print(f"  Results saved to: ./analysis_output/")
    print(f"  - final_report.json (summary statistics)")
    print(f"  - checkpoint_*.pkl files (for recovery)")


if __name__ == "__main__":
    main()
