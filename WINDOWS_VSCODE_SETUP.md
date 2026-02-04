# Windows Setup Guide: VS Code for Gendered Innovations Analysis

## Complete Setup for Windows (No Notebooks Required!)

---

## Part 1: Install Python (5 minutes)

### Step 1.1: Download Python
1. Go to: https://www.python.org/downloads/
2. Click **"Download Python 3.12.x"** (or latest 3.x version)
3. Run the installer

### Step 1.2: CRITICAL - Installation Options
✅ **CHECK "Add Python to PATH"** (at bottom of installer)
✅ Click **"Install Now"**

![Important checkbox at bottom of installer]

### Step 1.3: Verify Installation
1. Press `Windows Key + R`
2. Type: `cmd` and press Enter
3. In the Command Prompt, type:
```bash
python --version
```
Should show: `Python 3.12.x` (or your version)

4. Type:
```bash
pip --version
```
Should show: `pip 24.x.x`

✅ If both work, Python is installed correctly!

❌ If "python is not recognized":
   - Restart your computer
   - Or manually add to PATH (see Troubleshooting section)

---

## Part 2: Install VS Code (5 minutes)

### Step 2.1: Download VS Code
1. Go to: https://code.visualstudio.com/
2. Click **"Download for Windows"**
3. Run the installer (use default options)

### Step 2.2: Install Python Extension
1. Open VS Code
2. Click the **Extensions** icon on left sidebar (or press `Ctrl+Shift+X`)
3. Search for: **"Python"**
4. Install the one by **Microsoft** (should be first result)
5. Wait for it to install (shows "Installing..." then changes to "Installed")

### Step 2.3: Install Additional Extensions (Optional but Recommended)
Search and install these:
- **"Pylance"** by Microsoft (better Python intelligence)
- **"Jupyter"** by Microsoft (if you change your mind about notebooks later)
- **"Python Indent"** (auto-formatting help)

---

## Part 3: Install Required Libraries (3 minutes)

### Step 3.1: Open Terminal in VS Code
1. In VS Code, press: **Ctrl + `** (backtick key, usually above Tab)
2. Or go to: **Terminal → New Terminal**

You should see a terminal panel at the bottom showing:
```
PS C:\Users\YourName>
```

### Step 3.2: Install Libraries
Copy and paste this entire command, then press Enter:

```bash
pip install matplotlib seaborn numpy pandas scipy
```

This installs:
- `matplotlib` - for creating graphs
- `seaborn` - for beautiful visualizations
- `numpy` - for numerical operations
- `pandas` - for data analysis
- `scipy` - for statistics

⏳ Takes 2-3 minutes to download and install

✅ When done, you'll see: "Successfully installed..."

### Step 3.3: Verify Installation
Type in the terminal:
```bash
python -c "import matplotlib; import seaborn; import numpy; print('All libraries installed!')"
```

Should print: `All libraries installed!`

---

## Part 4: Set Up Your Project (5 minutes)

### Step 4.1: Create Project Folder
1. Open File Explorer
2. Navigate to somewhere convenient (e.g., `C:\Users\YourName\Documents\`)
3. Create new folder: **"ComorbidityAnalysis"**

### Step 4.2: Open Folder in VS Code
1. In VS Code: **File → Open Folder**
2. Select your **ComorbidityAnalysis** folder
3. Click **"Select Folder"**

VS Code will now show this folder in the left sidebar (Explorer)

### Step 4.3: Download the Python Scripts

**Option A: If you can download from our conversation**
1. Download these files from earlier:
   - `process_large_dataset.py`
   - `generate_visualizations.py`
   - `QUICK_START.md`
2. Move them to your `ComorbidityAnalysis` folder

**Option B: Create manually in VS Code**
1. In VS Code, click **"New File"** icon in Explorer panel
2. Name it: `process_large_dataset.py`
3. Copy the entire code from the file I created earlier and paste it in
4. Press `Ctrl+S` to save
5. Repeat for other files

### Step 4.4: Add Your Data File
1. Download your PubMed data file (500MB MEDLINE format)
2. Move it to your `ComorbidityAnalysis` folder
3. Rename it to something simple like: `pubmed_data.txt`

Your folder structure should now look like:
```
ComorbidityAnalysis/
├── process_large_dataset.py
├── generate_visualizations.py
├── QUICK_START.md
└── pubmed_data.txt (your 500MB file)
```

---

## Part 5: Running Your Analysis (Easy!)

### Step 5.1: Select Python Interpreter
1. Press `Ctrl+Shift+P` (opens Command Palette)
2. Type: "Python: Select Interpreter"
3. Choose the Python version you installed (e.g., "Python 3.12.x")

### Step 5.2: Run the Analysis

**Method 1: Using Terminal (Recommended)**
1. Open terminal in VS Code: `Ctrl + backtick`
2. Type:
```bash
python process_large_dataset.py pubmed_data.txt
```
3. Press Enter

**Method 2: Using Run Button**
1. Open `process_large_dataset.py` in VS Code
2. Modify the last lines to add your filename:
```python
if __name__ == "__main__":
    import sys
    sys.argv = ['process_large_dataset.py', 'pubmed_data.txt']
    main()
