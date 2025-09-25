'''
Group: Holland Pleskac – hples001 – Session 21, Arthur Hittinger – ahitt003 – Session 22
- Small Dataset Results:
- Forward: Feature Subset: {5, 3}, Acc: 0.92
- Backward: Feature Subset: {2, 4, 5, 7, 10} Acc: 0.82
- Large Dataset Results:
- Forward: Feature Subset: {27, 1}, Acc: 0.955
- Backward: Feature Subset: {27}, Acc: 0.847
'''

import random
import numpy as np
import time

class NearestNeighborClassifier:
    def __init__(self):
        self.train_data = None
        self.train_labels = None

    def train(self, features, labels):
        self.train_data = np.array(features)
        self.train_labels = np.array(labels)

    def test(self, test_instance):
        dists = np.linalg.norm(self.train_data - test_instance, axis=1)
        idx = np.argmin(dists)
        return self.train_labels[idx]

class LeaveOneOutValidator:
    def __init__(self, classifier):
        self.classifier = classifier

    def validate(self, dataset, labels, feature_subset):
        instances = len(dataset)
        correct = 0
        print("starting leave one out validation")
        start = time.time()
        for i in range(instances):
            # if i % 100 == 0:
            #     print("processed", i, "of", instances)
            
            train_data = np.delete(dataset, i, axis=0)
            train_labels = np.delete(labels, i)
            test_instance = dataset[i]
            test_label = labels[i]
            
            train_data = train_data[:, feature_subset]
            test_instance = test_instance[feature_subset]
            
            self.classifier.train(train_data, train_labels)
            pred_label = self.classifier.test(test_instance)
            if pred_label == test_label:
                correct += 1

        time_taken = time.time() - start
        accuracy = correct / instances
        print("leave one out validation finished")
        
        return accuracy, time_taken

def load_data(file_path):
    data = np.loadtxt(file_path)
    labels = data[:, 0].astype(int)
    features = data[:, 1:]
    return features, labels

def evaluation_function(features_subset):
    subset = [f - 1 for f in features_subset]
    accuracy, _ = validator.validate(scaled_features, labels, subset)
    return accuracy * 100

def forward_selection(num_features):
    start = time.time()
    print("Beginning the search...")

    current_set_of_features = []
    best_overall_accuracy = 0
    best_overall_features = []

    for i in range(1, num_features + 1):
        feature_to_add_at_this_level = None
        best_accuracy_this_level = 0
        
        for feature in range(1, num_features + 1):
            if feature not in current_set_of_features:
                temp_features = current_set_of_features + [feature]
                accuracy = evaluation_function(temp_features)
                print(f"Using the feature(s) {temp_features} the accuracy is {accuracy:.1f}%")
                
                if accuracy > best_accuracy_this_level:
                    best_accuracy_this_level = accuracy
                    feature_to_add_at_this_level = feature
        
        if feature_to_add_at_this_level is not None:
            current_set_of_features.append(feature_to_add_at_this_level)
            print(f"The feature set {current_set_of_features} was the best, accuracy is {best_accuracy_this_level:.1f}%")
        
        if best_accuracy_this_level > best_overall_accuracy:
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = current_set_of_features[:]
        else:
            print("(Warning, the accuracy has decreased!)")

    end = time.time()
    print("Finished the search!!")
    print(f"The best feature subset is {best_overall_features}, which has an accuracy of {best_overall_accuracy:.1f}%")
    print(f"Feature selection execution time: {end - start:.2f}")

def backward_elimination(num_features):
    start = time.time()
    print("beginning search.")

    current_set_of_features = list(range(1, num_features + 1))
    best_overall_accuracy = 0
    best_overall_features = []

    print(f"Starting with all features: {current_set_of_features}")

    while len(current_set_of_features) > 0:
        feature_to_remove_at_this_level = None
        best_accuracy_this_level = 0

        for feature in current_set_of_features:
            temp_features = [f for f in current_set_of_features if f != feature]
            accuracy = evaluation_function(temp_features) 
            print(f"Using features {temp_features} accuracy is {accuracy:.1f}%")
            
            if accuracy > best_accuracy_this_level:
                best_accuracy_this_level = accuracy
                feature_to_remove_at_this_level = feature

        if feature_to_remove_at_this_level is not None:
            current_set_of_features.remove(feature_to_remove_at_this_level)
            print(f"Feature set {current_set_of_features} was best, accuracy is {best_accuracy_this_level:.1f}%")

        if best_accuracy_this_level > best_overall_accuracy:
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = current_set_of_features[:]
        else:
            print("(warning, the accuracy has decreased!)")

    end = time.time()
    print("Finished search!!")
    print(f"The best feature subset is {best_overall_features}, which has an accuracy of {best_overall_accuracy:.1f}%")
    print(f"Feature selection execution time: {end - start:.2f}")
    
print("Welcome to hples001 and ahitt003 Feature Selection Algorithm.")
num_features = int(input("enter the total number of features: "))

file_path = input("enter the path to your dataset: ")
features, labels = load_data(file_path)
mean = features.mean(axis=0)
std = features.std(axis=0)
scaled_features = (features - mean) / std

classifier = NearestNeighborClassifier()
validator = LeaveOneOutValidator(classifier)

print("Type the number for the algorithm you want to run.")
print("1. Forward Selection")
print("2. Backward Elimination")

choice = int(input("enter your choice (1 or 2): "))

if choice == 1:
    forward_selection(num_features)
elif choice == 2:
    backward_elimination(num_features)
else:
    print("Please select 1 or 2")
