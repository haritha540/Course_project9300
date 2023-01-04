obdem=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/ob_metadata_democrat.csv')
obrep=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/ob_metadata_republican.csv')
t.test(obdem$dcc,obrep$dcc) 
t.test(obdem$reciprocity,obrep$reciprocity) 
#t.test(obdem$triad_count,obrep$traid_count) 
t.test(obdem$dyad_ratio,obrep$dyad_ratio)
obrep$tmr=obrep$triad_count/obrep$undirected_tc
obdem$tmr=obdem$triad_count/obdem$undirected_tc
t.test(obdem$tmr,obrep$tmr)

obdemext=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/metadata_extdemocrat_obama.csv')
obrepext=read.csv('C:/Users/harit/Desktop/filterbubblescripts/Metadata/metadata_extrepublican_obamacare.csv')

t.test(obdemext$dcc,obrepext$dcc) 
t.test(obdemext$reciprocity,obrepext$reciprocity) 
#t.test(obdemext$triad_count,obrepext$traid_count) 
t.test(obdemext$dyad_ratio,obrepext$dyad_ratio) 
obrepext$tmr=obrepext$triad_count/obrepext$undirected_tc
obdemext$tmr=obdemext$triad_count/obdemext$undirected_tc
t.test(obdemext$tmr,obrepext$tmr)