```
3. Press `F5` or click the ▶️ Run button at top right

### Step 5.3: What You'll See
```
======================================================================
GENDERED INNOVATIONS IN COMORBIDITY RESEARCH
Large-Scale PubMed Data Processor
======================================================================

Input file: pubmed_data.txt
File size: 487.3 MB
Estimated time: 10-15 minutes

Proceed with analysis? (yes/no): yes

Starting to parse pubmed_data.txt
This may take 5-10 minutes for 500MB file...
  Processed 1,000 entries, found 892 comorbidity papers...
  Processed 2,000 entries, found 1,784 comorbidity papers...
  ...
```

⏳ **Go get coffee!** This takes 10-15 minutes for 500MB

✅ **When done:**
```
✓ Analysis complete!
  Results saved to: ./analysis_output/
  - final_report.json (summary statistics)
```

### Step 5.4: Generate Visualizations
In the same terminal, type:
```bash
python generate_visualizations.py
```

Takes 1-2 minutes, creates 5 PNG files in `./analysis_output/figures/`

---

## Part 6: Viewing Your Results

### Step 6.1: Open Results Folder
1. In VS Code Explorer (left sidebar)
2. You'll now see: `analysis_output/` folder
3. Expand it to see:
   - `final_report.json`
   - `figures/` folder with PNG images

### Step 6.2: View JSON Report
1. Click `final_report.json` in VS Code
2. VS Code will show formatted JSON
3. Press `Ctrl+F` to search for specific terms

**Better viewing (optional):**
- Install extension: "JSON Viewer"
- Or open in browser: right-click file → "Reveal in File Explorer" → drag to Chrome

### Step 6.3: View Visualizations
1. Navigate to `analysis_output/figures/`
2. Double-click any PNG file
3. Opens in Windows Photo Viewer or your default image app

**Better viewing in VS Code:**
- Install extension: "Image Preview"
- Then you can view PNGs directly in VS Code

---

## Part 7: Interactive Work (VS Code Features)

### Run Code Line-by-Line (Interactive Mode)

1. **Install Jupyter extension** (if not already)
2. Add this to top of any Python file:
```python
# %%
# This creates an interactive cell
```

3. You'll see "Run Cell" appear above the `# %%`
4. Click it to run just that section

**Example - Explore Results Interactively:**
Create new file: `explore_results.py`

```python
# %%
# Load and explore results
import json

with open('./analysis_output/final_report.json', 'r') as f:
    report = json.load(f)

# %%
# Look at summary
summary = report['summary']
print(f"Total papers: {summary['total_papers']:,}")
print(f"Mixed teams: {summary['percentages']['mixed_pct']:.1f}%")

# %%
# Check specific year
year_2020 = report['temporal_trends']['2020']
print(f"2020 had {year_2020['total']} papers")
print(f"Mixed teams: {year_2020['mixed']} ({100*year_2020['mixed']/year_2020['total']:.1f}%)")

# %%
# Find most novel team type
novelty = report['novelty_analysis']
print(f"Novel discoveries: {novelty['total_novel_combinations']:,}")
for team, count in novelty['by_team_type'].items():
    pct = novelty['percentages'][team]
    print(f"  {team}: {count} ({pct:.1f}%)")
```

Run each cell (Shift+Enter) to explore interactively!

### Debugging

**Set Breakpoints:**
1. Click left of line number (red dot appears)
2. Press `F5` to debug
3. Code pauses at breakpoint
4. Hover over variables to see values
5. Press `F10` to step through line by line

**View Variables:**
When debugging, left sidebar shows:
- Variables and their values
- Call stack
- Watch expressions

---

## Part 8: Working with Large Files

### If VS Code Slows Down with 500MB File

**Don't open the data file directly in VS Code!**

Instead, preview in terminal:
```bash
# First 100 lines
python -c "with open('pubmed_data.txt', 'r') as f: print(''.join(f.readline() for _ in range(100)))"

# Search for specific PMID
python -c "import sys; [print(line, end='') for line in open('pubmed_data.txt') if 'PMID- 12345678' in line]"
```

### Monitor Progress

Create: `monitor_progress.py`
```python
import os
import time

while True:
    if os.path.exists('./analysis_output'):
        files = os.listdir('./analysis_output')
        checkpoints = [f for f in files if f.startswith('checkpoint')]
        print(f"\rCheckpoints: {len(checkpoints)}", end='', flush=True)
    time.sleep(5)
```

Run in separate terminal while analysis runs.

---

## Part 9: Keyboard Shortcuts (Speed up your work!)

