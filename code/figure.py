import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np

def fig(l,name):
    n = 20
    X = np.arange(n)
    Y = [0.67, 0.15,0.15,0.07,0.045,0.023,0.01,0.05,0.05,0,0,0,0,0,0,0,0,0,0,0] #length
    # Y = [0.1, 0.05, 0.14, 0.03, 0.11, 0.20, 0.15, 0.06, 0.04, 0.03, 0.03, 0.02, 0.01, 0.01, 0, 0, 0, 0, 0, 0]
    # for i in range(len(l)):
        # Y.append(float(l[i]))
    
    plt.bar(X, Y, facecolor='#332E7F', edgecolor='white')

    plt.ylabel("Proportion")
    plt.xlabel(name)
    plt.xticks((5,10,15,20), ('5', '10','15','20'))

    plt.savefig('../result/' + name + '-origin.png', dpi=100)
    plt.close()

def figDensity(lng, lat):
    for i in range(len(lng)):
        for j in range(len(lng[i])):
            pl.plot(lng[i][j], lat[i][j])
    pl.show()



if __name__ == "__main__":
	fig(1, 'Trajectory Acceleration')