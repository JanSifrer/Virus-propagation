import random
import matplotlib.pyplot as plt

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    return [x,y]

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {"0": prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({"{}".format(i):koordinate})
    
    okuzena_tocka = random.randrange(n)
    for j in range(0,n):
        x = tocke["{}".format(j)][0]
        y = tocke["{}".format(j)][1]
        if j == okuzena_tocka:
            plt.plot(x, y, 'o', color="red")
        else:
            plt.plot(x, y, 'o', color="black")
    return plt.show()

a = koordinate_tocke()
b = generiraj_n_tock(200)
b


