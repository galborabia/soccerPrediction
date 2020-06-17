from sklearn.naive_bayes import GaussianNB, CategoricalNB, MultinomialNB
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn import svm
from sklearn.model_selection import cross_validate
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold



# Generic function for making a classification model and accessing performance:

def classification_model(model, data, predictors, outcome):
    # Fit the model:
    model.fit(data[predictors], data[outcome])

    # Make predictions on training set:
    predictions = model.predict(data[predictors])

    # Print accuracy
    accuracy = metrics.accuracy_score(predictions, data[outcome])
    print("Training accuracy : %s" % "{0:.3%}".format(accuracy))

    # Perform k-fold cross-validation with 10 folds
    kf =KFold(n_splits=10, random_state=None, shuffle=False)
    accuracy = []

    for train, test in kf.split(predictions):
        # Filter training data
        train_predictors = (data[predictors].iloc[train, :])

        # The target we're using to train the algorithm.
        train_target = data[outcome].iloc[train]

        # Training the algorithm using the predictors and target.
        model.fit(train_predictors, train_target)

        # Record accuracy from each cross-validation run
        accuracy.append(model.score(data[predictors].iloc[test, :], data[outcome].iloc[test]))

    print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(accuracy)))

    # Fit the model again so that it can be refered outside the function:



    return  model;


# Reading the dataset in a dataframe using Pandas

df = pd.read_csv("allGambling/matchTrainingGamblingSplitTeam.csv")
# var_mod = ['stage', 'home_ratio', 'draw_ratio', 'away_ratio', 'overall_rating', 'finishing','heading_accuracy',	'short_passing','volleys',	'dribbling','curve','free_kick_accuracy','long_passing','ball_control', 'acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'shot_power',	'jumping',	'stamina',	'strength',	'long_shots',	'aggression',	'interceptions',	'positioning',	'vision',	'penalties',	'marking',	'standing_tackle',	'sliding_tackle',	'gk_diving',	'gk_handling'	,'gk_kicking',	'gk_positioning',	'gk_reflexes']
var_mod = ['home_ratio', 'draw_ratio', 'away_ratio', 'overall_rating', 'stage']
# model = svm.NuSVC(gamma='auto')
# model =svm.SVC()  ##Training accuracy : 51.654%##
model = RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=7, max_features='auto')
# model = GaussianNB()
outcome_var = 'result'
model = classification_model(model, df, var_mod, outcome_var)
df_test = pd.read_csv("specialData/matchTestSplitTeam.csv")

predictions = model.predict(df_test[var_mod])

# Print accuracy
accuracy = metrics.accuracy_score(predictions, df_test[outcome_var])
print("Training accuracy : %s" % "{0:.3%}".format(accuracy))
