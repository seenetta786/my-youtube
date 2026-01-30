#!/usr/bin/env python3
"""
Virat Kohli Cricket Statistics Histogram Report Generator
Creates comprehensive histogram visualizations for Virat Kohli's performance across all formats
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ViratKohliHistogramReport:
    def __init__(self):
        self.formats = ['Test', 'ODI', 'T20I', 'IPL']
        self.colors = ['#2E86AB', '#F18F01', '#C0392B', '#27AE60']
        
        # Sample Virat Kohli statistics (based on real career data as of 2024)
        self.career_stats = {
            'Test': {
                'matches': 113,
                'innings': 199,
                'runs': 8848,
                'highest_score': 254,
                'average': 49.43,
                'strike_rate': 54.71,
                'centuries': 29,
                'fifties': 31,
                'fours': 1140,
                'sixes': 100
            },
            'ODI': {
                'matches': 292,
                'innings': 281,
                'runs': 13848,
                'highest_score': 183,
                'average': 58.18,
                'strike_rate': 93.23,
                'centuries': 50,
                'fifties': 66,
                'fours': 1324,
                'sixes': 133
            },
            'T20I': {
                'matches': 117,
                'innings': 109,
                'runs': 4037,
                'highest_score': 122,
                'average': 51.75,
                'strike_rate': 137.76,
                'centuries': 1,
                'fifties': 36,
                'fours': 425,
                'sixes': 73
            },
            'IPL': {
                'matches': 285,
                'innings': 275,
                'runs': 8006,
                'highest_score': 113,
                'average': 37.22,
                'strike_rate': 130.39,
                'centuries': 7,
                'fifties': 66,
                'fours': 893,
                'sixes': 191
            }
        }
    
    def create_runs_histogram(self):
        """Create histogram showing runs distribution across formats"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Virat Kohli - Comprehensive Cricket Statistics Analysis', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # 1. Runs by Format
        runs_data = [self.career_stats[fmt]['runs'] for fmt in self.formats]
        bars1 = ax1.bar(self.formats, runs_data, color=self.colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax1.set_title('Total Runs by Format', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Runs', fontsize=12)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars1, runs_data):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 100,
                    f'{value:,}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Average by Format
        avg_data = [self.career_stats[fmt]['average'] for fmt in self.formats]
        bars2 = ax2.bar(self.formats, avg_data, color=self.colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax2.set_title('Batting Average by Format', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Average', fontsize=12)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, value in zip(bars2, avg_data):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Strike Rate by Format
        sr_data = [self.career_stats[fmt]['strike_rate'] for fmt in self.formats]
        bars3 = ax3.bar(self.formats, sr_data, color=self.colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax3.set_title('Strike Rate by Format', fontsize=16, fontweight='bold')
        ax3.set_ylabel('Strike Rate', fontsize=12)
        ax3.grid(axis='y', alpha=0.3)
        
        for bar, value in zip(bars3, sr_data):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Centuries by Format
        centuries_data = [self.career_stats[fmt]['centuries'] for fmt in self.formats]
        bars4 = ax4.bar(self.formats, centuries_data, color=self.colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax4.set_title('Centuries by Format', fontsize=16, fontweight='bold')
        ax4.set_ylabel('Number of Centuries', fontsize=12)
        ax4.grid(axis='y', alpha=0.3)
        
        for bar, value in zip(bars4, centuries_data):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        return fig
    
    def create_detailed_analysis(self):
        """Create detailed analysis charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Virat Kohli - Advanced Performance Metrics', 
                    fontsize=20, fontweight='bold', y=0.98)
        
        # 1. Matches vs Innings
        matches_data = [self.career_stats[fmt]['matches'] for fmt in self.formats]
        innings_data = [self.career_stats[fmt]['innings'] for fmt in self.formats]
        
        x = np.arange(len(self.formats))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, matches_data, width, label='Matches', 
                       color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
        bars2 = ax1.bar(x + width/2, innings_data, width, label='Innings', 
                       color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1)
        
        ax1.set_title('Matches vs Innings by Format', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Count', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(self.formats)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # 2. Boundaries Analysis (Fours and Sixes)
        fours_data = [self.career_stats[fmt]['fours'] for fmt in self.formats]
        sixes_data = [self.career_stats[fmt]['sixes'] for fmt in self.formats]
        
        bars1 = ax2.bar(x - width/2, fours_data, width, label='Fours', 
                       color='#f1c40f', alpha=0.8, edgecolor='black', linewidth=1)
        bars2 = ax2.bar(x + width/2, sixes_data, width, label='Sixes', 
                       color='#9b59b6', alpha=0.8, edgecolor='black', linewidth=1)
        
        ax2.set_title('Boundaries Analysis (Fours & Sixes)', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Count', fontsize=12)
        ax2.set_xticks(x)
        ax2.set_xticklabels(self.formats)
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 3. Fifties vs Centuries Ratio
        fifties_data = [self.career_stats[fmt]['fifties'] for fmt in self.formats]
        centuries_data = [self.career_stats[fmt]['centuries'] for fmt in self.formats]
        
        bars1 = ax3.bar(x - width/2, fifties_data, width, label='Fifties', 
                       color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1)
        bars2 = ax3.bar(x + width/2, centuries_data, width, label='Centuries', 
                       color='#e67e22', alpha=0.8, edgecolor='black', linewidth=1)
        
        ax3.set_title('Fifties vs Centuries by Format', fontsize=16, fontweight='bold')
        ax3.set_ylabel('Count', fontsize=12)
        ax3.set_xticks(x)
        ax3.set_xticklabels(self.formats)
        ax3.legend()
        ax3.grid(axis='y', alpha=0.3)
        
        # 4. Highest Scores
        highest_data = [self.career_stats[fmt]['highest_score'] for fmt in self.formats]
        bars4 = ax4.bar(self.formats, highest_data, color=self.colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax4.set_title('Highest Scores by Format', fontsize=16, fontweight='bold')
        ax4.set_ylabel('Highest Score', fontsize=12)
        ax4.grid(axis='y', alpha=0.3)
        
        for bar, value in zip(bars4, highest_data):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.92)
        return fig
    
    def create_summary_dashboard(self):
        """Create a summary dashboard with key metrics"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create a summary table
        summary_data = []
        for fmt in self.formats:
            stats = self.career_stats[fmt]
            summary_data.append([
                fmt,
                stats['matches'],
                stats['innings'],
                f"{stats['runs']:,}",
                f"{stats['average']:.2f}",
                f"{stats['strike_rate']:.2f}",
                stats['centuries'],
                stats['fifties'],
                f"{stats['highest_score']}"
            ])
        
        # Create the table
        table = ax.table(cellText=summary_data,
                        colLabels=['Format', 'Matches', 'Innings', 'Runs', 'Avg', 'SR', '100s', '50s', 'HS'],
                        cellLoc='center',
                        loc='center')
        
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        # Style the table
        for i in range(len(summary_data) + 1):
            for j in range(len(summary_data[0])):
                if i == 0:  # Header row
                    table[(i, j)].set_facecolor('#3498db')
                    table[(i, j)].set_text_props(weight='bold', color='white')
                else:
                    table[(i, j)].set_facecolor('#f8f9fa' if i % 2 == 0 else '#e9ecef')
        
        ax.set_title('Virat Kohli - Career Statistics Summary', fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
        
        return fig
    
    def save_all_charts(self):
        """Generate and save all histogram charts"""
        print("Generating Virat Kohli Cricket Statistics Histogram Report...")
        
        # Create main statistics charts
        fig1 = self.create_runs_histogram()
        fig1.savefig('virat_kohli_main_stats.png', dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        # Create detailed analysis charts
        fig2 = self.create_detailed_analysis()
        fig2.savefig('virat_kohli_detailed_analysis.png', dpi=300, bbox_inches='tight')
        plt.close(fig2)
        
        # Create summary dashboard
        fig3 = self.create_summary_dashboard()
        fig3.savefig('virat_kohli_summary_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close(fig3)
        
        print("✅ Histogram charts generated successfully!")
        print("📁 Generated files:")
        print("   - virat_kohli_main_stats.png")
        print("   - virat_kohli_detailed_analysis.png") 
        print("   - virat_kohli_summary_dashboard.png")
        
        # Create HTML report
        self.create_html_report()
    
    def create_html_report(self):
        """Create an interactive HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Virat Kohli - Cricket Statistics Histogram Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .subtitle {{
                    font-size: 1.2em;
                    margin-top: 10px;
                    opacity: 0.9;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .stat-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border-left: 5px solid;
                }}
                .stat-card.test {{ border-left-color: #2E86AB; }}
                .stat-card.odi {{ border-left-color: #F18F01; }}
                .stat-card.t20i {{ border-left-color: #C0392B; }}
                .stat-card.ipl {{ border-left-color: #27AE60; }}
                .stat-title {{
                    font-size: 1.2em;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #333;
                }}
                .stat-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                    border-bottom: 1px solid #eee;
                }}
                .stat-value {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .charts-section {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .chart-title {{
                    font-size: 1.5em;
                    margin-bottom: 20px;
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }}
                .chart-container {{
                    text-align: center;
                    margin-bottom: 40px;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #7f8c8d;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏏 Virat Kohli</h1>
                <div class="subtitle">Comprehensive Cricket Statistics Histogram Report</div>
            </div>
            
            <div class="stats-grid">
        """
        
        # Add statistics cards
        for i, fmt in enumerate(self.formats):
            stats = self.career_stats[fmt]
            html_content += f"""
                <div class="stat-card {fmt.lower()}">
                    <div class="stat-title">📊 {fmt} Statistics</div>
                    <div class="stat-item">
                        <span>Matches</span>
                        <span class="stat-value">{stats['matches']}</span>
                    </div>
                    <div class="stat-item">
                        <span>Innings</span>
                        <span class="stat-value">{stats['innings']}</span>
                    </div>
                    <div class="stat-item">
                        <span>Runs</span>
                        <span class="stat-value">{stats['runs']:,}</span>
                    </div>
                    <div class="stat-item">
                        <span>Average</span>
                        <span class="stat-value">{stats['average']:.2f}</span>
                    </div>
                    <div class="stat-item">
                        <span>Strike Rate</span>
                        <span class="stat-value">{stats['strike_rate']:.2f}</span>
                    </div>
                    <div class="stat-item">
                        <span>Centuries</span>
                        <span class="stat-value">{stats['centuries']}</span>
                    </div>
                    <div class="stat-item">
                        <span>Fifties</span>
                        <span class="stat-value">{stats['fifties']}</span>
                    </div>
                    <div class="stat-item">
                        <span>Highest Score</span>
                        <span class="stat-value">{stats['highest_score']}</span>
                    </div>
                </div>
            """
        
        html_content += """
            </div>
            
            <div class="charts-section">
                <div class="chart-title">📈 Main Statistics Histograms</div>
                <div class="chart-container">
                    <img src="virat_kohli_main_stats.png" alt="Main Statistics">
                </div>
                
                <div class="chart-title">🔍 Detailed Analysis Charts</div>
                <div class="chart-container">
                    <img src="virat_kohli_detailed_analysis.png" alt="Detailed Analysis">
                </div>
                
                <div class="chart-title">📋 Summary Dashboard</div>
                <div class="chart-container">
                    <img src="virat_kohli_summary_dashboard.png" alt="Summary Dashboard">
                </div>
            </div>
            
            <div class="footer">
                <p>Generated with Python Matplotlib & Seaborn | Data represents career statistics as of 2024</p>
                <p>📊 Histogram Report for Virat Kohli's Performance Across All Cricket Formats</p>
            </div>
        </body>
        </html>
        """
        
        with open('virat_kohli_histogram_report.html', 'w') as f:
            f.write(html_content)
        
        print("📄 HTML report generated: virat_kohli_histogram_report.html")

def main():
    """Main function to generate the complete histogram report"""
    print("🚀 Starting Virat Kohli Cricket Statistics Histogram Report Generation")
    print("=" * 70)
    
    # Create the report generator
    report = ViratKohliHistogramReport()
    
    # Generate all charts and reports
    report.save_all_charts()
    
    print("\n🎉 Virat Kohli Histogram Report Generation Complete!")
    print("\n📁 Generated Files:")
    print("   ✅ virat_kohli_main_stats.png - Main statistics histograms")
    print("   ✅ virat_kohli_detailed_analysis.png - Advanced analysis charts")
    print("   ✅ virat_kohli_summary_dashboard.png - Career summary table")
    print("   ✅ virat_kohli_histogram_report.html - Interactive HTML report")
    print("   ✅ kohli_histogram_report.py - This script")
    
    print("\n📊 Report Features:")
    print("   • Runs distribution across all formats")
    print("   • Batting averages comparison")
    print("   • Strike rate analysis")
    print("   • Century and fifty counts")
    print("   • Matches vs innings breakdown")
    print("   • Boundary analysis (fours & sixes)")
    print("   • Highest scores comparison")
    print("   • Comprehensive career summary")

if __name__ == "__main__":
    main()