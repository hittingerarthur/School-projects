import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#Exercice 7

mu=360
s=np.sqrt(36)
y_val=np.linspace(mu-3*s,mu+3*s, 1000)
pdf_val=norm.pdf(y_val,mu,s)
plt.plot(y_val,pdf_val,label='Distribution normale')
#plt.title('Courbe de densité de probabilité de Y')
plt.xlabel('Nb de réussites (Y)')
plt.ylabel('Densité de probabilité')
plt.legend()
plt.show()

s=np.sqrt(6)
p_moins_ou_28=norm.cdf(28,mu,s)
p_plus_28=1-p_moins_ou_28
print('\n', 'La probabilité que la clinique rate plus de 28 opérations dans l année est :', p_plus_28)

quantile_99=norm.ppf(0.99,mu,s)
print('\n',"Le nombre d'opérations ratées au-delà duquel il y a 1% de chance est :", quantile_99)