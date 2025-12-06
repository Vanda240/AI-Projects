Car Evaluation — Multi-Model Classification + Deep Learning (Keras)

This project trains and compares multiple machine learning models (and a Keras deep learning model) on the Car Evaluation dataset. It includes:

Data loading + preprocessing (label encoding + scaling)

Handling class imbalance using SMOTE

Model training + hyperparameter tuning with GridSearchCV

Evaluation: Accuracy, Weighted F1, Confusion Matrix

ROC curve plotting (multi-class one-vs-rest style)

Optional ensemble with a soft VotingClassifier

Learning curves for the deep learning model

Dataset

File: Car_Evaluation.csv
The script expects the dataset in the same folder as the Python file.

Columns used:

buying, maint, doors, persons, lug_boot, safety, class

The script reads the dataset using these column names and assumes no header in the CSV.

Requirements
Python Packages

Install dependencies (recommended in a virtual environment):

pip install pandas numpy matplotlib seaborn scikit-learn imbalanced-learn xgboost lightgbm catboost tensorflow


The script will:

Visualize feature distributions

Preprocess + split dataset

Apply SMOTE on training set

Train a deep learning model with early stopping

Train and tune ML models via GridSearchCV

Plot confusion matrices, learning curves, and model comparisons

Train a Voting Classifier ensemble and evaluate it

Perform cross-validation for the ensemble

Plot ROC curves for selected models

Models Included
Machine Learning Models

Logistic Regression (One-vs-Rest)

Decision Tree

Random Forest

KNN

SVM (probability=True)

Gradient Boosting

XGBoost

LightGBM

CatBoost

Deep Learning Model (TensorFlow/Keras)

Dense(64) + Dropout

Dense(32) + Dropout

Dense(4, softmax)

EarlyStopping on validation loss

Outputs / Visualizations

The code produces plots for:

Feature value distributions

Confusion matrix (for each model)

Learning curves (deep learning accuracy & loss)

Model accuracy comparison bar chart

Model F1 comparison bar chart

Random Forest feature importance

ROC curve comparison (only for models with probability scores)

Notes / Known Issues (Important)







