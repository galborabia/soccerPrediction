
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn import metrics
from sklearn.model_selection import KFold, cross_val_score



# Generic function for making a classification model and accessing performance:
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier


def classification_model(models, data, predictors, outcome, df_test):
    results = []
    names = []
    for name, model in models:
        model.fit(data[predictors],data[outcome])
        result = cross_val_score(model, data[predictors], data[outcome], cv=3)
        names.append(name)
        results.append(result)
    print("train accuracy")
    for i in range(len(names)):
        print(names[i], results[i].mean())

    # df_test = pd.read_csv("testNoSplit.csv")
    results = []
    names = []
    for name, model in models:
        predictions = model.predict(df_test[predictors])
        result = metrics.accuracy_score(predictions, df_test[outcome])
        names.append(name)
        results.append(result)
    print("test accuracy")
    for i in range(len(names)):
        print(names[i], results[i])



    # Fit the model:
    #     for name,model in models:
    #     model.fit(data[predictors], data[outcome])
    #
    #     # Make predictions on training set:
    #     predictions = model.predict(data[predictors])
    #
    #     # Print accuracy
    #     accuracy = metrics.accuracy_score(predictions, data[outcome])
    #     print("Training accuracy : %s" % "{0:.3%}".format(accuracy))
    #
    #     # Perform k-fold cross-validation with 10 folds
    #     kf = KFold(n_splits=10, random_state=None, shuffle=False)
    #     accuracy = []
    #
    #     for train, test in kf.split(predictions):
    #         # Filter training data
    #         train_predictors = (data[predictors].iloc[train, :])
    #
    #         # The target we're using to train the algorithm.
    #         train_target = data[outcome].iloc[train]
    #
    #         # Training the algorithm using the predictors and target.
    #         model.fit(train_predictors, train_target)
    #
    #         # Record accuracy from each cross-validation run
    #         accuracy.append(model.score(data[predictors].iloc[test, :], data[outcome].iloc[test]))
    #
    #     print("Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(accuracy)))
    #
    #     # Fit the model again so that it can be refered outside the function:
    #
    #
    #     df_test = pd.read_csv("specialData/matchTestSplitTeam.csv")
    #     predictions = model.predict(df_test[outcome])
    #
    #     # Print accuracy
    #     accuracy = metrics.accuracy_score(predictions, df_test[outcome])
    #     print("Test accuracy for model : %s" % "{0:.3%}".format(accuracy))


# Reading the dataset in a dataframe using Pandas



df_no_split = pd.read_csv("trainningNoSplit.csv")
df_split = pd.read_csv("trainningSplit.csv")
df_test_split = pd.read_csv("testNoSplit.csv")
df_test_no_split = pd.read_csv("testSplit.csv")

var_mod = ['stage', 'home_ratio', 'draw_ratio', 'away_ratio', 'overall_rating', 'finishing','heading_accuracy',	'short_passing','volleys',	'dribbling','curve','free_kick_accuracy','long_passing','ball_control', 'acceleration',	'sprint_speed',	'agility',	'reactions',	'balance',	'shot_power',	'jumping',	'stamina',	'strength',	'long_shots',	'aggression',	'interceptions',	'positioning',	'vision',	'penalties',	'marking',	'standing_tackle',	'sliding_tackle',	'gk_diving',	'gk_handling'	,'gk_kicking',	'gk_positioning',	'gk_reflexes','home_win',	'home_draw',	'home_lose'	, 'away_win','away_draw',	'away_lose']

models = []
models.append(("SVC",SVC()))
models.append(("LinearSVC",LinearSVC()))
models.append(("KNeighbors",KNeighborsClassifier()))
rf = RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=7, max_features='auto')
models.append(("RandomForest",rf))
outcome_var = 'result'
model = classification_model(models, df_no_split, var_mod, outcome_var,df_test_no_split)
print("-----------------split--------------\n")
model = classification_model(models, df_split, var_mod, outcome_var,df_test_split)
# df_test = pd.read_csv("specialData/matchTestSplitTeam.csv")
# # predictions = model.predict(df_test[var_mod])
# #
# # # Print accuracy
# # accuracy = metrics.accuracy_score(predictions, df_test[outcome_var])
# # print("Test accuracy : %s" % "{0:.3%}".format(accuracy))
