#Use BDgrapg
library(BDgraph)

#Read the b that is parsed as an argument from Python
parser = commandArgs(trailingOnly=TRUE)

#Read the if debugging lines should be printed
debugOn = parser[5]

b = as.integer(parser[1])  # Degrees of freedom

#Read the n (number of samples in the original data) that is parsed from Python
n = as.integer(parser[2])

if (debugOn){
    sprintf("[R] rgwish will now be sampling %d samples. The b (degrees of freedom) is set to %d", n, b)
}

G = read.table(text=parser[3])  # Input is already in the right format thanks to python
G = as.matrix(G)
if (debugOn){
    print("[R] Matrix G:")
    print(G)
}

K = read.table(text=parser[4])  # Input is already in the right format thanks to python
K = as.matrix(K)
if (debugOn){
    print("[R] Matrix K:")
    print(K)
}

shape_matrix = diag(dim(K)[1])  # Identity matrix of size k
if (debugOn){
    print("[R] Shape Matrix:")
    print(shape_matrix)
}

# Actual algorithm
#...
#

# Finally
if (debugOn){
    print("[R] Sampled Matrix G:")
    print(G)
    print("[R] Sampled Matrix K:")
    print(K)
    print("[R] returning results:")
}
# Printing results (to be deserialized by python) 
# (cat does not print newline)
G_vectorized = as.vector(t(G))
for (entry in G_vectorized) {
    cat(entry)
    cat(' ')
}
cat('\n')  # Newline

K_vectorized = as.vector(t(K))
for (entry in K_vectorized) {
    cat(entry)
    cat(' ')
}