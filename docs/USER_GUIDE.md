# 🎓 Capstone Placement App - Quick Start Guide for ECCS Chair

## 🌐 Access the Web App

### Option 1: Use the Public Web App (Easiest)
1. Open your browser and go to:
   ```
   https://yourusername-datadivas-lena.streamlit.app/
   ```
   (This URL will be provided once deployed)

2. No installation needed! Just start using it.

### Option 2: Run Locally
If you have Python installed:
1. Download or clone the project
2. Open Command Prompt / Terminal
3. Navigate to the project folder
4. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```
5. Open `http://localhost:8501` in your browser

## 📋 How to Use the App

### Step 1: Enter Project Data

In the **left panel** "Project Capacities", enter your projects:

```
Project Name,Capacity,Major1,Major2,...
```

**Example:**
```
Project Apollo,4,CS,CpE,EE
Project Atlas,4,CS,EE
Project Beacon,5,CS,CpE
Project Cypress,4,CpE,EE
```

**Rules:**
- Capacity must be between 4 and 6
- Valid majors: CS, CpE, EE
- One project per line
- Format: `Name,Capacity,Major1,Major2,...`

**Or upload a CSV file:**
- Click "Upload Projects CSV"
- Select a file with columns: Project, Capacity, Allowed Majors

### Step 2: Enter Student Rankings

In the **right panel** "Student Rankings", enter student preferences:

```
Student Name (Major): Project1, Project2, Project3
```

**Example:**
```
Alice (CS): Project Apollo, Project Atlas, Project Beacon
Ben (CpE): Project Atlas, Project Cypress, Project Apollo
Carmen (EE): Project Beacon, Project Apollo, Project Atlas
Diana (CpE): Project Cypress, Project Atlas, Project Apollo
```

**Rules:**
- Include student's major in parentheses
- Valid majors: CS, CpE, EE
- List projects in order of preference (1st choice first)
- Separate projects with commas
- One student per line

**Or upload a CSV file:**
- Click "Upload Students CSV"
- Select a file with columns: Student, Major, Rankings

### Step 3: Run the Assignment

1. Click the **"🚀 Run Assignment"** button
2. Wait for the optimization to complete (10-30 seconds)
3. Results will appear on the right side

### Step 4: Review Results

You'll see three sections:

#### 📊 Project Assignments
A table showing each student's assignment:
| Student | Major | Assigned Project |
|---------|-------|------------------|
| Alice   | CS    | Project Apollo   |

#### 📈 Assignment Quality Metrics
Shows how well students got their preferred projects:
- 1st choice: X%
- 2nd choice: X%
- 3rd choice: X%

And project compositions showing major diversity:
| Project | Total | Composition |
|---------|-------|-------------|
| Apollo  | 4     | CS: 1, CpE: 1, EE: 2 |

#### 📋 Full Assignment Report
Detailed report grouped by project.

### Step 5: Download Results

Click **"📥 Download CSV"** to save results as a spreadsheet:
```
Student,Major,Assigned Project,Rank Assigned
Alice,CS,Project Apollo,Choice #1
Ben,CpE,Project Atlas,Choice #1
Carmen,EE,Project Beacon,Choice #1
Diana,CpE,Project Cypress,Not in rankings
```

## 🔑 Key Features

✅ **No installation needed** - Works in any web browser
✅ **CSV import/export** - Easy data entry and results sharing
✅ **Quality metrics** - See how satisfied students are
✅ **Fair algorithm** - Uses advanced optimization to maximize happiness
✅ **Diverse teams** - Encourages mixed-major project teams
✅ **Clear constraints**:
- Projects must have 0 or 4-6 students (no partial teams)
- Only students with appropriate major can join projects

## ⚠️ Important Rules

### Project Capacity (Nixing Rule)
- **Every project must have:**
  - 0 students (empty), OR
  - 4-6 students (valid team)
- Partial teams (1-3 students) are not allowed
- This ensures balanced team sizes

### Student-Project Matching
- Students can only join projects that accept their major
- If a student has no valid project slots, they remain unassigned
- Unassigned students will show "Unassigned" in the result

### Assignment Quality
The algorithm prioritizes:
1. **Fairness** - Honor student preferences (1st choice best, 6th choice acceptable)
2. **Diversity** - Encourage mixed-major teams
3. **Capacity** - Respect project capacities and team size rules

## 🎯 Example Workflow

### Scenario: 4 Projects, 12 Students

**Input:**
- 4 projects with capacity 4, 4, 5, and 4
- 12 students with ranked preferences

**Process:**
- App optimizes assignments to minimize unhappiness
- Enforces team sizes of 4-6 per project
- Ensures diverse major representation

**Output:**
- Project 1: 4 students (2 CS, 1 CpE, 1 EE)
- Project 2: 4 students (2 CS, 2 EE)
- Project 3: 4 students (1 CS, 2 CpE, 1 EE)
- Project 4: 0 students (empty)

## 💡 Tips

1. **Sample data is pre-filled**: Click "🚀 Run Assignment" to see it work!

2. **Upload CSVs**: If you have data in Excel, export as CSV and upload

3. **Clear output**: Click "🗑️ Clear Output" to start over

4. **Download results**: Always save results as CSV for your records

5. **Try different inputs**: Experiment to see how the algorithm handles different scenarios

## 🆘 Troubleshooting

### "Error: Input Error"
- Check your format: `Project Name,Capacity,Majors`
- For students: `Name (Major): Projects`
- Capacity must be 4-6
- Majors must be: CS, CpE, or EE

### "Error: Unrecognized projects"
- Student ranked a project that doesn't exist
- Check spelling matches exactly

### "Some students are unassigned"
- Not enough projects with appropriate majors
- Some students' rankings may not match available projects
- Try adjusting project capacities or availability

### App is slow to load
- First run takes 10-30 seconds (normal, due to optimization)
- Subsequent runs in same session are faster

### "Cannot upload CSV"
- Verify it's a .csv file
- Check headers: "Project", "Capacity", "Student", "Major", "Rankings"
- Ensure no special characters in filenames

## 📚 Need Help?

- **For app issues**: Check that your data format matches the examples
- **For optimization questions**: See README.md for algorithm details
- **For deployment**: See DEPLOYMENT.md for server setup

## 🚀 Ready to Deploy?

Once you're happy with the app:

1. **Share the public URL** with students/faculty
2. **No downloads needed** - everyone just clicks the link
3. **Results are always saved** - download CSV after each run

**That's it! You now have a cloud-based capstone assignment system.** 🎉
