import numpy as np
import matplotlib.pyplot as plt
import statistics as s
import scipy.stats as stats
import pandas as pd
import seaborn as sns
import math

#Exercice 10

#1ab
with open("televisions.dat", "r") as tele:
    televisions=tele.read()
print(televisions)

#2
with open("televisions.dat", "r") as tele :
    lines=[line.split() for line in tele]
    lines.pop(0)
    Pays=[]
    espe_vie=[]
    tv=[]
    ph=[]
    espe_vieF=[]
    espe_vieH=[]
    for data in lines:
        if len(data)==6:
            Pays.append(data[0])
            espe_vie.append(float(data[1]))
            tv.append(float(data[2]))
            ph.append(float(data[3]))
            espe_vieF.append(float(data[4]))
            espe_vieH.append(float(data[5]))
        elif len(data)==5:
            Pays.append(data[0])
            espe_vie.append(float(data[1]))
            tv.append(0)
            ph.append(float(data[2]))
            espe_vieF.append(float(data[3]))
            espe_vieH.append(float(data[4]))
        else:
            Pays.append(data[0]+" "+data[1])
            espe_vie.append(float(data[2]))
            tv.append(float(data[3]))
            ph.append(float(data[4]))
            espe_vieF.append(float(data[5]))
            espe_vieH.append(float(data[6]))
print("2)",'\n',"Nb pays :",len(Pays),'\n',"Esperance vie moyenne :", np.mean(espe_vie),'\n',"Nb moyen de personnes par tv :", np.mean(tv),'\n',"Nb moyen de personnes par médecin :", np.mean(ph),'\n',"Esperance de vie moyenne des femmes :", np.mean(espe_vieF),'\n',"Esperance de vie moyenne des hommes:", np.mean(espe_vieH),"\n",)

#3
plt.figure(figsize=(10, 5))
plt.bar(Pays,tv)
plt.xticks(rotation=90)
plt.ylabel("Nb de personnes")
plt.title("Nb personnes par TV par pays")
plt.legend()
plt.grid()
plt.show()
plt.figure(figsize=(10,5))
plt.bar(Pays,ph)
plt.xticks(rotation=90)
plt.ylabel("Nb de personnes")
plt.title("Nb de personnes par médecin par pays")
plt.grid()
plt.show()

#4
plt.hist(espe_vie, bins=100)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de pays")
#plt.title("Espérance de vie")
plt.grid()
plt.show()
sns.boxplot(data=espe_vie,orient="h").set_title("")
#Boite de dispersion espérance de vie
plt.show()
plt.hist(espe_vieF, bins=100)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de pays")
#plt.title("Espérance de vie des femmes")
plt.grid()
plt.show()
sns.boxplot(data = espe_vieF, orient ="h").set_title("")
#Boite de dispersion espérance de vie femmes
plt.show()
plt.hist(espe_vieH, bins = 100)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de pays")
#plt.title("Esperance de vie hommes")
plt.grid()
plt.show()
sns.boxplot(data = espe_vieH, orient ="h").set_title("")
#Boîte de dispersion espérance de vie hommes
plt.show()

#5
plt.scatter(espe_vie, tv)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de personnes par télévisions")
#plt.title("Correlation entre espérance de vie et tv")
plt.grid()
plt.show()
Tv1=[]
espvie1=[]
for i in range(len(tv)):       
    if (tv[i]!=0 and tv[i]<300) :
       Tv1.append(tv[i])
       espvie1.append(espe_vie[i])
plt.scatter(espvie1, Tv1)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de personnes par télévisions")
#plt.title("Correlation entre espe_vie et tv sans valeurs extremes")
plt.grid()
plt.show()
print("5)", '\n',np.log10(Tv1))
plt.scatter(espvie1, np.log10(Tv1))
plt.xlabel("Esperance de vie")
plt.ylabel("log(tv)")
#plt.title("log(tv) en fonction de espe_vie")
plt.grid()
plt.show()

#6
plt.scatter(espe_vie, ph)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de personnes par médecin")
#plt.title("Correlation entre espe_vie et ph")
plt.grid()
plt.show()
Ph1=[]
espvie1=[]
for i in range(len(tv)):       
    if (ph[i]!=0 and ph[i]<15000):
       Ph1.append(ph[i])
       espvie1.append(espe_vie[i])
plt.scatter(espvie1, Ph1)
plt.xlabel("Esperance de vie")
plt.ylabel("Nb de personnes par médecin")
#plt.title("Correlation entre espe_vie et tv sans valeurs extremes")
plt.grid()
plt.show()
plt.scatter(espvie1, np.log10(Ph1))
plt.xlabel("Esperance de vie")
plt.ylabel("log(ph)")
#plt.title("log(ph) en fonction de espe_vie")
plt.grid()
plt.show()