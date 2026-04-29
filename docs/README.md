# DataDivas

DataDivas is a capstone project assignment system that helps the ECCS chair map students to capstone projects using student-ranked project preferences. It implements an optimization algorithm using Google OR-Tools (CP-SAT) to achieve optimal assignments while respecting project capacity constraints.

## What it does

- **Accepts project data**: List of projects with capacities constrained to 4-6 students per project (enforced by ECCS guidelines).
- **Accepts student preferences**: Student rankings for projects in order of preference, including major information.
- **Computes optimal assignments**: Uses Google OR-Tools CP-SAT solver to minimize overall "unhappiness" while honoring student preferences and respecting capacity limits.
- **Validates all input**: Ensures consistent data format, prevents duplicates, requires valid capacity ranges, and validates majors.
- **Enforces the Nixing Rule**: Ensures each project has either 0 students or between 4-6 students (no partial teams).
- **Exports results**: Save assignment results to CSV with each student's assigned project and ranking match quality.

## Features

- **Web-based interface (Streamlit)**: Cloud-deployable web app with public URL for easy access.
- **Optional desktop interface (Tkinter)**: Run locally as a desktop application.
- **Advanced optimization**: Uses OR-Tools CP-SAT with penalty system:
  - 1st choice = 1 point
  - 6th choice = 36 points
  - Unassigned = 10,000 points (heavily penalized)
- **Diversity penalties**: Detects and penalizes monochromatic projects (single major only).
- **Robust validation**: Clear error messages for invalid input formats.
- **Multiple import formats**: Load project and student data from CSV files or enter manually.
- **Preference tracking**: CSV export shows how well each student's assignment matches their ranked preferences.
- **Capacity enforcement**: Ensures no project exceeds its capacity and maintains minimum team size of 4 students.
- **Comprehensive testing**: Unit tests cover parsing logic, validation, and assignment correctness.

## Quick Start: Web App (Recommended)

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` in your browser.

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app" and select your repository
4. Select `streamlit_app.py` as the script path
5. Click "Deploy"

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Quick Start: Desktop App

1. Install Python 3.9+ if needed.
2. Open a terminal in this repository.
3. Install dependencies:

```bash
pip install ortools
```

4. Run the app:

```bash
python main.py
```

## Usage: Web App

1. Paste or upload project capacities:
   ```
   Project Name,Capacity,Major1,Major2,...
   Project Apollo,4,CS,CpE,EE
   ```

2. Paste or upload student rankings:
   ```
   Student Name (Major): Project1, Project2, ...
   Alice (CS): Project Apollo, Project Atlas, Project Beacon
   ```

3. Click "🚀 Run Assignment"

4. Review results in the dashboard:
   - Project Assignments table
   - Assignment Quality Metrics
   - Project Compositions
   - Full Assignment Report

5. Download results as CSV using "📥 Download CSV"

## Usage: Desktop App

1. Enter project capacities in the left panel using `Project Name,capacity` lines.
   - Capacities must be set between 4 and 6 inclusive.
2. Enter student rankings using `Student Name (major): Project 1, Project 2, ...` lines.
3. Optionally import project or student data from CSV using the provided buttons.
   - Projects CSV should include headers like `Project` and `Capacity`.
   - Students CSV should include headers like `Student` and `Rankings`.
4. Click `Run Assignment`.
5. Review the assignment results.
6. Export to CSV if desired—results will list each student with their assigned project.

## Example Output

```
Project Apollo: Alice (CS), Diana (CpE)
Composition: CS: 1, CpE: 1, EE: 2

Project Atlas: Ben (CpE), Frank (CS)
Composition: CS: 1, CpE: 1

Project Beacon: Carmen (EE)
Composition: EE: 1

Unassigned: Eve (CS)
```

## Testing

Run the unit tests with:

```bash
python -m unittest discover -s tests
```

## File layout

- **`streamlit_app.py`** — Web app entry point (main interface).
- **`main.py`** — Desktop app entry point (legacy).
- **`datadivas/assignment.py`** — Optimization logic (OR-Tools, parsing, validation).
- **`datadivas/gui.py`** — Desktop Tkinter interface (legacy).
- **`requirements.txt`** — Dependencies for web app.
- **`tests/test_assignment.py`** — Test coverage for parsing and assignment behavior.
- **`DEPLOYMENT.md`** — Deployment instructions for Streamlit Cloud.
- **`ROBOTS.md`** — AI/automation guidance.

## Algorithm Details

### Penalty System

The optimization minimizes total "unhappiness" using this penalty scale:
- **1st choice**: 1 point
- **2nd choice**: 4 points
- **3rd choice**: 9 points
- **4th choice**: 16 points
- **5th choice**: 25 points
- **6th choice**: 36 points
- **Not ranked**: 100 points
- **Unassigned**: 10,000 points

### Nixing Rule (Hard Constraint)

Each project must have:
- **0 students** (completely empty), OR
- **4-6 students** (valid team size)

No partial teams are allowed.

### Diversity Penalty (Soft Constraint)

- **Missing major**: 150 points per empty major slot in a project
- **Monochromatic project** (only one major): 5,000 points

### Major Eligibility (Hard Constraint)

Students can only be assigned to projects that accept their major:
- Valid majors: CS, CpE, EE

## Design notes

- The algorithm prioritizes minimizing student unhappiness while respecting all hard constraints.
- Diversity penalties encourage mixed-major teams.
- Students may remain unassigned when project capacity is insufficient or matching their preferences cannot satisfy constraints.
- The app uses Google OR-Tools CP-SAT solver for efficiency and correctness.
- The app can be extended with additional constraints or rules as needed.
