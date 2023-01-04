gcdem=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/gc_metadata_democrat.csv')
gcrep=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/gc_metadata_republican.csv')
t.test(gcdem$dcc,gcrep$dcc) 
t.test(gcdem$reciprocity,gcrep$reciprocity) 
t.test(gcdem$dyad_ratio,gcrep$dyad_ratio) 
t.test(gcdem$triad_count,gcrep$traid_count)
#t.test(gcdem$triad_count,gcrep$traid_count)
#do tmr  with tc/untc and find t test for each
gcrep$tmr=gcrep$triad_count/gcrep$undirected_tc
gcdem$tmr=gcdem$triad_count/gcdem$undirected_tc
t.test(gcdem$tmr,gcrep$tmr)


gcdemext=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/metadata_extdemocrat_guncontrol.csv')
gcrepext=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/metadata_extrepublican_guncontrol.csv')
t.test(gcdemext$dcc,gcrepext$dcc) 
t.test(gcdemext$reciprocity,gcrepext$reciprocity) 
#t.test(gcdemext$triad_count,gcrepext$traid_count) 
t.test(gcdemext$dyad_ratio,gcrepext$dyad_ratio) 
gcrepext$tmr=gcrepext$triad_count/gcrepext$undirected_tc
gcdemext$tmr=gcdemext$triad_count/gcdemext$undirected_tc
t.test(gcdemext$tmr,gcrepext$tmr)
