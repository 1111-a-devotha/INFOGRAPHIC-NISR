import random, re, json, unicodedata
random.seed(7)
L={}
C={'en':{'maize':['maize','corn'],'potato':['irish potatoes','potatoes','potato','irish potato'],'cassava':['cassava'],'sweet':['sweet potatoes','sweet potato']},
   'fr':{'maize':['maïs','mais'],'potato':['pommes de terre','pomme de terre'],'cassava':['manioc'],'sweet':['patates douces','patate douce']},
   'rw':{'maize':['ibigori'],'potato':['ibirayi'],'cassava':['imyumbati'],'sweet':['ibijumba']}}
S={'en':['season A','season B','season C','Season A','Season B'],'fr':['saison A','saison B','saison C'],'rw':['igihembwe A','igihembwe B','igihembwe C',"igihembwe cy'ihinga A","igihembwe cy'ihinga B"]}
I={'en':['improved seeds','improved seed','organic fertilizer','manure','inorganic fertilizer','chemical fertilizer','pesticides','fertilizer','compost','NPK'],
   'fr':['semences améliorées','engrais organique','fumier','engrais minéraux','engrais chimiques','pesticides','engrais'],
   'rw':["imbuto z'indobanure","ifumbire y'imborera",'ifumbire mvaruganda','imiti yica udukoko','ifumbire','imiti']}
