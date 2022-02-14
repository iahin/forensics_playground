To predict unknown crimetype, find ways to detect "out-of-distribution"/outlier detection method

- information on outliers: https://scikit-learn.org/stable/modules/outlier_detection.html

#### What if unknown class that is not trained is predicted?

- New data point will undergo novelty detection to find if it is outlier. if it is, it will be labeled as "others" or numerical class of 2. After which can be trained in model to predict outliers after several samples.