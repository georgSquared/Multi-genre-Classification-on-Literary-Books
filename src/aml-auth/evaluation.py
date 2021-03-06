import numpy as np
from sklearn import metrics


def get_hamming_score(y_true, y_pred, normalize=True, sample_weight=None):
    """
    Compute the Hamming score (a.k.a. label-based accuracy) for the multi-label case
    https://stackoverflow.com/q/32239577/395857
    :param y_true:
    :param y_pred:
    :param normalize:
    :param sample_weight:
    :return:
    """
    acc_list = []
    for i in range(y_true.shape[0]):
        set_true = set(np.where(y_true[i])[0])
        set_pred = set(np.where(y_pred[i])[0])

        if len(set_true) == 0 and len(set_pred) == 0:
            tmp_a = 1
        else:
            tmp_a = len(set_true.intersection(set_pred)) / \
                    float(len(set_true.union(set_pred)))
        acc_list.append(tmp_a)
    return np.mean(acc_list)


def evaluate_model(actual, predicted, average="micro", print_results=False):
    recall_score = metrics.recall_score(actual, predicted, average=average)
    precision_score = metrics.precision_score(actual, predicted, average=average)
    f1_score = metrics.f1_score(actual, predicted, average=average)
    accuracy_score = metrics.accuracy_score(actual, predicted)
    hamming_loss = metrics.hamming_loss(actual, predicted)
    classfication_report = metrics.classification_report(actual, predicted)

    if print_results:
        print(f"Accuracy score: {accuracy_score:.4f}")
        print(f"Precision score: {precision_score:.4f} with average parameter: {average}")
        print(f"Recall score: {recall_score:.4f} with average parameter: {average}")
        print(f"F1 score: {f1_score:.4f} with average parameter: {average}")
        print(f"Hamming loss: {hamming_loss:.4f}")
        print(f"Classification report:\n{classfication_report}")

    return accuracy_score, precision_score, recall_score, f1_score, hamming_loss, classfication_report


def imbalanced_evaluate(actual, predicted, proba, average="micro", print_results=False):
    f1_score = metrics.f1_score(actual, predicted, average=average)
    auc = metrics.roc_auc_score(actual, proba, multi_class='ovr', average="weighted")
    # brier_score_loss = metrics.brier_score_loss(actual, predicted)

    if print_results:
        print(f"F1 score: {f1_score:.2f} with average parameter: {average}")
        # print(f"Brier score loss: {brier_score_loss:.2f} with average parameter: {brier_score_loss}")

    return f1_score, auc


def evaluate_per_label(actual, predicted, print_results=False):
    accuracy_per_label = []
    precision_per_label = []
    recall_per_label = []
    f1_per_label = []

    for label in range(actual.shape[1]):
        actual_label = actual.values[:, label]
        predicted_label = predicted[:, label]

        recall_score = metrics.recall_score(actual_label, predicted_label)
        precision_score = metrics.precision_score(actual_label, predicted_label)
        f1_score = metrics.f1_score(actual_label, predicted_label)
        accuracy_score = metrics.accuracy_score(actual_label, predicted_label)

        accuracy_per_label.append(accuracy_score)
        precision_per_label.append(precision_score)
        recall_per_label.append(recall_score)
        f1_per_label.append(f1_score)


        if print_results:
            print(f"Accuracy score: {accuracy_score:.4f}")
            print(f"Precision score: {precision_score:.4f}")
            print(f"Recall score: {recall_score:.4f}")
            print(f"F1 score: {f1_score:.4f}")

    return accuracy_per_label, precision_per_label, recall_per_label, f1_per_label


def run():
    pass


if __name__ == "__main__":
    run()
