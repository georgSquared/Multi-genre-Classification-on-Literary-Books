import time
from functools import partial

import numpy as np
from active_learning_methods.helper_functions import create_random_pool_and_initial_sets, delete_rows_csr
from modAL import ActiveLearner
from modAL.batch import uncertainty_batch_sampling
from modAL.density import information_density
from sklearn import metrics

BATCH_SIZE = 5


def run(X, y, n_samples_for_intial, n_queries, estimator):
    start_time = time.time()

    X_train, y_train, X_pool, y_pool = create_random_pool_and_initial_sets(X, y, n_samples_for_intial)

    preset_batch = partial(uncertainty_batch_sampling, n_instances=BATCH_SIZE*3)

    learner = ActiveLearner(
        estimator=estimator,
        X_training=X_train,
        y_training=y_train,
        query_strategy=preset_batch
    )

    initial_accuracy = learner.score(X, y)
    print("Initial Accuracy: ", initial_accuracy)
    performance_history = [initial_accuracy]

    f1_score = 0
    index = 0
    while  f1_score < 0.65:
        index += 1
        query_index, _ = learner.query(X_pool)

        X_candidate, y_candidate = X_pool[query_index, :], y_pool[query_index]

        # Get the information density matrix, sort it and pick the 3 most information dense examples
        info_density_matrix = information_density(X_candidate)
        candidate_index = info_density_matrix.argsort()[-BATCH_SIZE:][::-1]

        # Teach our ActiveLearner model the record it has requested.
        X_selected, y_selected = X_candidate[candidate_index, :], y_candidate[candidate_index]
        learner.teach(X=X_selected, y=y_selected)

        # Remove the queried instance from the unlabeled pool.
        pool_idx_list = []
        for idx in candidate_index:
            row = query_index[idx]
            pool_idx_list.append(row)

        pool_idx = np.asarray(pool_idx_list)

        X_pool = delete_rows_csr(X_pool, pool_idx)
        y_pool = np.delete(y_pool, pool_idx)

        # Calculate and report our model's f1_score.
        y_pred = learner.predict(X)
        f1_score = metrics.f1_score(y, y_pred, average='micro')
        if index % 20 == 0:
            print('F1 score after {n} training samples: {f1:0.4f}'.format(n=index * batch_size, f1=f1_score))

        # Save our model's performance for plotting.
        performance_history.append(f1_score)



    num_of_annotated_samples = index * BATCH_SIZE
    print("--- %s seconds ---" % (time.time() - start_time))
    return num_of_annotated_samples


if __name__ == "__main__":
    run()
