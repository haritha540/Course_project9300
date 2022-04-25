setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

abdem=read.csv('ab_metadata_democrat.csv')
abrep=read.csv('ab_metadata_republican.csv')
pairs(~dcc +reciprocity+ dyad_ratio + triad_count , data = abdem)
pairs(~dcc +reciprocity+ dyad_ratio + triad_count , data = abrep)

library(PerformanceAnalytics)

chart.Correlation(abdem, histogram = TRUE, method = "pearson")
chart.Correlation(abrep, histogram = TRUE, method = "pearson")
par(mfrow=c(5,5))

#shapiro.test(abdem$dyad_ratio) 
#shapiro.test(abrep$dyad_ratio) 

hist(abdem$dcc,main='democract dcc')
hist(abrep$dcc,main='republican dcc')
hist(abdem$reciprocity,main='democrat recp')
hist(abrep$reciprocity,main='republican recp')
hist(abdem$undirected_tc,main='democrat undirect')
hist(abrep$undirected_tc,main='republican undirect')
hist(abdem$triad_count,main='democrat traid count')
hist(abrep$triad_count,main='republican traid count')
hist(abdem$dyad_ratio,main='democrat dyad ratio')
hist(abrep$dyad_ratio,main='republican dyad ratio')


#boxplots of each metrics
boxplot(abdem$dcc,abrep$dcc,ylab = "clustering",names = c("democrat","republican"), main = "DCC metric")
boxplot(abdem$reciprocity,abrep$reciprocity, ylab = "reciprocity",names = c("democrat","republican"),main = "Reciprocity metric")
boxplot(abdem$triad_count,abrep$triad_count,ylab = "triad count",names = c("democrat","republican"), main = "Triad count metric")
boxplot(abdem$dyad_ratio,abrep$dyad_ratio,ylab = "dyad ratio",names = c("democrat","republican"), main = "Dyad ratio metric")
#Mann-Whitney-Wilcoxon U Test for independent samples;
#H0:Metric of democrat and metric of republicans are identical populations

wilcox.test(abdem$dcc,abrep$dcc) 
wilcox.test(abdem$reciprocity,abrep$reciprocity) 
wilcox.test(abdem$triad_count,abrep$traid_count) 
wilcox.test(abdem$dyad_ratio,abrep$dyad_ratio) 




gcdem=read.csv('gc_metadata_democrat.csv')
gcrep=read.csv('gc_metadata_republican.csv')
hist(gcdem$dcc,col='green',main='Gun control directed clustering coefficient')
hist(gcrep$dcc,col='blue',add=TRUE)
hist(gcdem$reciprocity)
hist(gcdem$undirected_tc)
hist(gcdem$triad_count)
hist(gcdem$dyad_ratio)

#t.test(gcdem$triad_count ~ gcrep$triad_count,paired=TRUE)



hist(gcrep$reciprocity)
hist(gcrep$undirected_tc)
hist(gcrep$triad_count)
hist(gcrep$dyad_ratio)

obdem=read.csv('ob_metadata_democrat.csv')

hist(obdem$dcc)
hist(obdem$reciprocity)
hist(obdem$undirected_tc)
hist(obdem$triad_count)
hist(obdem$dyad_ratio)

obrep=read.csv('ob_metadata_republican.csv')

hist(obrep$dcc)
hist(obrep$reciprocity)
hist(obrep$undirected_tc)
hist(obrep$triad_count)
hist(obrep$dyad_ratio)
