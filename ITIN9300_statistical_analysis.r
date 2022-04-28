setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
#ABORTION DATASET
abdem=read.csv('ab_metadata_democrat.csv')
abrep=read.csv('ab_metadata_republican.csv')
pairs(~dcc +reciprocity+ dyad_ratio + triad_count , data = abdem)
pairs(~dcc +reciprocity+ dyad_ratio + triad_count , data = abrep)

shapiro.test(abdem$dcc) 
shapiro.test(abrep$dcc) 
shapiro.test(abdem$reciprocity) 
shapiro.test(abrep$reciprocity) 
shapiro.test(abdem$dyad_ratio) 
shapiro.test(abrep$dyad_ratio) 
shapiro.test(abdem$triad_count) 
shapiro.test(abrep$triad_count) 
#q-q plots for abortion dataset

qqnorm(abdem$dcc, pch = 1, frame = FALSE)
qqline(abdem$dcc, col = "steelblue", lwd = 2)

qqnorm(abrep$dcc, pch = 1, frame = FALSE)
qqline(abrep$dcc, col = "steelblue", lwd = 2)

qqnorm(abdem$reciprocity, pch = 1, frame = FALSE)
qqline(abdem$reciprocity, col = "steelblue", lwd = 2)

qqnorm(abrep$reciprocity, pch = 1, frame = FALSE)
qqline(abrep$reciprocity, col = "steelblue", lwd = 2)


qqnorm(abdem$dyad_ratio, pch = 1, frame = FALSE)
qqline(abdem$dyad_ratio, col = "steelblue", lwd = 2)

qqnorm(abrep$dyad_ratio, pch = 1, frame = FALSE)
qqline(abrep$dyad_ratio, col = "steelblue", lwd = 2)
#HISTOGRAM for abortion dataset
par(mfrow=c(5,5))
hist(abdem$dcc,main='abortion dcc',col='green')
hist(abrep$dcc,main='abortion dcc',col = 'blue',add=TRUE)
hist(abdem$reciprocity,main='democrat recp')
hist(abrep$reciprocity,main='republican recp')
hist(abdem$undirected_tc,main='democrat undirect')
hist(abrep$undirected_tc,main='republican undirect')
hist(abdem$triad_count,main='democrat traid count')
hist(abrep$triad_count,main='republican traid count')
hist(abdem$dyad_ratio,main='democrat dyad ratio')
hist(abrep$dyad_ratio,main='republican dyad ratio')


#boxplots of each metrics for abortion
boxplot(abdem$dcc,abrep$dcc,ylab = "clustering",names = c("democrat","republican"), main = "DCC metric")
boxplot(abdem$reciprocity,abrep$reciprocity, ylab = "reciprocity",names = c("democrat","republican"),main = "Reciprocity metric")
boxplot(abdem$triad_count,abrep$triad_count,ylab = "triad count",names = c("democrat","republican"), main = "Triad count metric")
boxplot(abdem$dyad_ratio,abrep$dyad_ratio,ylab = "dyad ratio",names = c("democrat","republican"), main = "Dyad ratio metric")
#Statistical t-test for abortion dataset
t.test(abdem$dcc,abrep$dcc) 
t.test(abdem$reciprocity,abrep$reciprocity) 
t.test(abdem$triad_count,abrep$traid_count) 
t.test(abdem$dyad_ratio,abrep$dyad_ratio) 



