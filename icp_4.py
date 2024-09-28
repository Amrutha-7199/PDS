# -*- coding: utf-8 -*-
"""ICP_4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ERTRuqKkD3KFilK3G9wL0grv1O18hyPQ

***Over View***

i) Data Augmentation

ii) Machine Learning Modeling:

>Feature selection

>Missing values

>Filtering or normalization

>Classification Models

> Cross Validation

>Evalutaion

>Confusion Matrix

>Accuracy, precision, recall, f-measure, AUC, etc.

**1) Data Augmentation on Text Data**

Data Augmentation is the process that enables us to increase the size of the training data without actually collecting the data. But why do we need more data? The answer is simple — the more data we have, the better the performance of the model.
Image data augmentation steps such as flipping, cropping, rotation, blurring, zooming, etc. helped tremendously in computer vision. Also, it is relatively easy to create augmented images but the same is not the case with Text data due to the complexities inherent in the language. We will use two methods, TextAttack (synonym based approach) library and Googletrans (transaltion based approach).


TextAttack is a Python framework that can be used for data augmentation in Text. The textattack.Augmenter class provides six methods for data augmentation, WordNetAugmenter, EmbeddingAugmenter, CharSwapAugmenter, EasyDataAugmenter, CheckListAugmenter, and CLAREAugmenter.

 Googletrans is built on top of Google Translate API. This uses Google Translate Ajax API for language detection and translation.Usage
The key parameters to translate() method are:
>src: source language. Optional parameter as googletrans will detect it.

>dest: destination language. Mandatory parameter.

>text: the text to be translated from source language to the destination language. Mandatory parameter.

let install the libraries to start the today's ICP
"""

!pip install textattack
!pip uninstall googletrans
!pip install googletrans==3.1.0a0

from textattack.augmentation import WordNetAugmenter, EmbeddingAugmenter, EasyDataAugmenter, CharSwapAugmenter

text = "Leadership requires two things: a vision of the world that does not yet exist and the ability to communicate it."

aug = WordNetAugmenter()
aug.augment(text)

aug = EmbeddingAugmenter()
aug.augment(text)

aug = EasyDataAugmenter()
aug.augment(text)

aug = CharSwapAugmenter()
aug.augment(text)

import googletrans
from googletrans import Translator
translator = Translator()

print(googletrans.LANGUAGES)

origin_text = "The role of a leader is not to come up with all the great ideas. The role of a leader is to create an environment in which great ideas can happen"
print(origin_text)

# translate from English to Italian
text_trans = translator.translate(text=origin_text, dest='it').text
print(text_trans)

# translate back to English from Italian
translator.translate(text=text_trans, dest='en').text

# translate from English to Urdu
text_trans = translator.translate(text=origin_text, dest='ur').text
print(text_trans)

# translate back to English from Urdu
translator.translate(text=text_trans, dest='en').text

"""**Lets Start the Machine Learning Part Now**"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

"""**Data Set**

The Pima Indians Diabetes Dataset involves predicting the onset of diabetes within 5 years in Pima Indians given medical details. It is a binary (2-class) classification problem. The Pima Indian Diabetes Dataset, originally from the National Institute of Diabetes and Digestive and Kidney Diseases, contains information of 768 women from a population near Phoenix, Arizona, USA. The outcome tested was Diabetes, 258 tested positive and 500 tested negative. Therefore, there is one target (dependent) variable and the 8 attributes.

"""

df_pima=pd.read_csv('https://raw.githubusercontent.com/npradaschnor/Pima-Indians-Diabetes-Dataset/master/diabetes.csv')
df_pima.head(8)

"""So you can see 8 different features labeled into the outcomes of 1 and 0 where 1 stands for the observation has diabetes, and 0 denotes the observation does not have diabetes

lets explore the data more
"""

df_pima.describe()

"""Check Missing Values"""

df_pima.isnull().sum()

"""No missing values? Oh wait, but I just saw somebody's Blood Pressure as 0! LOL.

The dataset is known to have missing values. Specifically, there are missing observations for some columns that are marked as a zero value. You can deduce this by the definition of those columns, and it is impractical to have a zero value is invalid for those measures, e.g., zero for body mass index or blood pressure is invalid.

so lets fix this issue. Have to fill these 0's with NaN. Not changing Pregnancies and Outcome variable because 0 is a valid answer for both of them

