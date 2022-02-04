import numpy as np


# Binder loss function (FA revised)
# Sum for i < j -> 1 error for each pair that is equal in one and different in the other

def binder_loss(Z_sample, Z_true, debug=False):
    # Input: Z_sample, Z_true matrices -> We only need the cluster indexes
    # Output: err scalar -> Sum of errors
    if Z_sample.shape != Z_true.shape:
        raise Exception('Error: Z matrices of different shape')
    # Idea: Turn matrices into single row to check all pairs more easily
    # First element checks all next elements
    # Get all possible pairs without repeating
    Z_sample_indicator = Z_sample.flatten()
    # Idea: Matrix of differences between rows
    # https://stackoverflow.com/questions/9704565/populate-numpy-matrix-from-the-difference-of-two-vectors
    Z_sample_indicator = np.equal.outer(Z_sample_indicator, Z_sample_indicator)
    # See only equals -> absolute of the difference
    # Eq + Eq -> abs(1-1) = 0 no error
    # Eq + Diff or Diff + Eq -> abs(1-0) = abs(0-1) = 1 error
    # Diff + Diff -> abs(0-0) = 0 no error
    Z_true_indicator = Z_true.flatten()
    Z_true_indicator = np.equal.outer(Z_true_indicator, Z_true_indicator)
    # Now we have the pairwise differences to compare
    error_sum = np.not_equal(Z_sample_indicator, Z_true_indicator).sum() 
    errors = int(error_sum/2)  # We take the entire matrix so the errors are duplicated
    # Max error
    max_err = Z_true_indicator.shape[0] * Z_true_indicator.shape[1]
            
    if debug:
        print('Error: '+str(errors))
        print('Max error: '+ str(max_err))
        print('Error %: '+str(100*errors/max_err))
    return errors/max_err  # Return a percentage to feel better


# An experimental binder loss
def binder_loss_fast(Z_sample, Z_true, debug=False):
    # Input: Z_sample, Z_true matrices -> We only need the cluster indexes
    # Output: err scalar -> Sum of errors
    if Z_sample.shape != Z_true.shape:
        raise Exception('Error: Z matrices of different shape')
    # Idea: Turn matrices into single row to check all pairs more easily
    # First element checks all next elements
    # Get all possible pairs without repeating
    errors = np.zeros((k, k))
    for t_sample in range(k):  # iterate over sample topics
        Z_sample_indicator = Z_sample == t_sample
        for t_true in range(k):  # iterate over true topics
            # See only equals -> absolute of the difference
            # Eq + Eq -> abs(1-1) = 0 no error
            # Eq + Diff or Diff + Eq -> abs(1-0) = abs(0-1) = 1 error
            # Dif + Diff -> abs(0-0) = 0 no error
            Z_true_indicator = Z_true == t_true
            error_sum = np.not_equal(Z_sample_indicator, Z_true_indicator).sum() 
            errors[t_sample][t_true] = error_sum
            
    if debug:
        print('Error matrix:')
        print(errors)
        print('Error sum:')
        print(errors.sum())
    # Minimization (Stable Marriage Problem)
    final_loss = 0
    matches = []
    theoretical_max = Z_sample.size  # I will use it as a dummy variable
    while not len(matches) == k:
        min_error = np.amin(errors.flatten())  # Select min
        i, j = np.where(errors == min_error)  # Find index
        # There could be multiple minima, only using the first one
        i = i[0]
        j = j[0]
        if debug:
            print(f"Sample topic {i} was matched with true topic {j} with error {min_error}")
        final_loss += min_error
        matches.append([i, j])
        # Filling corresponding row and column so that those two indexes will not be selected again
        errors[:,j] = theoretical_max
        errors[i,:] = theoretical_max
    return final_loss