##GUN CONTROL DATASET
gcdem=read.csv('gc_metadata_democrat.csv')
gcrep=read.csv('gc_metadata_republican.csv')
hist(gcdem$dcc,col='green',main='Gun control directed clustering coefficient')
hist(gcrep$dcc,col='blue',add=TRUE)
hist(gcdem$reciprocity)
hist(gcdem$undirected_tc)
hist(gcdem$triad_count)
hist(gcdem$dyad_ratio)
hist(gcrep$reciprocity)
hist(gcrep$undirected_tc)
hist(gcrep$triad_count)
hist(gcrep$dyad_ratio)
#boxplots for gun control
boxplot(gcdem$dcc,gcrep$dcc,ylab = "clustering",names = c("democrat","republican"), main = "DCC metric")
boxplot(gcdem$reciprocity,gcrep$reciprocity, ylab = "reciprocity",names = c("democrat","republican"),main = "Reciprocity metric")
boxplot(gcdem$triad_count,gcrep$triad_count,ylab = "triad count",names = c("democrat","republican"), main = "Triad count metric")
boxplot(gcdem$dyad_ratio,gcrep$dyad_ratio,ylab = "dyad ratio",names = c("democrat","republican"), main = "Dyad ratio metric")
#q-q plots for gun control
qqnorm(gcdem$dcc, pch = 1, frame = FALSE)
qqline(gcdem$dcc, col = "steelblue", lwd = 2)
qqnorm(gcrep$dcc, pch = 1, frame = FALSE)
qqline(gcrep$dcc, col = "steelblue", lwd = 2)
qqnorm(gcdem$reciprocity, pch = 1, frame = FALSE)
qqline(gcdem$reciprocity, col = "steelblue", lwd = 2)
qqnorm(gcrep$reciprocity, pch = 1, frame = FALSE)
qqline(gcrep$reciprocity, col = "steelblue", lwd = 2)
qqnorm(gcdem$dyad_ratio, pch = 1, frame = FALSE)
qqline(gcdem$dyad_ratio, col = "steelblue", lwd = 2)
qqnorm(gcrep$dyad_ratio, pch = 1, frame = FALSE)
qqline(gcrep$dyad_ratio, col = "steelblue", lwd = 2)

# Statistical t test for gun control
t.test(gcdem$dcc,gcrep$dcc) 
t.test(gcdem$reciprocity,gcrep$reciprocity) 
t.test(gcdem$triad_count,gcrep$traid_count) 
t.test(gcdem$dyad_ratio,gcrep$dyad_ratio) 

##OBAMA CARE DATASET

obdem=read.csv('ob_metadata_democrat.csv')
obrep=read.csv('ob_metadata_republican.csv')
hist(obdem$dcc)
hist(obdem$reciprocity)
hist(obdem$undirected_tc)
hist(obdem$triad_count)
hist(obdem$dyad_ratio)
hist(obrep$dcc)
hist(obrep$reciprocity)
hist(obrep$undirected_tc)
hist(obrep$triad_count)
hist(obrep$dyad_ratio)
#boxplot obama care dataset
boxplot(obdem$dcc,obrep$dcc,ylab = "clustering",names = c("democrat","republican"), main = "DCC metric")
boxplot(obdem$reciprocity,obrep$reciprocity, ylab = "reciprocity",names = c("democrat","republican"),main = "Reciprocity metric")
boxplot(obdem$triad_count,obrep$triad_count,ylab = "triad count",names = c("democrat","republican"), main = "Triad count metric")
boxplot(obdem$dyad_ratio,obrep$dyad_ratio,ylab = "dyad ratio",names = c("democrat","republican"), main = "Dyad ratio metric")
#q-q plots for obama care
qqnorm(obdem$dcc, pch = 1, frame = FALSE)
qqline(obdem$dcc, col = "steelblue", lwd = 2)
qqnorm(obrep$dcc, pch = 1, frame = FALSE)
qqline(obrep$dcc, col = "steelblue", lwd = 2)
qqnorm(obdem$reciprocity, pch = 1, frame = FALSE)
qqline(obdem$reciprocity, col = "steelblue", lwd = 2)
qqnorm(obrep$reciprocity, pch = 1, frame = FALSE)
qqline(obrep$reciprocity, col = "steelblue", lwd = 2)
qqnorm(obdem$dyad_ratio, pch = 1, frame = FALSE)
qqline(obdem$dyad_ratio, col = "steelblue", lwd = 2)
qqnorm(obrep$dyad_ratio, pch = 1, frame = FALSE)
qqline(obrep$dyad_ratio, col = "steelblue", lwd = 2)

#Statistical t test for obama care
t.test(obdem$dcc,obrep$dcc) 
t.test(obdem$reciprocity,obrep$reciprocity) 
t.test(obdem$triad_count,obrep$traid_count) 
t.test(obdem$dyad_ratio,obrep$dyad_ratio) 
