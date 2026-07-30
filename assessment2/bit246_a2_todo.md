# BIT246 Assessment 2 — Software Project Todo List
**Dataset:** Health Insurance Cross Sell Prediction (`hicsp.csv`) | **Due:** 4 October 2026 | **Weight:** 35%

---

## 1. Dataset Selection ✅ (done)
- [x] Dataset chosen: Health Insurance Cross Sell Prediction (`hicsp.csv`, ~381k rows)
- [x] Target confirmed: `Response` (0/1 — did customer buy vehicle insurance)
- [ ] Write a short justification paragraph for why this dataset was chosen

## 2. Business Problem & Scope (5 marks)
- [ ] Define the business problem (e.g., predicting which existing health insurance customers are likely to buy vehicle insurance, to target cross-sell campaigns efficiently)
- [ ] State what's in-scope (e.g., binary prediction of purchase likelihood using demographic/policy features)
- [ ] State what's out-of-scope (e.g., pricing optimization, claims processing, multi-product recommendations)
- [ ] Justify the scope against the dataset and project goals

## 3. Data Exploration (20 marks)
- [ ] Load `hicsp.csv`, inspect shape, dtypes, and summary stats
- [ ] Chart: missing/null values
- [ ] Chart: class balance of `Response` (this dataset is known to be imbalanced — discuss it)
- [ ] Chart: distributions of key attributes (Age, Annual_Premium, Vintage — histograms/boxplots)
- [ ] Chart: correlation heatmap of numeric features
- [ ] Write up findings and justify what each chart shows

## 4. Data Cleaning & Transformation (20 marks)
- [ ] Apply **two** cleaning techniques (e.g., impute/handle missing values, remove outliers/inconsistencies in Annual_Premium)
- [ ] Apply **one** transformation technique (e.g., scale/normalize numeric features, encode categorical variables like Gender, Vehicle_Age, Vehicle_Damage)
- [ ] Justify every cleaning/transformation step in writing

## 5. Predictive Modelling (20 marks)
- [ ] Split `hicsp.csv` into your own train/test sets
- [ ] Implement Random Forest classifier (variation 1 — baseline)
- [ ] Implement Random Forest classifier (variation 2 — e.g., tuned hyperparameters, class-weight balancing for imbalance, or different feature set)
- [ ] Evaluate both with accuracy, precision, recall, F1-score, ROC-AUC
- [ ] Justify model/parameter choices for each variation

## 6. Results & Conclusion (30 marks — biggest weight)
- [ ] Compare the two model variations against each other
- [ ] Discuss results in relation to the business problem and scope
- [ ] Write a clear, well-supported conclusion with recommendations

## 7. Report Writing (5 marks, ~2,000 words equivalent)
- [ ] Structure: Business Problem & Scope → Data Exploration → Data Cleaning & Transformation → Model Development & Evaluation → Conclusion
- [ ] Appendix: paste Python code with execution screenshots
- [ ] Add references/citations for any external sources used
- [ ] Save as MS Word (.docx), submit via Turnitin on Moodle

## 8. Before Submitting
- [ ] Confirm code runs end-to-end with no errors
- [ ] Prep for demonstration/Q&A (grade gets scaled down based on how well you answer questions live)
- [ ] Double-check `test.csv` and `sample_submission.csv` were NOT used (Kaggle competition artifacts only — not needed here)

---
*Note: this list currently reflects working solo. Update file naming (e.g., `BIT2460012_A2`) once/if a group code is assigned.*
