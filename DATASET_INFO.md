# Dataset Information — UCI Student Performance

## Source

- **Name:** Student Performance Data Set
- **Repository:** UCI Machine Learning Repository
- **URL:** https://archive.ics.uci.edu/ml/datasets/Student+Performance
- **Direct Download:** https://archive.ics.uci.edu/ml/machine-learning-databases/00320/student.zip
- **Authors:** Paulo Cortez, University of Minho, Guimarães, Portugal
- **Year:** 2014

## Citation

P. Cortez and A. Silva. *Using Data Mining to Predict Secondary School Student Performance.*
In A. Brito and J. Teixeira (Eds.), Proceedings of 5th FUture BUsiness TEChnology Conference
(FUBUTEC 2008), pp. 5-12, Porto, Portugal, April, 2008, EUROSIS, ISBN 978-9077381-39-7.

## Dataset Description

This dataset contains student achievement in secondary education at two Portuguese schools.
The data was collected using school reports and questionnaires. Two courses are available:
- **student-mat.csv** — Mathematics (395 students) ← **Used in this project**
- **student-por.csv** — Portuguese (649 students)

## File Used

**student-mat.csv** (Mathematics course) — 395 rows × 33 columns, semicolon-separated.

## Target Variable

| Variable | Description | Range |
|----------|-------------|-------|
| **G3** | Final grade | 0 to 20 |

For this project, G3 is converted into three performance categories:

| Category | Grade Range | Description |
|----------|-------------|-------------|
| **Low** | 0 – 9 | At risk, needs academic support |
| **Medium** | 10 – 14 | Average performance |
| **High** | 15 – 20 | Good performance |

## Feature Descriptions

### Demographic Attributes
| Feature | Description | Values |
|---------|-------------|--------|
| school | Student's school | GP (Gabriel Pereira), MS (Mousinho da Silveira) |
| sex | Student's sex | F (female), M (male) |
| age | Student's age | 15 to 22 |
| address | Home address type | U (urban), R (rural) |
| famsize | Family size | LE3 (≤3), GT3 (>3) |
| Pstatus | Parent's cohabitation status | T (together), A (apart) |

### Family & Education
| Feature | Description | Values |
|---------|-------------|--------|
| Medu | Mother's education | 0: none, 1: primary (4th grade), 2: 5th–9th grade, 3: secondary, 4: higher |
| Fedu | Father's education | Same scale as Medu |
| Mjob | Mother's job | teacher, health, services, at_home, other |
| Fjob | Father's job | Same categories as Mjob |
| guardian | Student's guardian | mother, father, other |
| reason | Reason to choose this school | home, reputation, course, other |

### School & Study
| Feature | Description | Values |
|---------|-------------|--------|
| traveltime | Home to school travel time | 1: <15 min, 2: 15–30 min, 3: 30–60 min, 4: >60 min |
| studytime | Weekly study time | 1: <2 hrs, 2: 2–5 hrs, 3: 5–10 hrs, 4: >10 hrs |
| failures | Number of past class failures | 0 to 4 |
| schoolsup | Extra educational support | yes, no |
| famsup | Family educational support | yes, no |
| paid | Extra paid classes | yes, no |
| activities | Extra-curricular activities | yes, no |
| nursery | Attended nursery school | yes, no |
| higher | Wants to take higher education | yes, no |
| internet | Internet access at home | yes, no |
| romantic | In a romantic relationship | yes, no |

### Social & Health
| Feature | Description | Values |
|---------|-------------|--------|
| famrel | Quality of family relationships | 1 (very bad) to 5 (excellent) |
| freetime | Free time after school | 1 (very low) to 5 (very high) |
| goout | Going out with friends | 1 (very low) to 5 (very high) |
| Dalc | Workday alcohol consumption | 1 (very low) to 5 (very high) |
| Walc | Weekend alcohol consumption | 1 (very low) to 5 (very high) |
| health | Current health status | 1 (very bad) to 5 (very good) |
| absences | Number of school absences | 0 to 93 |

### Period Grades
| Feature | Description | Values |
|---------|-------------|--------|
| G1 | First period grade | 0 to 20 |
| G2 | Second period grade | 0 to 20 |

## Limitations

1. **Small sample size:** Only 395 students from two schools in Portugal.
2. **Geographic bias:** Data comes from a specific region (Portugal), so patterns may not transfer to other countries/cultures.
3. **Temporal relevance:** Data was collected around 2005–2006; educational patterns may have changed.
4. **Feature completeness:** Important factors like learning disabilities, teaching quality, and socioeconomic status in detail are not included.
5. **Self-reported data:** Some features (alcohol consumption, study time) are self-reported and may be inaccurate.
6. **Class imbalance:** The "High" performance category has fewer samples than "Low" and "Medium".

## Download Instructions

The training script downloads the dataset automatically. If you need to download manually:

1. Visit https://archive.ics.uci.edu/ml/machine-learning-databases/00320/
2. Download `student.zip`
3. Extract `student-mat.csv` into the `data/` folder
4. Ensure the file uses semicolons (`;`) as delimiters
