'''
 train.py
 Exercise 6: Naive Bayes text classifier
'''

import func
import time
import numpy as np

def train(dataBase):

    startTime = time.clock()
    func.sys.stdout = func.Logger("Log/Record_train.log")
    print("----------------------------------> Train part <----------------------------------")
    print("Train record time:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "\n")
    print("This train-process is using database: ", dataBase)

    # store the number of training examples
    # store the dictionary size
    numTrainDocs = 700
    numTokens = 2500

    print("Data record:")
    # read the features matrix
    M = np.mat(func.importData(dataBase[0]))
    Matrix = M.tolist()
    # test
    print("Train 'Matrix' is :\n", Matrix)
    spmatrix = func.buildSparse(Matrix, numTokens, numTrainDocs)
    train_matrix = np.mat(spmatrix)
    # test
    print("train_matrix:\n", train_matrix)

    # train_matrix now contains information about the words within the emails
    # the i-th row of train_matrix represents the i-th training email
    # for a particular email, the entry in the j-th column tells
    # you how many times the j-th dictionary word appears in that email

    # read the training labels
    train_labels = func.importData(dataBase[1])
    # the i-th entry of train_labels now indicates whether document i is spam

    # Find the indices for the spam and nonspam labels
    spam_indices = func.find(train_labels, "true")
    nonspam_indices = func.find(train_labels, "false")
    # test
    print("spam_indices:\n", spam_indices, "\nnonspam_indices:\n", nonspam_indices)

    # Calculate probability of spam
    prob_spam = len(spam_indices) / numTrainDocs
    # test
    print("prob_spam:", prob_spam)

    # Sum the number of words in each email by summing along each row of
    # train_matrix
    _email_lengths = np.sum(train_matrix, axis=1)
    email_lengths = []
    for  i in range(len(_email_lengths)):
        email_lengths.append((int)(_email_lengths[i][0]))
    # test
    print("email_lengths:\n", email_lengths)

    # Now find the total word counts of all the spam emails and nonspam emails
    spam_wc = func.getSumOfElements(email_lengths, spam_indices)
    nonspam_wc = func.getSumOfElements(email_lengths, nonspam_indices)
    # test
    print("spam_wc: \n", spam_wc, "\nnonspam_wc: \n", nonspam_wc)

    # Calculate the probability of the tokens in spam emails
    prob_tokens_spam = ((((np.mat(func.getSumOfRow(spmatrix, spam_indices))) + 1) / (spam_wc + numTokens)).tolist())[0]
    # Now the k-th entry of prob_tokens_spam represents phi_(k|y=1)

    # Calculate the probability of the tokens in non-spam emails
    prob_tokens_nonspam = ((((np.mat(func.getSumOfRow(spmatrix, nonspam_indices))) + 1) / (nonspam_wc + numTokens)).tolist())[0]
    # Now the k-th entry of prob_tokens_nonspam represents phi_(k|y=0)
    # test
    print("prob_tokens_spam:\n", prob_tokens_spam, "\nprob_tokens_nonspam:\n", prob_tokens_nonspam)

    print("----------------------------------> Train over <----------------------------------")

    endTime = time.clock()
    return [[prob_tokens_spam, prob_tokens_nonspam], prob_spam, str(endTime - startTime)]

