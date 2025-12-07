# Wine Quality Classification — Logistic Regression & Deep Dynamic Ensemble (From Scratch)

This project implements **logistic regression** and a series of **dynamic ensemble logistic regression** models (tree-structured, probabilistic routing) from scratch using **NumPy**, and evaluates them on the Wine Quality dataset (`allwine.csv`).

It includes four tasks:

1. **Simple Logistic Regression (baseline)**
2. **Dynamic Ensemble Logistic Regression (2-leaf / 3-node tree)**
3. **Deep Dynamic Ensemble Model (3-layer fixed design, 7 nodes)**
4. **Bonus:** **Generalized Deep Dynamic Ensemble** supporting an **arbitrary number of layers**

---

## Dataset

**File:** `allwine.csv`

**Input features (10):**
- fixed acidity  
- volatile acidity  
- citric acid  
- residual sugar  
- chlorides  
- free sulfur dioxide  
- density  
- pH  
- sulphates  
- alcohol  

**Target:**
- `quality`

### Label Setup (Binary Classification)
If `quality` contains more than 2 classes, it is converted into binary:
- `1` if quality **>= 6**
- `0` otherwise

---

## Requirements

Install dependencies:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn
How to Run
Task 1 — Simple Logistic Regression (From Scratch)

Runs a grid search over learning rates and epochs and plots the cost curve.

python task1_logistic_regression.py


Best result (example from your run):

Best LR: 0.001

Epochs: 15000

Test Accuracy: 0.7297

Train Accuracy: 0.7357

Task 2 — Dynamic Ensemble Logistic Regression (3 nodes)

Implements a small tree-style ensemble with a routing node + two leaf logistic models.

python task2_dynamic_ensemble_lr.py


Best result (example from your run):

Best Test Accuracy: 0.7297

Best config: lr=0.003, iterations=10000

Task 3 — Deep Dynamic Ensemble (3-layer fixed / 7 nodes)

Implements a deeper ensemble with multiple gating nodes and leaf predictors.

python task3_three_layer_ensemble.py


Best result (example from your run):

Best Test Accuracy: 0.7297

Best config: lr=0.05, iterations=5000

Task 4 (Bonus) — Generalized Deep Ensemble (N layers)

Generalizes the model to support any number of layers using a complete binary tree:

total nodes = 2^n_layers - 1

Run:

python task4_generalized_deep_ensemble.py


You will be prompted for:

number of layers

learning rate

number of iterations

Example input:

n_layers = 3
lr = 0.05
num_iter = 15000


Example result (your run):

Test Accuracy: 0.7438 with n_layers=3, lr=0.05, iterations=15000

Model Overview
1) Baseline Logistic Regression

Standard sigmoid classifier trained via gradient descent on cross-entropy loss.

2) Dynamic Ensemble Logistic Regression (Small Tree)

A probabilistic routing model:

A “middle” node decides routing probability

Left/right leaf logistic regressors produce predictions

Final probability is a weighted mixture based on routing

3) Deep Dynamic Ensemble

Extends the routing idea across multiple nodes to form a deeper mixture-of-experts style tree.

4) Generalized N-Layer Tree Ensemble (Bonus)

Builds a complete binary tree of logistic units and computes:

per-node probabilities (sigmoid outputs)

path probabilities to each leaf

final prediction from weighted leaf contributions
Includes gradient-based training of all nodes.

Output / What You’ll See

Printed best hyperparameters (learning rate, iterations)

Train and test accuracy

(Task 1) Cost curve plot

(Task 4) Loss printed every 500 steps

Notes / Limitations

These implementations are educational and focus on clarity.

The deep ensemble training can be slow for large iteration counts because it computes paths and gradients over many nodes.

Further improvements could include:

vectorizing path computations

adding regularization

early stopping

mini-batch training
