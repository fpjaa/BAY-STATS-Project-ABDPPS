#Read the b that is parsed as an argument from Python
parser = commandArgs(trailingOnly=TRUE)

# Reading test matrix
test_matrix = read.table(text=parser[1])  # Input is already in the right format thanks to python
test_matrix = as.matrix(test_matrix)

test_matrix_vectorized = as.vector(t(test_matrix))
for (entry in test_matrix_vectorized) {
    cat(formatC(entry, digits = 32, format = "f"))
    cat(' ')
}