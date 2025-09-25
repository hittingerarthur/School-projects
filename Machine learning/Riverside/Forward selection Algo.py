import random

# stub evaluation function
def evaluation_function(features):
    """
    Return a random accuracy score between 25 and 100 percent.
    """
    return random.uniform(25, 100)

# forward Selection Algorithm
def forward_selection(num_features):
    print("Welcome to hples001 and ahitt003 Feature Selection Algorithm.")
    print(f"Enter the total number of features: {num_features}")
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
                accuracy = evaluation_function(temp_features)  # using the stub evaluation function
                print(f"Using the feature(s) {temp_features} the accuracy is {accuracy:.1f}%")
                
                if accuracy > best_accuracy_this_level:
                    best_accuracy_this_level = accuracy
                    feature_to_add_at_this_level = feature
        
        if feature_to_add_at_this_level is not None:
            current_set_of_features.append(feature_to_add_at_this_level)
            print(f"The feature set {current_set_of_features} was the best, accuracy is {best_accuracy_this_level:.1f}%")
        
        # track the best overall feature set
        if best_accuracy_this_level > best_overall_accuracy:
            best_overall_accuracy = best_accuracy_this_level
            best_overall_features = current_set_of_features[:]
        else:
            print("(Warning, the accuracy has decreased!)")
    
    print("Finished the search!!")
    print(f"The best feature subset is {best_overall_features}, which has an accuracy of {best_overall_accuracy:.1f}%")

forward_selection(4)