**Replacing 0's with 'NaN'**
"""

df_pima['Glucose'] = df_pima['Glucose'].replace(0, np.nan)
df_pima['BloodPressure'] = df_pima['BloodPressure'].replace(0, np.nan)
df_pima['SkinThickness'] = df_pima['SkinThickness'].replace(0, np.nan)
df_pima['Insulin'] = df_pima['Insulin'].replace(0, np.nan)
df_pima['BMI'] = df_pima['BMI'].replace(0, np.nan)
df_pima['DiabetesPedigreeFunction'] = df_pima['DiabetesPedigreeFunction'].replace(0, np.nan)
df_pima['Age'] = df_pima['Age'].replace(0, np.nan)

df_pima.head(8)

df_pima.isnull().sum()

"""There you go. We have to now deal with these missing values in order to proceed.

**Filling Missing Values**
"""

df_pima['BMI'].fillna(df_pima['BMI'].median(), inplace=True)
df_pima['Glucose'].fillna(df_pima['Glucose'].median(), inplace=True)
df_pima['BloodPressure'].fillna(df_pima['BloodPressure'].median(), inplace=True)
df_pima['SkinThickness'].fillna(df_pima['SkinThickness'].median(), inplace=True)
df_pima['Insulin'].fillna(df_pima['Insulin'].median(), inplace=True)

df_pima.describe()

"""Missing values are replaced by medians as seen above

**Next lets make a corelation plot for feature selection**

The importance of feature selection can best be recognized when you are dealing with a dataset that contains a vast number of features. This type of dataset is often referred to as a high dimensional dataset. Now, with this high dimensionality, comes a lot of problems such as - this high dimensionality will significantly increase the training time of your machine learning model, it can make your model very complicated which in turn may lead to Overfitting.
Often in a high dimensional feature set, there remain several features which are redundant meaning these features are nothing but extensions of the other essential features. These redundant features do not effectively contribute to the model training as well. So, clearly, there is a need to extract the most important and the most relevant features for a dataset in order to get the most effective predictive modeling performance.
"""

corr = df_pima[df_pima.columns].corr()
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap, annot = True)

"""**Feature selcetion with SelectKBest**

Let's convert the DataFrame object to a NumPy array to achieve faster computation. Also, let's segregate the data into separate variables so that the features and the labels are separated, this will help in feature selection.The scikit-learn library provides the SelectKBest class that can be used with a suite of different statistical tests to select a specific number of features, in this case, it is Chi-Squared. First,we will implement a Chi-Squared statistical test for non-negative features to select 4 of the best features from the dataset.
"""

array = df_pima.values
X = array[:,0:8]
Y = array[:,8]

Y

# Import the necessary libraries first
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

# Feature extraction
test = SelectKBest(score_func=chi2, k=5)
fit = test.fit(X, Y)

# Summarize scores
np.set_printoptions(precision=3)
print(fit.scores_)


features = fit.transform(X)
# Summarize selected features
print(features[0:5,:])

"""Interpretation:
You can see the scores for each attribute and the 4 attributes chosen (those with the highest scores): Pregnancies, Glucose, Insulin, and age. This scores will help you further in determining the best features for training your model. This scores will help you further in determining the best features for training your model.
"""

df_pima

"""Based on this analysis lets reduce our features"""

X_features = pd.DataFrame(data = df_pima, columns = ["Pregnancies","Glucose","Insulin","BMI","Age"])
X_graph=X_features.copy()
X_features.head()

Y = df_pima.iloc[:,8]
Y.head(3)

"""**Data Normalization/Scaling**

What is Feature Scaling?

It refers to putting the values in the same range or same scale so that no variable is dominated by the other.

Why Scaling?

