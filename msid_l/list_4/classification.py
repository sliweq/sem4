from typing import List, Tuple

# https://en.wikipedia.org/wiki/Confusion_matrix
# https://towardsai.net/p/l/multi-class-model-evaluation-with-confusion-matrix-and-classification-report

def get_confusion_matrix(
    y_true: List[int], y_pred: List[int], num_classes: int,
) -> List[List[int]]:
    """
    Generate a confusion matrix in a form of a list of lists. 

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values
    :param num_classes: number of supported classes

    :return: confusion matrix
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Invalid input shapes!")
    for i in range(len(y_true)):
        if y_true[i] >= num_classes or y_true[i] < 0: 
            raise ValueError("Invalid prediction classes!")
        if y_pred[i] >= num_classes or y_pred[i] < 0:
            raise ValueError("Invalid prediction classes!")
    
    result = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
    for i in range(len(y_true)):
        result[y_true[i]][y_pred[i]] += 1
    return result    


def get_quality_factors(
    y_true: List[int],
    y_pred: List[int],
) -> Tuple[int, int, int, int]:
    """
    Calculate True Negative, False Positive, False Negative and True Positive 
    metrics basing on the ground truth and predicted lists.

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: a tuple of TN, FP, FN, TP
    """
    
    result = [0, 0, 0, 0]
    for i in range(len(y_true)):
        if y_true[i]:
            if y_pred[i]:
                result[3] += 1
            else:
                result[2] += 1 
        else:
            if y_pred[i]:
                result[1] += 1 
            else:
                result[0] += 1 
    return tuple(result)
    

def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the accuracy for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: accuracy score
    """
    # accuracy = (TP + TN) / (TP + TN + FP + FN)
    result = get_quality_factors(y_true, y_pred)
    return (result[0] + result[3]) / sum(result)


def precision_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the precision for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: precision score
    """
    return get_quality_factors(y_true, y_pred)[3]/y_pred.count(1)


def recall_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the recall for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: recall score
    """
    return get_quality_factors(y_true, y_pred)[3]/y_true.count(1)


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the F1-score for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: F1-score
    """
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    return 2 * (precision * recall) / (precision + recall)


if __name__ == "__main__":
    print("get_quality_factors:")
    print(get_quality_factors([1, 1, 0, 1, 1, 0, 1, 0, 0, 1,], [1, 1, 0, 1, 1, 0, 0, 1, 0, 1,]))
    print(get_quality_factors([1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,]))
    print(get_quality_factors([0, 1, 0, 0, 1, 1, 0, 1, 0, 0,],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1,]))
    print("accuracy_score:")
    print(accuracy_score([1, 1, 0, 1, 1, 0, 1, 0, 0, 1,],
            [1, 1, 0, 1, 1, 0, 0, 1, 0, 1,]))
    print(accuracy_score([1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,]))
    print(accuracy_score( [0, 1, 0, 0, 1, 1, 0, 1, 0, 0,],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1,]))
    print("precision_score:")
    print(precision_score([1, 1, 0, 1, 1, 0, 1, 0, 0, 1,],
            [1, 1, 0, 1, 1, 0, 0, 1, 0, 1,]))
    print(precision_score([1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,]))
    print(precision_score([0, 1, 0, 0, 1, 1, 0, 1, 0, 0,],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1,]))
    print("recall_score:")
    print(recall_score([1, 1, 0, 1, 1, 0, 1, 0, 0, 1,],
            [1, 1, 0, 1, 1, 0, 0, 1, 0, 1,]))
    print(recall_score([1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,]))
    print(recall_score([0, 1, 0, 0, 1, 1, 0, 1, 0, 0,],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1,]))
    print("f1_score:")
    
    print(f1_score([1, 1, 0, 1, 1, 0, 1, 0, 0, 1,],
            [1, 1, 0, 1, 1, 0, 0, 1, 0, 1,]))
    print(f1_score([1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1,],
            [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,]))
    print(f1_score([0, 1, 0, 0, 1, 1, 0, 1, 0, 0,],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 1,]))
    
    
    
    
    
    
    
    