D=['Musanze','Nyagatare','Rubavu','Nyabihu','Gatsibo','Huye','Kirehe','Rusizi','Gakenke','Bugesera','Kayonza','Nyamagabe']
T={
'top_districts':{
'en':['Which districts grew the most {c}?','Which district produces the most {c}?','Where is most {c} grown?','top {c} districts','Top producing districts for {c}','Where do they grow {c} in Rwanda?','Which areas lead in {c} production?','best districts for {c}','Is {d} a top {c} producer?','What does {d} grow the most?','which districts are the biggest producers','Where is {c} produced most in {s}?','leading districts','which region grows {c}','What crops is {d} known for?','Tell me about {d} district','where does {c} grow','where do {c} grow best'],
'fr':['Quels districts ont produit le plus de {c} ?','Quel district produit le plus de {c} ?','Où cultive-t-on le plus de {c} ?','principaux districts producteurs de {c}','Où se cultive le {c} au Rwanda ?','Quelles régions produisent le plus de {c} ?','{d} est-il un grand producteur de {c} ?','Que produit le district de {d} ?','les meilleurs districts pour le {c}','quels sont les premiers districts producteurs','Où pousse le {c} ?','Où pousse la {c} ?'],
'rw':['Ni utuhe turere twejeje {c} byinshi?','Ni akahe karere keza {c} byinshi?','{c} byera cyane he?','Ni hehe hahingwa {c} cyane?','Uturere twa mbere mu {c}','Ni utuhe turere duhinga {c} cyane?','Ese {d} ni kamwe mu turere twera {c} cyane?','Akarere ka {d} keza iki cyane?','Ni utuhe turere tuza imbere mu musaruro','{c} bihingwa cyane mu turere tuhe?','Mbwira ku karere ka {d}']},
'yield':{
'en':['How big is the yield gap for {c}?','What is the {c} yield?','How many tonnes per hectare of {c}?','yield of {c} for small farmers','Do large farms harvest more {c} per hectare?','{c} yield small vs large farmers','How much {c} does one hectare give?','average yield of {c}','How much more do big farms harvest?','productivity per hectare','How much would my 2 ha farm produce?','If I plant 3 hectares of {c}, how much will I harvest?','tonnes per hectare','yield gap','why do large farmers get higher yields?','compare {c} yields','harvest per hectare for {c} in {s}'],
'fr':["Quel est l'écart de rendement pour la {c} ?",'Quel est le rendement du {c} ?','Combien de tonnes par hectare de {c} ?','rendement des petits exploitants','Les grandes fermes récoltent-elles plus de {c} ?','rendement moyen du {c}','Combien récolterait ma ferme de 2 ha ?','Si je plante 3 hectares de {c}, combien vais-je récolter ?','écart de rendement','tonnes par hectare de {c} en {s}','pourquoi les grands exploitants ont de meilleurs rendements ?'],
'rw':["Icyuho mu musaruro w'{c} kingana iki?","Umusaruro w'{c} kuri hegitari ni uwuhe?",'Hegitari imwe yeza toni zingahe?',"Abahinzi bato basarura {c} bingahe kuri hegitari?",'Abahinzi banini beza kurusha abato ku kihe kigero?',"Umusaruro mpuzandengo w'{c}",'Umurima wanjye wa hegitari 2 wakweza angahe?',"Nimpinga hegitari 3 z'{c} nzasarura angahe?",'Toni kuri hegitari','Icyuho mu musaruro','Kuki abahinzi banini beza cyane?',"Umusaruro kuri hegitari mu {s}"]},
'production':{
'en':['How much {c} was produced in {s}?','total {c} production','How many tonnes of {c} were harvested?','Did {c} production go up or down?','{c} production change from 2024','Which crop produced the most?','production in {s}','how much did the country harvest of {c}','Did {c} output increase?','biggest harvest','compare production of crops','What was the {c} harvest in {s} 2025?','how much {c} did Rwanda produce','How many tonnes of {c}?','tonnes of {c} harvested in {s}','{c} tonnes'],
'fr':['Combien de {c} a été produit en {s} ?','production totale de {c}','Combien de tonnes de {c} ont été récoltées ?','La production de {c} a-t-elle augmenté ?','Quelle culture a le plus produit ?','production en {s}','variation de la production de {c} par rapport à 2024','récolte de {c} en {s} 2025','Combien de tonnes de {c} ?','tonnes de {c} en {s}'],
'rw':["Umusaruro w'{c} wari ungana iki mu {s}?","Hasaruwe toni zingahe z'{c}?","Umusaruro w'{c} wiyongereye cyangwa wagabanutse?",'Ni ikihe gihingwa cyeze cyane?',"Umusaruro wose w'{c}","Umusaruro mu {s}","Impinduka mu musaruro w'{c} ugereranyije na 2024","U Rwanda rwasaruye {c} bingana iki?","Toni zingahe z'{c}?","Toni z'{c} zasaruwe mu {s}"]},
'area':{
'en':['How much land was planted with {c}?','cultivated area of {c}','How many hectares of {c} in {s}?','area under {c}','Did the {c} area grow?','hectares planted with {c}','how big is the {c} area'],
'fr':['Quelle superficie est cultivée en {c} ?','superficie de {c} en {s}','Combien d\'hectares de {c} ?','surface cultivée de {c}','La superficie de {c} a-t-elle augmenté ?'],
'rw':["Ubuso buhinzeho {c} ni bungahe?","Hegitari zingahe zahinzweho {c} mu {s}?","Ubuso bwa {c}","Ubuso buhingwaho {c} bwariyongereye?"]},
'input_use':{
'en':['How did input use change across the seasons?','What share of farmers used {i}?','How many farmers use {i}?','percentage of farmers using {i} in {s}','use of {i}','Which input is used the most?','input use in {s}','Did {i} use go down in {s}?','how common is {i}','What percent of farmers apply {i}?','farm inputs','trend in {i} use','most common farm input'],
'fr':["Comment l'usage des intrants a-t-il changé selon les saisons ?",'Quelle part des agriculteurs utilise des {i} ?','Combien d\'agriculteurs utilisent des {i} ?','pourcentage d\'agriculteurs utilisant {i} en {s}','utilisation des {i}','Quel intrant est le plus utilisé ?','intrants en {s}','usage des intrants'],
'rw':["Ikoreshwa ry'inyongeramusaruro ryahindutse rite mu bihembwe?",'Abahinzi bangahe bakoresha {i}?',"Ijanisha ry'abahinzi bakoresheje {i} mu {s}","Ikoreshwa rya {i}",'Ni iyihe nyongeramusaruro ikoreshwa cyane?','Inyongeramusaruro mu {s}','Ese {i} byakoreshejwe gake mu {s}?','Inyongeramusaruro']},
'input_gap':{
'en':['What is the gap between small and large farmers in {i}?','Do smallholders use {i} less than large farmers?','{i} use small vs large farms','How many smallholders use {i}?','What percent of large-scale farmers used {i} in {s}?','compare small and large farmers','input gap','Who uses more {i}, small or large farmers?','smallholder input use','large scale farmers inputs'],
'fr':['Quel est l\'écart entre petits et grands exploitants pour les {i} ?','Les petits exploitants utilisent-ils moins de {i} ?','Combien de petits exploitants utilisent des {i} ?','écart d\'intrants','comparer petits et grands exploitants','Qui utilise plus de {i}, les petits ou les grands ?','intrants des grands exploitants en {s}'],
'rw':['Icyuho hagati y\'abahinzi bato n\'abanini muri {i} kingana iki?','Abahinzi bato bakoresha {i} gake kurusha abanini?','Abahinzi bato bangahe bakoresha {i}?','Abahinzi banini bakoresheje {i} ku kihe kigero mu {s}?','Icyuho mu nyongeramusaruro','Gereranya abahinzi bato n\'abanini','Ni bande bakoresha {i} cyane, abato cyangwa abanini?']},
'land':{
'en':['How much of Rwanda is farmland?','agricultural land','How much land is used for farming?','total land area','What share of land is agricultural?','permanent crops area','land use in {s}','permanent pasture','How many hectares does Rwanda have?'],
'fr':['Quelle part du Rwanda est agricole ?','terres agricoles','Combien de terres sont utilisées pour l\'agriculture ?','superficie totale du pays','cultures permanentes','pâturages permanents','utilisation des terres en {s}'],
'rw':["Ubutaka bukoreshwa mu buhinzi ni bungahe?","Ubuso bw'u Rwanda bwose","Ijanisha ry'ubutaka bw'ubuhinzi",'Ubutaka bw\'ubuhinzi mu {s}','Ibihingwa bihoraho','Inzuri zihoraho']},
'seasons':{
'en':['When is {s}?','What are the agricultural seasons?','How many seasons are there?','When does season A start?','which months are {s}','What is season C?','explain the seasons','how long is {s}'],
'fr':['Quand a lieu la {s} ?','Quelles sont les saisons agricoles ?','Combien de saisons y a-t-il ?','Quels mois couvre la {s} ?','Qu\'est-ce que la saison C ?'],
'rw':['{s} kiba ryari?','Ibihembwe by\'ihinga ni ibihe?','Hari ibihembwe bingahe?','Igihembwe A gitangira ryari?','{s} kigizwe n\'amezi ayahe?','Igihembwe C ni iki?']},
'pest_brand':{
'en':['Which pesticide is used the most?','most used pesticides','What is Rocket?','How many farmers use Dithane?','pesticide brands','Cypermethrin use','top pesticide products'],
'fr':['Quel pesticide est le plus utilisé ?','pesticides les plus utilisés','marques de pesticides','utilisation de Dithane'],
'rw':['Ni uwuhe muti wica udukoko ukoreshwa cyane?','Imiti ikoreshwa cyane','Rocket ikoreshwa ku kihe kigero?','Amoko y\'imiti yica udukoko']},
'erosion':{
'en':['soil erosion control','How many farmers fight soil erosion?','erosion measures','What share of farmers protect their soil from erosion?','terraces and erosion'],
'fr':["lutte contre l'érosion",'Combien d\'agriculteurs luttent contre l\'érosion ?','érosion des sols'],
'rw':['Kurwanya isuri','Abahinzi bangahe barwanya isuri?','Isuri','Ingamba zo kurwanya isuri']},
'about':{
'en':['Where does this data come from?','What is the source?','Who made this?','What survey is this?','How many farmers were surveyed?','sample size','Is this data official?','what is SAS','what is NISR'],
'fr':['D\'où viennent ces données ?','Quelle est la source ?','Qui a fait cette infographie ?','Quelle enquête est-ce ?','Combien d\'agriculteurs ont été interrogés ?'],
'rw':['Aya makuru aturuka he?','Inkomoko y\'aya makuru ni iyihe?','Ni nde wakoze ibi?','Ubu ni ubuhe bushakashatsi?','Hakozwe ubushakashatsi ku bahinzi bangahe?']},
'greet':{
'en':['hello','hi','hey there','good morning','what can you do?','help','how do I use this?','thanks','thank you','who are you?'],
'fr':['bonjour','salut','merci','aide','que peux-tu faire ?','qui es-tu ?','bonsoir'],
'rw':['muraho','mwaramutse','mwiriwe','murakoze','ufasha iki?','uri nde?','amakuru','bite','ndashaka ubufasha']},
'other':{
'en':['What is the weather tomorrow?','Who won the football match?','Who is the president of France?','tell me a joke','write a python program','what is the capital of Kenya','price of a phone','How do I plant {c}?','How do I grow {c}?','how to plant {c} in {s}','what is the best way to grow {c}','best time to plant {c}','How do I cook {c}?','recipe for {c}','where can I buy {i}?','how to apply {i}','Is {i} safe for my health?','what is love','translate this to English','how old are you','what is 2+2','give me the news','how to start a business','Bitcoin price','how many people live in Kigali','book a hotel in {d}','bus from {d} to Kigali','who will win the election','what time is it','who is the president of Rwanda','what is your name','sing a song','how to lose weight','what is the best phone','who invented the internet','what year is it','play music','what is the meaning of life','how do I learn English'],
'fr':['Quel temps fera-t-il demain ?','Qui a gagné le match ?','Raconte-moi une blague','Quelle est la capitale du Kenya ?','Comment planter le {c} ?','Comment cultiver le {c} ?','Comment cuisiner le {c} ?','Où acheter des {i} ?','prix du téléphone','les nouvelles du jour','hôtel à {d}','quelle heure est-il','qui va gagner les élections','qui est le président','comment apprendre l\'anglais','quel est ton nom','chante une chanson'],
'rw':['Ejo hazaba ikirere kimeze gute?','Ni nde watsinze umupira?','Nsetsa','Umurwa mukuru wa Kenya ni uwuhe?','Nahinga nte {c}?','Nakwita nte ku {c}?','Ni ryari nahinga {c}?','Nteka nte {c}?','Nagura he {i}?','Amakuru y\'uyu munsi','Igiciro cya telefone','Imodoka iva {d} ijya i Kigali','Ni nde perezida wa Amerika','Ni saa ngahe?','Witwa nde?','Ndirimbira','Nakwiga nte icyongereza','Ni nde uzatsinda amatora']}
}
def fill(tpl,lang):
    return (tpl.replace('{c}',random.choice(sum(C[lang].values(),[])))
             .replace('{s}',random.choice(S[lang])).replace('{i}',random.choice(I[lang])).replace('{d}',random.choice(D)))
def typo(s):
    if len(s)<6: return s
    i=random.randrange(len(s)); op=random.random()
    if op<.4: return s[:i]+s[i+1:]
    if op<.7 and i<len(s)-1: return s[:i]+s[i+1]+s[i]+s[i+2:]
    return s[:i]+random.choice('aeioustrn')+s[i:]
rows=[]
for intent,by in T.items():
    for lang,tpls in by.items():
        for tpl in tpls:
            n=10 if '{' in tpl else 5
            for k in range(n):
                q=fill(tpl,lang)
                r=random.random()
                if r<.25: q=q.lower()
                elif r<.4: q=typo(q)
                elif r<.5: q=re.sub(r'[?!.]','',q)
                rows.append((q,intent,lang))
json.dump(rows,open('train.json','w'),ensure_ascii=False)
print(len(rows))
from collections import Counter
print(Counter(r[1] for r in rows)); print(Counter(r[2] for r in rows))
