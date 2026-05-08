# Team Contributions

## Project: Spotify Trends Dashboard

### Team Member Roles and Responsibilities

---

## [Team Member 1 Name] - Data Engineering Lead

**Primary Responsibilities:**
- Designed and implemented the 6-tier year extraction cascade
- Developed data preprocessing pipeline in `five_a_data_prep.ipynb`
- Managed API integrations (Spotify Web API, MusicBrainz API)
- Created data cleaning and validation logic

**Key Contributions:**
- Built fault-tolerant data extraction system with multiple fallback mechanisms
- Implemented OAuth2 authentication for Spotify API access
- Developed local caching strategy to minimize API calls
- Engineered `Popularity_Category` feature for categorical analysis
- Ensured data quality through rigorous validation rules

**Code Sections:**
- `five_a_data_prep.ipynb`: Complete ETL pipeline (cells 1-15)
- `app.py`: `_load_data()` function (lines 47-140)
- External API functions: `get_spotify_access_token()`, `fetch_spotify_years()`, `fetch_musicbrainz_year()`

---

## [Team Member 2 Name] - Visualization & Dashboard Lead

**Primary Responsibilities:**
- Designed and implemented all 14 chart visualizations
- Created responsive dashboard layout using Dash
- Developed interactive controls and callbacks
- Established color scheme and styling guidelines

**Key Contributions:**
- Implemented charts covering all 9 weeks of course requirements (plus 5 bonus charts)
- Created unified `_style()` function for consistent chart formatting
- Designed dark theme UI with accessibility considerations
- Built 4 interactive controls (dropdown, range slider, radio items, search input)
- Integrated KPI cards and insight generation

**Code Sections:**
- `app.py`: Chart functions `chart_1()` through `chart_14()` (lines 207-440)
- `app.py`: Dashboard layout (lines 473-852)
- `app.py`: Callback functions (lines 854-938)

---

## [Team Member 3 Name] - Documentation & Quality Assurance Lead

**Primary Responsibilities:**
- Authored comprehensive README.md documentation
- Created data dictionary and schema documentation
- Performed testing and validation of dashboard functionality
- Prepared submission materials and checklists

**Key Contributions:**
- Documented technological rationale and project architecture
- Created detailed setup and execution instructions
- Mapped all chart implementations to weekly requirements
- Developed pre-submission verification checklist
- Ensured academic integrity compliance

**Deliverables:**
- `Readme.md`: Project overview, tech stack, application flow (180+ lines)
- `COVERAGE_CHECKLIST.md`: Comprehensive requirements mapping
- Data dictionary with 18-column schema documentation
- Testing protocols and verification scripts

---

## Collaborative Efforts

### Joint Design Decisions
- **Color Scheme**: Selected teal (#14B8A6) and orange (#F97316) for accessibility and brand alignment
- **Chart Selection**: Collective decision to exceed requirements with 14 charts vs. 9 required
- **Architecture**: Agreed on modular function design for maintainability
- **Data Pipeline**: Collaborative design of 6-tier cascade approach

### Code Review Process
- All code reviewed by at least two team members
- Weekly sync meetings to track progress and resolve blockers
- Shared understanding of all code sections for Q&A preparation

### Meeting Notes Summary
- **Week 1**: Project scoping, dataset selection, role assignment
- **Week 2-3**: Data pipeline development, API integration
- **Week 4-6**: Chart implementation, iterative design
- **Week 7-8**: Dashboard integration, interactivity features
- **Week 9**: Documentation, testing, final polish

---

## Individual Learning Outcomes

### Team Member 1
- Mastered complex API orchestration with rate limiting and error handling
- Gained expertise in Pandas data transformation techniques
- Learned OAuth2 authentication flows

### Team Member 2
- Developed proficiency in Plotly Express and Dash frameworks
- Understood principles of effective data visualization
- Learned responsive web design patterns

### Team Member 3
- Improved technical writing and documentation skills
- Gained understanding of data visualization best practices
- Learned project management and quality assurance processes

---

## Contact Information

| Team Member | Email | GitHub |
|-------------|-------|--------|
| [Name 1] | [email1@university.edu] | [@github1] |
| [Name 2] | [email2@university.edu] | [@github2] |
| [Name 3] | [email3@university.edu] | [@github3] |

---

## Statement of Originality

We hereby certify that:
- All code presented in this project is our original work
- Any external resources or tutorials used have been properly cited
- No code has been shared with or copied from other teams
- All team members can explain every line of code during Q&A
- AI tool usage (if any) has been documented appropriately

**Signatures:**

_________________________  Date: ___________  
[Team Member 1 Name]

_________________________  Date: ___________  
[Team Member 2 Name]

_________________________  Date: ___________  
[Team Member 3 Name]

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Course**: [Course Name/Number]  
**Instructor**: [Instructor Name]
