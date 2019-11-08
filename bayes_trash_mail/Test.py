'''
 test.py
 Exercise 6: Naive Bayes text classifier
'''

import numpy as np
import time
import func

np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)


def test(prob_tokens_list, prob_spam):
    startTime = time.clock()
    func.sys.stdout = func.Logger("Log/Record_test.log")
    print("----------------------------------> Test part <----------------------------------")
    print("Train record time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "\n")
    print("Data record:")

    # read the test matrix in the same way we read the training matrix
    N = np.mat(func.importData("Data/test/test-features.txt"))
    Matrix = N.tolist()
    print("Train 'Matrix' is:\n", Matrix)

    spmatrix = func.buildSparse(Matrix, 2500, (int)(Matrix[len(Matrix) - 1][0]))
    test_matrix = np.mat(spmatrix)
    print("test_matrix :\n", test_matrix, "\n", len(test_matrix))

    # Store the number of test documents and the size of the dictionary
    numTestDocs = (int)(test_matrix.shape[0])
    numTokens = (int)(test_matrix.shape[1])
    print("numTestDocs: ", numTestDocs)
    print("numTokens: ", numTokens)

    # The output vector is a vector that will store the spam/nonspam prediction
    # for the documents in our test set.
    output = func.zeros(numTestDocs)
    print("output(init): \n", output)

    # Calculate log p(x|y=1) + log p(y=1)
    # and log p(x|y=0) + log p(y=0)
    # for every document
    # make your prediction based on what value is higher
    # (note that this is a vectorized implementation and there are other
    #  ways to calculate the prediction)
    log_a = test_matrix * (np.mat(func.logList(prob_tokens_list[0]))).T + np.log(prob_spam)
    log_b = test_matrix * (np.mat(func.logList(prob_tokens_list[1]))).T + np.log(1 - prob_spam)
    print("log_a: \n", log_a)
    print("log_b: \n", log_b)

    func.bigger(log_a, log_b, output)
    print("output:\n", output)

    # Read the correct labels of the test set
    L = func.importData("Data/test/test-labels.txt")
    test_labels = L.tolist()
    print("test_labels: ", test_labels)

    # Compute the error on the test set
    # A document is misclassified if it's predicted label is different from
    # the actual label, so count the number of 1's from an exclusive "or"
    numdocs_worng = func.sumList(func.xorList(output, test_labels))
    print("numdocs_worng: ", numdocs_worng)

    # Print out error statistics on the test set
    fractions_worng = numdocs_worng / numTestDocs
    print("fractions_worng: ", fractions_worng)

    endTime = time.clock()
    print("----------------------------------> Test over <----------------------------------")

    return ["numdocs_worng: " + str(numdocs_worng), "fractions_worng: " + str(fractions_worng), str(endTime - startTime)]
