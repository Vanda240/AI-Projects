# Student College Admission Prediction (KNN, Random Forest, LSTM)

This project predicts whether a student **will go to college** using demographic, school, and family-related features. It compares three models:

- **K-Nearest Neighbors (KNN)** (tuned with GridSearchCV)
- **Random Forest (RF)** (tuned with GridSearchCV)
- **LSTM (Keras/TensorFlow)** (trained on reshaped tabular features)

It evaluates models using **Stratified 10-Fold Cross-Validation** and reports detailed classification and probability-based metrics.

---

## Repository Contents

- `Student College Admission Prediction.ipynb` — main notebook
- `Student College Admission Prediction_data.csv` — dataset
- `README.md` — project documentation
- `requirements.txt` — dependencies

---

## Dataset

**File:** `Student College Admission Prediction_data.csv`  
**Rows:** 1000  
**Target:** `will_go_to_college` (boolean)

**Columns:**
- `type_school` (categorical)
- `school_accreditation` (categorical)
- `gender` (categorical)
- `interest` (categorical)
- `residence` (categorical)
- `parent_age` (numeric)
- `parent_salary` (numeric)
- `house_area` (numeric)
- `average_grades` (numeric)
- `parent_was_in_college` (boolean)
- `will_go_to_college` (boolean target)

---

## Methodology

### 1) Preprocessing
- Label encoding for categorical columns:
  - `type_school, school_accreditation, gender, interest, residence, parent_was_in_college, will_go_to_college`
- Feature scaling using **StandardScaler**
- Train/test split: **90% / 10%** with stratification
- Cross-validation: **StratifiedKFold(n_splits=10, shuffle=True, random_state=42)**

### 2) Hyperparameter Tuning (GridSearchCV)
**KNN**
- `n_neighbors`: 3 to 19 (odd numbers)

**Random Forest**
- `n_estimators`: 50 to 200 (step 25)
- `min_samples_split`: [5, 10, 15, 20]

### 3) Models
**KNN (sklearn)**  
**Random Forest (sklearn)**  
**LSTM (Keras)**
- LSTM(64, activation='relu')
- Dense(1, activation='sigmoid')
- loss: binary_crossentropy, optimizer: adam

> For LSTM, each sample is reshaped from `(num_features,)` to `(num_features, 1)`.

---

## Metrics Reported

For each fold, the following metrics are computed:

### Confusion matrix-based
- TP, TN, FP, FN  
- TPR (Recall), TNR (Specificity)  
- FPR, FNR  
- Precision  
- F1 Measure  
- Accuracy, Error Rate  
- Balanced Accuracy (BACC)  
- TSS (True Skill Statistic)  
- HSS (Heidke Skill Score)

### Probability-based
- **Brier Score** (calibration error)
- **ROC AUC**

At the end, average metrics across folds are printed for each model.

---

## How to Run

### Option A: Run the notebook
Open and run:
- `Student College Admission Prediction.ipynb`

### Option B: Run as a Python script
If you converted the notebook to a script:

```bash
python main.py
