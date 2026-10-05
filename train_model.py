import json, re, unicodedata, math
from collections import defaultdict, Counter
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=re.sub(r'[\u0300-\u036f]','',s)
    return re.sub(r'[^a-z0-9]+',' ',s).strip()
def feats(s):
    out=set()
    for w in norm(s).split():
        out.add('#'+w); p='<'+w+'>'
        for n in (3,4):
            for i in range(len(p)-n+1): out.add(p[i:i+n])
    return out
def train(rows,labels,alpha):
    classes=sorted(set(labels)); fc={c:Counter() for c in classes}; cc=Counter(labels); df=Counter()
    for r,l in zip(rows,labels):
        f=feats(r); fc[l].update(f); df.update(f)
    vocab=sorted(f for f,n in df.items() if n>=2)
    V=len(vocab); model={'classes':classes,'prior':[],'vocab':vocab,'w':[]}
    tot={c:sum(fc[c][f] for f in vocab) for c in classes}
    for c in classes: model['prior'].append(round(math.log(cc[c]/len(labels)),3))
    for f in vocab:
        model['w'].append([round(math.log((fc[c][f]+alpha)/(tot[c]+alpha*V)),2) for c in classes])
    return model
def predict(m,s):
    idx=m.get('_i') or {f:i for i,f in enumerate(m['vocab'])}; m['_i']=idx
    sc=list(m['prior'])
    for f in feats(s):
        if f in idx:
            w=m['w'][idx[f]]
            for k in range(len(sc)): sc[k]+=w[k]
    mx=max(sc); ex=[math.exp(x-mx) for x in sc]; Z=sum(ex)
    best=max(range(len(sc)),key=lambda k:sc[k]); return m['classes'][best], ex[best]/Z
rows=json.load(open('train.json'))
X=[r[0] for r in rows]
mi=train(X,[r[1] for r in rows],0.3); ml=train(X,[r[2] for r in rows],0.3)
test=[('Which districts grew the most maize?','top_districts','en'),('How big is the yield gap for Irish potatoes?','yield','en'),
('How did input use change across the seasons?','input_use','en'),('where are sweet potatoes grown','top_districts','en'),
('how much cassava did rwanda produce','production','en'),('what percent of smallholders used improved seed in season B','input_gap','en'),
('Ni utuhe turere twejeje ibigori byinshi?','top_districts','rw'),("Icyuho mu musaruro w'ibirayi kingana iki?",'yield','rw'),
("Ikoreshwa ry'inyongeramusaruro ryahindutse rite mu bihembwe?",'input_use','rw'),('Quels districts ont produit le plus de maïs ?','top_districts','fr'),
("Quel est l'écart de rendement pour la pomme de terre ?",'yield','fr'),("Comment l'usage des intrants a-t-il changé selon les saisons ?",'input_use','fr'),
('who will win the election','other','en'),('how do i fix my laptop','other','en'),('ni nde perezida wa Amerika','other','rw'),
('quelle heure est-il','other','fr'),('how much land is cultivated in rwanda','land','en'),('when does season b end','seasons','en'),
('how much maize per hectare do big farms get','yield','en'),('pesticide most popular','pest_brand','en'),('umusaruro w imyumbati','production','rw'),
('ubuso bw ibirayi mu gihembwe B','area','rw'),('engrais chez les petits exploitants','input_gap','fr'),('salut','greet','fr'),('murakoze cyane','greet','rw'),
('what about season B?','production','en'),('do farmers use manure','input_use','en'),('Is Musanze a big potato district','top_districts','en'),
('soil erosion','erosion','en'),('who collected this data','about','en'),('my farm is 0.5 ha of maize, how much will I get','yield','en')]
ok=0
for q,i,l in test:
    pi,p=predict(mi,q); pl,pp=predict(ml,q); ok+=pi==i
    print(('OK ' if pi==i else 'XX ')+('  ' if pl==l else 'L!'),f'{p:.2f}',pi,'|',pl,f'{pp:.2f}','|',q)
print(ok,'/',len(test))
for m,n in ((mi,'intent'),(ml,'lang')):
    m.pop('_i',None); json.dump(m,open(n+'.json','w'),separators=(',',':'))
import os; print(len(mi['vocab']),os.path.getsize('intent.json'),os.path.getsize('lang.json'))
# compact export with pruning
def export(m,name,minspread):
    keep=[k for k,w in enumerate(m['w']) if max(w)-min(w)>=minspread]
    vocab=[m['vocab'][k] for k in keep]
    W=[int(round(x*10)) for k in keep for x in m['w'][k]]
    out={'c':m['classes'],'p':m['prior'],'v':' '.join(vocab),'w':','.join(map(str,W))}
    json.dump(out,open(name+'.min.json','w'),separators=(',',':'))
    m2={'classes':m['classes'],'prior':m['prior'],'vocab':vocab,'w':[[W[i*len(m['classes'])+j]/10 for j in range(len(m['classes']))] for i in range(len(vocab))]}
    return m2, os.path.getsize(name+'.min.json')
for sp in (0.5,1.0,1.5):
    a,sz=export(json.load(open('intent.json')),'intent',sp)
    b,sz2=export(json.load(open('lang.json')),'lang',sp)
    tr=sum(predict(a,q)[0]==i for q,i,l in rows)/len(rows)
    te=sum(predict(a,q)[0]==i for q,i,l in test)
    tl=sum(predict(b,q)[0]==l for q,i,l in rows)/len(rows)
    print(sp,sz,sz2,'train',round(tr,3),'test',te,'lang',round(tl,3))
def export2(m,name):
    C=len(m['classes'])
    base=[min(w[c] for w in m['w']) for c in range(C)]
    vocab=[];ent=[]
    for f,w in zip(m['vocab'],m['w']):
        parts=[f"{c}{'' if True else ''}:{int(round((w[c]-base[c])*10))}" for c in range(C) if round((w[c]-base[c])*10)!=0]
        vocab.append(f); ent.append(';'.join(p.replace(':','') if False else p for p in parts))
    out={'c':m['classes'],'p':m['prior'],'b':base,'v':' '.join(vocab),'w':'|'.join(ent)}
    json.dump(out,open(name+'.min.json','w'),separators=(',',':'))
    # reconstruct for eval
    m2={'classes':m['classes'],'prior':m['prior'],'vocab':vocab,'w':[]}
    for e in ent:
        w=list(base)
        for p in e.split(';'):
            if p: c,v=p.split(':'); w[int(c)]=base[int(c)]+int(v)/10
        m2['w'].append(w)
    return m2, os.path.getsize(name+'.min.json')
a,sz=export2(json.load(open('intent.json')),'intent'); b,sz2=export2(json.load(open('lang.json')),'lang')
print('sparse',sz,sz2,'train',round(sum(predict(a,q)[0]==i for q,i,l in rows)/len(rows),3),'test',sum(predict(a,q)[0]==i for q,i,l in test),'lang',round(sum(predict(b,q)[0]==l for q,i,l in rows)/len(rows),3))
