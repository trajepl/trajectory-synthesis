import matplotlib.pyplot as plt
import numpy as np

def fig(l,name):
    n = 20
    X = np.arange(n)
    # Y = [0.54, 0.12,0.20,0.05,0.04,0.02,0.01,0.02,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(l)):
        Y.append(float(l[i]))
    
    plt.bar(X, Y, facecolor='#332E7F', edgecolor='white')

    plt.ylabel("Proportion")
    plt.xlabel(name)
    plt.xticks((5,10,15,20), ('5', '10','15','20'))

    plt.savefig('../result/' + name + '.png', dpi=100)
    plt.close()


if __name__ == "__main__":
	fig(1, 'acceleration')