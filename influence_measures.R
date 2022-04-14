library(rstudioapi)
library(ggplot2)
library(reshape2)
tryCatch({
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
}, error=function(cond){message(paste("Cannot change working directory."))
})

flip <- function(x) {
  y <- as.numeric(x)
  z <- y * -1
  return(z)
}

ranking_comparisons <- function(ranks) {
  numeric_cols <- c("core_rank", "degree_rank", "eigen_rank")
  ranks[numeric_cols] <- sapply(ranks[numeric_cols], flip)
  
  blue <- rgb(0,0,1, alpha=0.5)
  green <- rgb(0,1,0, alpha=0.5)
  red  <- rgb(1,0,0, alpha=0.5)
  
  ranks$nodeID <- as.character(ranks$nodeID)
  melted_ranks <- melt(ranks, id.vars = c("nodeID"))
  
  # increment N by some % until you find the right alignment for the line
  N = 0.14
  id <- ranks$nodeID[N*nrow(ranks)]
  
  p2 <- ggplot(melted_ranks, aes(x=nodeID, y=value)) +
    geom_line(aes(colour=variable, group=variable)) +
    scale_x_discrete(limits=ranks$nodeID) +
    geom_vline(xintercept=id)

  return(p2)
}



dem_ranks <- as.data.frame(read.csv("dem_subgraph_democrat_rankings.csv"))
demplot <- ranking_comparisons(dem_ranks)
demplot



#pnodes <- cbind(c("B","D","E","F","A","C"),
#                        c(1,2,3,4,5,6),
#                        c(1,4,2,5,6,3),
#                        c(2,3,1,4,6,5))
#colnames(pnodes) <- c("nodeID", "core_rank", "degree_rank", "eigen_rank")
#write.table(pnodes, "~/Desktop/rankings.csv", row.names = FALSE)
#colnames(ranks) <- ranks[1,]
#ranks <- ranks[-1,]


#barplot(height = as.numeric(ranks$core_rank), names.arg = ranks$nodeID, col = c(blue))
#barplot(height = as.numeric(ranks$degree_rank), names.arg = ranks$nodeID, col = c(red), add=TRUE)
#barplot(height = as.numeric(ranks$eigen_rank), names.arg = ranks$nodeID, col = c(green), add=TRUE)

#p <- ggplot(ranks, aes(x=nodeID, y=seq(1,nrow(ranks)))) + 
#      scale_x_discrete(limits=ranks$nodeID) +
#      geom_point(aes(x=nodeID, y=core_rank, colour=green)) +
#      geom_point(aes(x=nodeID, y=degree_rank, color=red)) + 
#      geom_point(aes(x=nodeID, y=eigen_rank, color=blue))


