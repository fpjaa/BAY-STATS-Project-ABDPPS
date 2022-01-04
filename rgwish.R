#Use BDgrapg
library(BDgraph)

#Read the b that is parsed as an argument from Python
parser = commandArgs(trailingOnly=TRUE)
b = as.integer(parser[1])
#Read the n (number of samples required) that is parsed from Python
n = as.integer(parser[2])
#Read the if debugging lines should be printed
debugOn = parser[3]


#Read the adjacency matrix from the input csv file (adj.csv)
adj <- read.csv("adj.csv", header=FALSE)
adj = data.matrix(adj)

#Read the shape_matrix from the input csv file (shape.csv)
shape <- read.csv("shape.csv", header=FALSE)
shape <- as.matrix(shape)
rownames(shape) <- colnames(shape)<-NULL

#Call rgwish
if (debugOn){
    sprintf("[R] rgwish will now be sampling %d samples. The b (degrees of freedom) is set to %d", n, b)
}
sample <- rgwish( n = n, adj = adj, b = b, D = shape )
#Round to two decimals
output <- round( sample, 2 )

#Write the result in the output file (gwish.csv)
write.table(output, file = "gwish.csv", sep = ",", row.names = FALSE, col.names = FALSE)
if (debugOn){
    print("[R] rgwish succesfully executed!")
}