Most of the times, your dataset will contain features highly varying in magnitudes, units and range. But since, most of the machine learning algorithms use Euclidean distance between two data points in their computations, this is a problem.If left alone, these algorithms only take in the magnitude of features neglecting the units. The results would vary greatly between different units, 5kg and 5000gms. The features with high magnitudes will weigh in a lot more in the distance calculations than features with low magnitudes. To suppress this effect, we need to bring all features to the same level of magnitudes. This can be achieved by scaling
"""

#Standard Scaling
scaler = StandardScaler()
X_features = scaler.fit_transform(X_features)
X_features

"""Split Data: Training & Testing"""

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X_features, Y, test_size=0.20, random_state=10)

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
models = []

models.append(("Logistic Regression:",LogisticRegression()))
models.append(("Support Vector Machine-linear:",SVC(kernel="linear",C=0.2)))
models.append(("Support Vector Machine-rbf:",SVC(kernel="rbf")))
models.append(("Random Forest:",RandomForestClassifier(n_estimators=5)))
models.append(("eXtreme Gradient Boost:",XGBClassifier()))

print('Models appended...')

results = []
names = []
for name,model in models:
    kfold = KFold(n_splits=5, random_state=3, shuffle = True)
    cv_result = cross_val_score(model,X_train,Y_train, cv = kfold,scoring = "accuracy")
    names.append(name)
    results.append(cv_result)
for i in range(len(names)):
    print(names[i],results[i].mean()*100)

from sklearn import metrics
from IPython.display import Image
from sklearn import tree
from pydotplus import graph_from_dot_data

# Instantiate Decision Tree with a max depth of 3
tree_model = DecisionTreeClassifier(max_depth=3)
# Fit a decision tree
tree_model = tree_model.fit(X_train, Y_train)
# Training accuracy
tree_model.score(X_train, Y_train)

# Predictions/probs on the test dataset
predicted = pd.DataFrame(tree_model.predict(X_test))
probs = pd.DataFrame(tree_model.predict_proba(X_test))

probs

# Score metrics
tree_accuracy = metrics.accuracy_score(Y_test, predicted)
tree_roc_auc = metrics.roc_auc_score(Y_test, probs[1])
tree_confus_matrix = metrics.confusion_matrix(Y_test, predicted)
tree_classification_report = metrics.classification_report(Y_test, predicted)
tree_precision = metrics.precision_score(Y_test, predicted, pos_label=1)
tree_recall = metrics.recall_score(Y_test, predicted, pos_label=1)
tree_f1 = metrics.f1_score(Y_test, predicted, pos_label=1)

print("accuracy: ", tree_accuracy)
print("AUC: ", tree_roc_auc)
print("Precision: ",tree_precision)
print("Recall: ", tree_recall)
print("F1 Score: ", tree_f1)

print(tree_classification_report)

print(tree_confus_matrix)

# Creating the confusion matrix graphs
plt.figure(figsize=(10,8))
ax=sns.heatmap(tree_confus_matrix,cmap="YlGnBu", annot=True, fmt='d')
ax.set(ylabel="True Label", xlabel="Predicted Label")
plt.show()

# output decision plot
dot_data = tree.export_graphviz(tree_model, out_file=None,
                     feature_names=X_graph.columns.tolist(),
                     class_names=['Dibetic', 'NonDibetic'],
                     filled=True, rounded=True,
                     special_characters=True)
graph = graph_from_dot_data(dot_data)
graph.write_png("decision_tree.png")

"""#Fine tuning two hyper parameters of two models"""

# Fine-tuned SVC model
svc_model = SVC(C=10, kernel='linear')

# Train the fine-tuned SVC model
svc_model.fit(X_train, Y_train)

# Evaluate the SVC model
svc_accuracy = svc_model.score(X_test, Y_test)
print(f"SVC Accuracy: {svc_accuracy * 100:.2f}%")

# Fine-tuned Random Forest model
rf_model = RandomForestClassifier(n_estimators=50, max_depth=5)

# Train the fine-tuned Random Forest model
rf_model.fit(X_train, Y_train)

# Evaluate the Random Forest model
rf_accuracy = rf_model.score(X_test, Y_test)
print(f"Random Forest Accuracy: {rf_accuracy * 100:.2f}%")

# Define and append models
models = []
models.append(("Logistic Regression:", LogisticRegression()))
models.append(("Support Vector Machine-linear:", SVC(kernel="linear", C=10)))  # Fine-tuned values
models.append(("Support Vector Machine-rbf:", SVC(kernel="rbf")))
models.append(("Random Forest:", RandomForestClassifier(n_estimators=50, max_depth=5)))  # Fine-tuned values
models.append(("eXtreme Gradient Boost:", XGBClassifier()))

# Cross-validation and results
results = []
names = []
for name, model in models:
    kfold = KFold(n_splits=5, random_state=3, shuffle=True)
    cv_result = cross_val_score(model, X_train, Y_train, cv=kfold, scoring="accuracy")
    names.append(name)
    results.append(cv_result)

# Display cross-validation results
for i in range(len(names)):
    print(f"{names[i]}: {results[i].mean() * 100:.2f}% accuracy")

# Train and evaluate the Decision Tree with the fine-tuned parameters (optional)
tree_model = DecisionTreeClassifier(max_depth=3)
tree_model = tree_model.fit(X_train, Y_train)
predicted = pd.DataFrame(tree_model.predict(X_test))
probs = pd.DataFrame(tree_model.predict_proba(X_test))

# Score metrics for Decision Tree
from sklearn import metrics
tree_accuracy = metrics.accuracy_score(Y_test, predicted)
tree_roc_auc = metrics.roc_auc_score(Y_test, probs[1])
tree_confus_matrix = metrics.confusion_matrix(Y_test, predicted)
tree_classification_report = metrics.classification_report(Y_test, predicted)

print("Decision Tree Accuracy: ", tree_accuracy)
print("AUC: ", tree_roc_auc)
print("Confusion Matrix:\n", tree_confus_matrix)