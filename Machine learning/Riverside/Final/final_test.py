import random
import numpy as np
import time
import matplotlib.pyplot as plt

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
    global best_overall_features
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
    
    print("Finished the search!!")
    print(f"The best feature subset is {best_overall_features}, which has an accuracy of {best_overall_accuracy:.1f}%")

def backward_elimination(num_features):
    global best_overall_features
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
    
    print("Finished search!!")
    print(f"The best feature subset is {best_overall_features}, which has an accuracy of {best_overall_accuracy:.1f}%")

def plot_best_features(features, labels, best_feature_subset, method_name, dataset_name):
    if len(best_feature_subset) == 1:
        feature_idx = best_feature_subset[0] - 1
        x_feature = features[:, feature_idx]
        
        plt.figure(figsize=(8, 6))
        for label in np.unique(labels):
            classification_type = 'Correct Classification' if label == 1 else 'Incorrect Classification'
            plt.scatter(x_feature[labels == label], 
                        np.zeros_like(x_feature[labels == label]) + label * 0.02, 
                        label=classification_type, alpha=0.6)
        
        plt.xlabel(f'Feature {best_feature_subset[0]}')
        plt.title(f'{method_name} Selection on {dataset_name}: Feature {best_feature_subset[0]}')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
    
    elif len(best_feature_subset) >= 2:
        feature_1_idx = best_feature_subset[0] - 1
        feature_2_idx = best_feature_subset[1] - 1
        
        x_feature = features[:, feature_1_idx]
        y_feature = features[:, feature_2_idx]
        
        plt.figure(figsize=(8, 6))
        for label in np.unique(labels):
            classification_type = 'Correct Classification' if label == 1 else 'Incorrect Classification'
            plt.scatter(x_feature[labels == label], 
                        y_feature[labels == label], 
                        label=classification_type, alpha=0.6)
        
        plt.xlabel(f'Feature {best_feature_subset[0]}')
        plt.ylabel(f'Feature {best_feature_subset[1]}')
        plt.title(f'{method_name} Selection on {dataset_name}: Features {best_feature_subset[0]} and {best_feature_subset[1]}')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()

def generate_best_feature_plot(best_feature_subset, method_name, file_path):
    dataset_name = file_path.split("/")[-1]
    if len(best_feature_subset) >= 1:
        plot_best_features(scaled_features, labels, best_feature_subset, method_name, dataset_name)

print("Welcome to hples001 and ahitt003 Feature Selection Algorithm.")
num_features = int(input("Enter the total number of features: "))

file_path = input("Enter the path to your dataset: ")
features, labels = load_data(file_path)
mean = features.mean(axis=0)
std = features.std(axis=0)
scaled_features = (features - mean) / std

classifier = NearestNeighborClassifier()
validator = LeaveOneOutValidator(classifier)

print("Type the number for the algorithm you want to run.")
print("1. Forward Selection")
print("2. Backward Elimination")

choice = int(input("Enter your choice (1 or 2): "))

best_overall_features = []

if choice == 1:
    forward_selection(num_features)
    generate_best_feature_plot(best_overall_features, 'Forward Selection', file_path)
elif choice == 2:
    backward_elimination(num_features)
    generate_best_feature_plot(best_overall_features, 'Backward Elimination', file_path)
else:
    print("Please select 1 or 2")
