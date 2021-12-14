#Working directory setup
print(getwd())
setwd("/Users/caspar/Desktop/Bayesian Project/BAY-STATS-Project-ABDPPS")

#Read the adjacency from the input csv file (adj.csv)
adj <- read.csv("adj.csv", header=FALSE)
adj = data.matrix(adj)

#Calculate b=k-1
dim = dim(adj)
b = dim[1]-1

#Call rgwish
sample <- rgwish( n = 1, adj = adj, b = b, D = diag( b ) )
#Round to two decimals
output <- round( sample, 2 )

#Write the result in the output file (gwish.csv)
write.table(output, file = "gwish.csv", row.names = FALSE, col.names = FALSE)


