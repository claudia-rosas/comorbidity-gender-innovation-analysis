#!/usr/bin/env python3
"""
Generate visualizations from processed data
Works with output from process_large_dataset.py
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'
sns.set_style("whitegrid")
sns.set_palette("husl")


class ResultsVisualizer:
    """Generate all visualizations from analysis results"""
    
    def __init__(self, report_path: str = './analysis_output/final_report.json'):
        with open(report_path, 'r') as f:
            self.report = json.load(f)
        
        self.output_dir = Path('./analysis_output/figures')
        self.output_dir.mkdir(exist_ok=True)
        
    def generate_all(self):
        """Generate all visualizations"""
        print("\nGenerating visualizations...")
        print("="*60)
        
        self.plot_team_composition()
        self.plot_temporal_trends()
        self.plot_novelty_comparison()
        self.plot_top_combinations()
        self.create_summary_dashboard()
        
        print(f"\n✓ All visualizations saved to: {self.output_dir}/")
        
    def plot_team_composition(self):
        """Pie chart of overall team composition"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        comp = self.report['summary']['team_composition']
        pcts = self.report['summary']['percentages']
        
        # Filter out unknown if very small
        teams = ['all_male', 'all_female', 'mixed']
        if comp['unknown'] > comp['all_male'] * 0.1:  # If unknown > 10% of male
            teams.append('unknown')
        
        values = [comp[team] for team in teams]
        labels = [self._format_team_label(team) for team in teams]
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#95a5a6'][:len(teams)]
        
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        
        # Make percentage text white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
        
        ax.set_title('Team Gender Composition in Comorbidity Research\n' + 
                     f'(n={self.report["summary"]["total_papers"]:,} papers)',
                     fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'team_composition.png', bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: team_composition.png")
        
    def plot_temporal_trends(self):
        """Line plot of trends over time"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        temporal = self.report['temporal_trends']
        years = sorted([int(y) for y in temporal.keys()])
        
        # Absolute counts
        all_male = [temporal[str(y)]['all_male'] for y in years]
        all_female = [temporal[str(y)]['all_female'] for y in years]
        mixed = [temporal[str(y)]['mixed'] for y in years]
        
        ax1.plot(years, all_male, marker='o', linewidth=2.5, 
                label='All-male teams', color='#3498db')
        ax1.plot(years, all_female, marker='s', linewidth=2.5,
                label='All-female teams', color='#e74c3c')
        ax1.plot(years, mixed, marker='^', linewidth=2.5,
                label='Mixed-gender teams', color='#2ecc71')
        
        ax1.set_xlabel('Year', fontsize=12)
        ax1.set_ylabel('Number of Publications', fontsize=12)
        ax1.set_title('Comorbidity Research Publications by Team Composition Over Time',
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        # Percentages (stacked area)
        totals = [all_male[i] + all_female[i] + mixed[i] for i in range(len(years))]
        
        pct_male = [100 * all_male[i] / totals[i] if totals[i] > 0 else 0 
                    for i in range(len(years))]
        pct_female = [100 * all_female[i] / totals[i] if totals[i] > 0 else 0
                      for i in range(len(years))]
        pct_mixed = [100 * mixed[i] / totals[i] if totals[i] > 0 else 0
                     for i in range(len(years))]
        
        ax2.fill_between(years, 0, pct_male, 
                        label='All-male', alpha=0.7, color='#3498db')
        ax2.fill_between(years, pct_male,
                        [pct_male[i] + pct_female[i] for i in range(len(years))],
                        label='All-female', alpha=0.7, color='#e74c3c')
        ax2.fill_between(years,
                        [pct_male[i] + pct_female[i] for i in range(len(years))],
                        100, label='Mixed-gender', alpha=0.7, color='#2ecc71')
        
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Percentage of Publications', fontsize=12)
        ax2.set_title('Team Composition Distribution Over Time (%)',
                     fontsize=14, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=11)
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'temporal_trends.png', bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: temporal_trends.png")
        
    def plot_novelty_comparison(self):
        """Bar chart comparing novelty by team type"""
        fig, ax = plt.subplots(figsize=(12, 7))
        
        novelty = self.report['novelty_analysis']
        
        teams = ['All-male', 'All-female', 'Mixed-gender']
        team_keys = ['all_male', 'all_female', 'mixed']
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        
        counts = [novelty['by_team_type'].get(key, 0) for key in team_keys]
        
        bars = ax.bar(teams, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count):,}',
                   ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Add percentage labels
        percentages = [novelty['percentages'].get(key, 0) for key in team_keys]
        for i, (bar, pct) in enumerate(zip(bars, percentages)):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height()/2,
                   f'{pct:.1f}%',
                   ha='center', va='center', fontsize=12, 
                   color='white', fontweight='bold')
        
        ax.set_ylabel('Number of Novel Disease Combinations Discovered', fontsize=13)
        ax.set_title('Novel Disease Combination Discovery by Team Gender Composition\n' +
                    '(First publication on specific disease pair/triplet)',
                    fontsize=15, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add enrichment annotation
        comp = self.report['summary']['percentages']
        if comp['mixed_pct'] > 0 and percentages[2] > 0:
            enrichment = percentages[2] / comp['mixed_pct']
            if enrichment > 1.1:
                ax.text(0.98, 0.98, 
                       f'Mixed teams: {comp["mixed_pct"]:.1f}% of papers\n' +
                       f'but {percentages[2]:.1f}% of novel discoveries\n' +
                       f'→ {enrichment:.2f}× enrichment ⭐',
                       transform=ax.transAxes,
                       fontsize=11, 
                       verticalalignment='top',
                       horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'novelty_comparison.png', bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: novelty_comparison.png")
        
    def plot_top_combinations(self):
        """Heatmap of top disease combinations"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        top_combos = self.report['top_disease_combinations'][:20]
        
        # Prepare data
        combo_names = [c['combination'][:60] + '...' if len(c['combination']) > 60 
                      else c['combination'] for c in top_combos]
        
        team_types = ['all_male', 'all_female', 'mixed']
        matrix = np.zeros((len(top_combos), len(team_types)))
        
        for i, combo in enumerate(top_combos):
            total = combo['total_papers']
            for j, team in enumerate(team_types):
                count = combo['by_team'].get(team, 0)
                matrix[i, j] = 100 * count / total if total > 0 else 0
        
        # Create heatmap
        im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', vmin=0, vmax=100)
        
        # Set ticks
        ax.set_xticks(range(len(team_types)))
        ax.set_xticklabels(['All-male', 'All-female', 'Mixed-gender'], fontsize=11)
        ax.set_yticks(range(len(combo_names)))
        ax.set_yticklabels(combo_names, fontsize=9)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, pad=0.02)
        cbar.set_label('% of studies on this combination', 
                      rotation=270, labelpad=20, fontsize=11)
        
        # Add text annotations
        for i in range(len(top_combos)):
            for j in range(len(team_types)):
                text = ax.text(j, i, f'{matrix[i, j]:.0f}%',
                             ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title('Top 20 Disease Combinations: Team Composition Distribution',
                    fontsize=15, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_combinations.png', bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: top_combinations.png")
        
    def create_summary_dashboard(self):
        """Create comprehensive summary dashboard"""
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Gendered Innovations in Comorbidity Research - Summary Dashboard',
                    fontsize=18, fontweight='bold', y=0.98)
        
        # Panel 1: Key metrics
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        s = self.report['summary']
        n = self.report['novelty_analysis']
        
        metrics_text = f"""
        DATASET OVERVIEW
        • Total Papers: {s['total_papers']:,}
        • Year Range: {s['year_range'][0]} - {s['year_range'][1]}
        • Novel Disease Combinations: {n['total_novel_combinations']:,}
        
        TEAM COMPOSITION                          NOVEL DISCOVERIES
        • Mixed-gender:  {s['percentages']['mixed_pct']:>5.1f}%        • Mixed-gender:  {n['percentages'].get('mixed', 0):>5.1f}%
        • All-male:      {s['percentages']['all_male_pct']:>5.1f}%        • All-male:      {n['percentages'].get('all_male', 0):>5.1f}%
        • All-female:    {s['percentages']['all_female_pct']:>5.1f}%        • All-female:    {n['percentages'].get('all_female', 0):>5.1f}%
        """
        
        ax1.text(0.5, 0.5, metrics_text, 
                fontsize=12, family='monospace',
                verticalalignment='center', horizontalalignment='center',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        # Panel 2: Pie chart
        ax2 = fig.add_subplot(gs[1, 0])
        comp = s['team_composition']
        teams = ['all_male', 'all_female', 'mixed']
        values = [comp[t] for t in teams]
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        ax2.pie(values, labels=['All-male', 'All-female', 'Mixed'], 
               autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('Team Composition', fontweight='bold')
        
        # Panel 3: Novelty bars
        ax3 = fig.add_subplot(gs[1, 1])
        novelty_counts = [n['by_team_type'].get(t, 0) for t in teams]
        ax3.bar(['All-male', 'All-female', 'Mixed'], novelty_counts, color=colors)
        ax3.set_ylabel('Novel Discoveries')
        ax3.set_title('Novelty by Team Type', fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Panel 4: Enrichment comparison
        ax4 = fig.add_subplot(gs[1, 2])
        x = [s['percentages'][t+'_pct'] for t in teams]
        y = [n['percentages'].get(t, 0) for t in teams]
        
        ax4.scatter(x, y, s=200, c=colors, alpha=0.7, edgecolors='black', linewidth=2)
        
        # Add diagonal line (y=x)
        max_val = max(max(x), max(y))
        ax4.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Equal proportion')
        
        # Label points
        labels = ['Male', 'Female', 'Mixed']
        for i, label in enumerate(labels):
            ax4.annotate(label, (x[i], y[i]), 
                        xytext=(5, 5), textcoords='offset points', fontsize=10)
        
        ax4.set_xlabel('% of Total Papers')
        ax4.set_ylabel('% of Novel Discoveries')
        ax4.set_title('Discovery Enrichment', fontweight='bold')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Panel 5: Temporal trend
        ax5 = fig.add_subplot(gs[2, :])
        temporal = self.report['temporal_trends']
        years = sorted([int(y) for y in temporal.keys()])
        mixed_pct = []
        
        for year in years:
            data = temporal[str(year)]
            total = data['total']
            if total > 0:
                pct = 100 * data['mixed'] / total
                mixed_pct.append(pct)
            else:
                mixed_pct.append(0)
        
        ax5.plot(years, mixed_pct, linewidth=3, color='#2ecc71', marker='o')
        ax5.fill_between(years, 0, mixed_pct, alpha=0.3, color='#2ecc71')
        ax5.set_xlabel('Year')
        ax5.set_ylabel('% Mixed-Gender Teams')
        ax5.set_title('Growth of Mixed-Gender Teams Over Time', fontweight='bold')
        ax5.grid(True, alpha=0.3)
        
        plt.savefig(self.output_dir / 'summary_dashboard.png', bbox_inches='tight')
        plt.close()
        print("  ✓ Saved: summary_dashboard.png")
        
    def _format_team_label(self, team_key: str) -> str:
        """Format team type for display"""
        labels = {
            'all_male': 'All-Male Teams',
            'all_female': 'All-Female Teams',
            'mixed': 'Mixed-Gender Teams',
            'unknown': 'Unknown'
        }
        return labels.get(team_key, team_key)


def main():
    """Main execution"""
    import sys
    
    print("\n" + "="*70)
    print("VISUALIZATION GENERATOR")
    print("="*70 + "\n")
    
    report_path = './analysis_output/final_report.json'
    
    if len(sys.argv) > 1:
        report_path = sys.argv[1]
    
    if not Path(report_path).exists():
        print(f"❌ Error: Report file not found: {report_path}")
        print("\nPlease run process_large_dataset.py first.")
        return
    
    visualizer = ResultsVisualizer(report_path)
    visualizer.generate_all()
    
    print("\n✓ Visualization complete!")
    print("  View figures in: ./analysis_output/figures/")


if __name__ == "__main__":
    main()
