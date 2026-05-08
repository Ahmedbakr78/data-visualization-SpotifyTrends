# Citations & References

## Dataset Sources

### Primary Dataset
**Spotify Tracks Dataset**
- **Source**: Kaggle / Spotify API
- **URL**: [Insert actual URL if known]
- **Access Date**: [Date downloaded]
- **License**: [Specify license if known]
- **Description**: Raw dataset containing 114,000+ tracks with audio features including danceability, energy, valence, tempo, loudness, acousticness, speechiness, instrumentalness, liveness, and popularity metrics.

### Supplementary Data Sources

**Spotify Web API**
- **Provider**: Spotify AB
- **Documentation**: https://developer.spotify.com/documentation/web-api
- **Usage**: High-confidence release year extraction via album metadata
- **Authentication**: OAuth2 Client Credentials Flow
- **Rate Limits**: As per Spotify API terms of service

**MusicBrainz API**
- **Provider**: MetaBrainz Foundation
- **Documentation**: https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2
- **Usage**: Fallback release year extraction via recording metadata
- **Rate Limiting**: 1 request per second (implemented in code)
- **License**: CC0 1.0 Universal (Public Domain Dedication)

---

## External Libraries & Frameworks

### Core Dependencies

**Dash**
- **Version**: >=2.18.2
- **Authors**: Plotly Inc.
- **URL**: https://dash.plotly.com/
- **License**: MIT License
- **Usage**: Web framework for analytical dashboard construction

**Plotly Express**
- **Version**: >=5.24.1
- **Authors**: Plotly Inc.
- **URL**: https://plotly.com/python/plotly-express/
- **License**: MIT License
- **Usage**: All 14 chart visualizations

**Pandas**
- **Version**: >=2.2.2
- **Authors**: pandas Development Team
- **URL**: https://pandas.pydata.org/
- **License**: BSD 3-Clause License
- **Usage**: Data manipulation, DataFrame transformations, cleaning operations

**NumPy**
- **Version**: >=2.1.1
- **Authors**: NumPy Developers
- **URL**: https://numpy.org/
- **License**: BSD 3-Clause License
- **Usage**: Numerical operations, mathematical coercions, NaN handling

**JupyterLab**
- **Version**: >=4.2.5
- **Authors**: Project Jupyter
- **URL**: https://jupyterlab.readthedocs.io/
- **License**: BSD 3-Clause License
- **Usage**: Interactive development environment for data preparation notebook

---

## Tutorials & Educational Resources

### Course Materials
**[Course Name] Lecture Notes**
- **Institution**: [University Name]
- **Instructor**: [Instructor Name]
- **Semester**: [Semester/Year]
- **Topics Applied**:
  - Week 1-2: Comparison charts (column, bar, stacked, clustered)
  - Week 3-4: Relationship charts (scatter, bubble)
  - Week 5-7: Distribution charts (histogram, box, violin)
  - Week 8-9: Time-series charts (line, area)
  - Dashboard design principles
  - Color theory and accessibility

### Online Documentation
**Plotly Python Graphing Library**
- **URL**: https://plotly.com/python/
- **Specific Guides Used**:
  - Bar Charts: https://plotly.com/python/bar-charts/
  - Scatter Plots: https://plotly.com/python/line-and-scatter/
  - Heatmaps: https://plotly.com/python/heatmaps/
  - Subplots: https://plotly.com/python/subplots/

**Dash User Guide**
- **URL**: https://dash.plotly.com/
- **Specific Sections**:
  - Callbacks: https://dash.plotly.com/basic-callbacks
  - Layout: https://dash.plotly.com/layout
  - Styling: https://dash.plotly.com/external-resources

**Pandas Documentation**
- **URL**: https://pandas.pydata.org/docs/
- **Key Functions Referenced**:
  - `pd.to_numeric()`: Data type conversion
  - `pd.cut()`: Binning and segmentation
  - `groupby()`: Aggregation operations
  - `merge()`: DataFrame joins

---

## Code Inspiration & Patterns

### Design Patterns
**6-Tier Cascade Pattern**
- **Inspiration**: Multi-level fallback architecture common in distributed systems
- **Application**: Year extraction with progressive confidence levels
- **Original Implementation**: Custom implementation for this project

**Dashboard Layout Pattern**
- **Inspiration**: Modern dashboard design (Grid-based, responsive)
- **Framework**: CSS Grid with auto-fit and minmax()
- **Customization**: Dark theme with Spotify-inspired color palette

**Styling Utility Function**
- **Pattern**: DRY (Don't Repeat Yourself) principle
- **Implementation**: `_style()` function for consistent chart formatting
- **Benefit**: Single source of truth for visual properties

### Color Palette Selection
**Primary Colors**
- Teal (#14B8A6): Selected for high contrast and accessibility
- Orange (#F97316): Complementary accent color
- Reference: Tailwind CSS color palette (open source)

**Accessibility Considerations**
- WCAG 2.1 AA compliance for text contrast
- Colorblind-friendly palette selection
- Reference: ColorBrewer 2.0 (https://colorbrewer2.org/)

---

## AI Tool Usage Disclosure

### AI-Assisted Development
**Tools Used**: [Specify if any AI tools were used, e.g., GitHub Copilot, ChatGPT, etc.]

**Extent of Usage**:
- [ ] Code suggestions and completions
- [ ] Debugging assistance
- [ ] Documentation generation
- [ ] Testing scenario generation
- [ ] None (fully manual implementation)

**Human Oversight**:
- All AI-generated code reviewed and understood by team members
- Manual verification of all algorithmic logic
- Custom adaptation to project-specific requirements

---

## Academic Integrity Statement

We affirm that:
1. All code implementations are original work by team members
2. External resources are properly cited in this document
3. No code has been copied from other students or teams
4. All team members can explain every line of code
5. Any AI tool usage has been disclosed above

This project adheres to [University Name]'s Academic Integrity Policy.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | [Date] | Initial citations document |

---

**Prepared By**: [Team Name/Number]  
**Course**: [Course Name/Number]  
**Submission Date**: [Date]