### Essential VS Code Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + P` | Quick open file |
| `Ctrl + Shift + P` | Command palette |
| `Ctrl + backtick` | Toggle terminal |
| `Ctrl + B` | Toggle sidebar |
| `Ctrl + /` | Comment/uncomment line |
| `Ctrl + D` | Select next occurrence |
| `Ctrl + Shift + K` | Delete line |
| `Alt + Up/Down` | Move line up/down |
| `F5` | Start debugging |
| `Shift + F5` | Stop debugging |
| `Ctrl + Shift + F` | Search in all files |

### Python-Specific

| Shortcut | Action |
|----------|--------|
| `Shift + Enter` | Run cell (if using cells) |
| `Ctrl + Shift + Enter` | Run entire file |
| `F9` | Toggle breakpoint |
| `F10` | Step over (debugging) |
| `F11` | Step into (debugging) |

---

## Part 10: Tips & Best Practices

### Organizing Your Work

**Create a scripts folder:**
```
ComorbidityAnalysis/
├── scripts/
│   ├── process_large_dataset.py
│   ├── generate_visualizations.py
│   └── explore_results.py
├── data/
│   └── pubmed_data.txt
├── output/
│   └── (analysis results will go here)
└── docs/
    ├── QUICK_START.md
    └── research_protocol.md
```

**Modify scripts to use new structure:**
Change output paths:
```python
analyzer = BatchAnalyzer(output_dir='../output/analysis_output')
```

### Git Version Control (Optional)

1. Install Git: https://git-scm.com/download/win
2. In VS Code, click Source Control icon (left sidebar)
3. Initialize repository
4. Add `.gitignore` file:
```
pubmed_data.txt
*.pkl
analysis_output/
__pycache__/
*.pyc
```
5. Commit your scripts (but not the large data file!)

### Remote Development (Optional)

If processing is slow:
1. Install "Remote - SSH" extension
2. Connect to a server/cloud VM
3. Run analysis there (faster)
4. Download only the results

---

## Troubleshooting

### "Python not recognized"

**Fix PATH manually:**
1. Search Windows: "Environment Variables"
2. Click "Environment Variables" button
3. Under "System variables", find "Path"
4. Click "Edit"
5. Click "New" and add:
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python312\`
   - `C:\Users\YourName\AppData\Local\Programs\Python\Python312\Scripts\`
6. Click OK, restart VS Code

### "Module not found: matplotlib"

Terminal might be using different Python. Check:
```bash
where python
python --version
pip --version
```

If multiple Pythons, specify which pip:
```bash
python -m pip install matplotlib seaborn numpy pandas
```

### "Permission denied" when running script

Right-click the .py file → Properties → Unblock

### Analysis is very slow (>30 minutes)

**Speed it up:**
1. Increase batch size in script:
```python
analyzer.process_dataset(filepath, batch_size=5000)  # was 1000
```

2. Close other applications
3. Disable antivirus temporarily (can slow file reading)

### "Out of memory" error

Process in chunks:
```bash
# Split data file first (install Git to get split command)
# Or use Python:
python -c "
lines_per_file = 50000
with open('pubmed_data.txt', 'r') as f:
    for i, line in enumerate(f):
        file_num = i // lines_per_file
        with open(f'chunk_{file_num}.txt', 'a') as out:
            out.write(line)
"
```

Then process each chunk separately.

### VS Code is slow/laggy

Settings (Ctrl+,):
- Disable: "Python > Linting: Enabled"
- Disable: "Files: Auto Save" (change to "onFocusChange")
- Enable: "Files: Exclude" for `*.pkl` files

---

## Quick Reference Card

**Setup:**
```bash
# Install libraries
pip install matplotlib seaborn numpy pandas scipy

# Verify
python --version
pip list
```

**Run Analysis:**
```bash
# Navigate to project folder
cd C:\Users\YourName\Documents\ComorbidityAnalysis

# Run main analysis
python process_large_dataset.py pubmed_data.txt

# Generate figures
python generate_visualizations.py
```

**Check Results:**
```bash
# Open in VS Code
code analysis_output/final_report.json

# Or view in terminal
python -c "import json; print(json.dumps(json.load(open('analysis_output/final_report.json')), indent=2))"
```

---

## Next Steps After Setup

1. ✅ Run analysis on your 500MB file
2. 📊 Review visualizations
3. 📈 Explore results interactively
4. 📝 Export findings for paper/presentation
5. 🔄 Iterate with different analyses

---

## Support Resources

**VS Code:**
- Official docs: https://code.visualstudio.com/docs/python/python-tutorial
- Python in VS Code video: https://www.youtube.com/watch?v=7EXd4_ttIuw

**Python:**
- Python.org tutorials: https://docs.python.org/3/tutorial/
- Real Python: https://realpython.com/

**This Project:**
- Read `QUICK_START.md` for analysis details
- Read `research_protocol.md` for methodology

---

**You're all set! Time to discover how gender diversity drives innovation! 🚀**
