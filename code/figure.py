import matplotlib.pyplot as plt
import numpy as np

def fig(l,name):
    n = 20
    X = np.arange(n)
    Y = []
    for i in range(len(l)):
        Y.append(float(l[i]))
    
    plt.bar(X, Y, facecolor='blue', edgecolor='white')

    plt.ylabel("Proportion")
    plt.xlabel(name)
    plt.xticks((5,10,15,20), ('50km', '100km','150km','200km'))

    plt.savefig('../result/' + name + '2.png', dpi=100)
    plt.close()
