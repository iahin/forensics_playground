# Steps

**Pre-req**

1. To have at least 3 sample cases with 3 different classes[UA, DT, Unknown] labeled ==> In  order to validate case classification at the beginning
2. The 3 case records are available as graph data
3. the 3 case records are trained into k-means model and saved

**Process**

1. Create Case and then generate graph data with various information
2. Generate graph embedding from graph data
3. Feed the graph embedding into model to get a predicted value based on cluster in vector space
4. display a crime type and confidence percentage(distance to cluster center of a class)
5. Prompts user if it is correct. If correct, added to intell database for deep learning training. If wrong, retrain k-means and save.
6. Once deep learning model hits 100 cases(or specified threshold), takes over from k-means model(transfer learning)

# FAQ

#### What if user labels wrongly and train the model with wrong label?

- User will be given various inferences and prediction to assist with the labelling
- In an event the data were labelled wrongly, can use novelty detection to cross check the data distribution with existing corrected labelled data vs new labelled data
- However, there is not definite way to tell if the data was labelled wrongly