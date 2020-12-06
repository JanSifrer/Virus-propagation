import random
import matplotlib.pyplot as plt
import numpy as np
import csv
import os.path
import io, urllib, base64

### Najprej uvozimo potrebne pakete
### Definiramo funckijo, ki nam nakljucno doloci koordinate tock

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    koliko_dni_se_kuzna = 0
    ze_prebolela = 0
    return [x,y,koliko_dni_se_kuzna, ze_prebolela]

### Definiramo funckijo, ki nam zgenerira n tock

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {0: prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({i:koordinate})
    return tocke

### Definiramo funkcijo, ki nam ustvari slovar sosedov, 
### pogledamo najprej ali je kandidat sosed od neke dolocene tocke,
### ce je, dodamo to tocko v seznam sosedov od kandidata.
def ali_je_sosed(kandidat, tocka, tocke, radij, dict_sosedov):
    x_tocke, y_tocke = tocke[tocka][0:2]
    x_kandidat, y_kandidat = tocke[kandidat][0:2]
    if (x_kandidat-x_tocke)**2 + (y_kandidat-y_tocke)**2 < radij**2:
        if tocka in dict_sosedov[kandidat]:
            pass
        else:
            dict_sosedov[kandidat] += [tocka]
    return dict_sosedov

### Dolocimo funckijo, ki nam narise tocke
def za_risanje_tock(n,tocke, dict_sosedov, korak_slike, ze_poznane_slike):
    plt.clf()
    for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
        if ze_prebolela == 1:
            plt.plot(x, y, 'o', color="blue")
        else:
            if koliko_dni_se_kuzna > 0:
                plt.plot(x, y, 'o', color="red")
            else:
                if len(dict_sosedov[k]) > 0:
                    plt.plot(x, y, 'o', color="green")
                else:
                    plt.plot(x, y, 'o', color="black")
    plt.suptitle("slika na {} koraku".format(korak_slike))
    korak_slike = io.BytesIO()
    plt.savefig(korak_slike, format="png")
    korak_slike.seek(0)
    string = base64.b64encode(korak_slike.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    ze_poznane_slike.update({korak_slike:uri})
    return ze_poznane_slike

def narisi_m_okuzenih_tock(n, m, tocke, T, radij):
    ### Najprej dediniram slovar sosedov, in zapisem, da nobena tocka ni sosed od kere okuzene
    dict_sosedov = {}
    for i in range(0,n):
        dict_sosedov.update({i:[]})
    for i in range(0,m):
        ### Izberem neko nakljucno okuzeno tocko, in nastavim da bo kuzna se T dni 
        okuzena_tocka = random.randrange(n)
        tocke[okuzena_tocka][2] = T
        for j in range(0,n):
            ### Za vse tocke preverim, ali so sosedi okuzene tocke
            dict_sosedov = ali_je_sosed(j, okuzena_tocka, tocke, radij, dict_sosedov)
    ### Narisem prvo stanje
    ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, 1, {})
    return tocke, dict_sosedov, ze_poznane_slike

def okuzi_sosede(n, koliko_zacetnih_okuzenih, verjetnost, T, max_st_ponovitev, radij, koraki_do_slike, ali_risem_slike):
    tocke = generiraj_n_tock(n)
    tocke, dict_sosedov, ze_poznane_slike = narisi_m_okuzenih_tock(n, koliko_zacetnih_okuzenih, tocke, T, radij)
    koraki = 0
    while max_st_ponovitev > 0:
        max_st_ponovitev -= 1
        koraki += 1
        for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
            if ze_prebolela < 1:
                if koliko_dni_se_kuzna < 1:
                    ### Najpprej preverimo, ce je sosed od kaksne okuzene tocke, in ce je, od koliko tock je sosed
                    kolikokart_sosed = len(dict_sosedov[k])
                    if kolikokart_sosed > 0:
                        ### Toliko kolikor ima okuzenih sosedov, tolikokrat je lahko z doloceno verjetnostjo okuzen
                        ali_se_okuzi = np.random.binomial(size=kolikokart_sosed, n=1, p=verjetnost)
                        ali_se_okuzi = max(ali_se_okuzi)
                        if ali_se_okuzi > 0:
                            ### Ce se okuzi, nastavimo cas kuznosti na T+1 (T je cas kuznosti, +1 pa mi v naslednji dveh 
                            ### for zankah omogoca, da popravim sosede od nje...)
                            tocke[k][2] = T+1
        stevilo_trenutno_bolnih = 0
        preboleli = 0
        for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
            if ze_prebolela < 1:
                ### Za vsako tocko pogledamo koliko dni bo se kuzna, ce ni kuzna, vrne 0
                if koliko_dni_se_kuzna > 0:
                    for j in range(0,n):
                        if koliko_dni_se_kuzna > 1:
                            ### Ce bo tocka okuzena se vec kakor 1 dan, potem za vse druge tocke pogledam,
                            ### ce je soseda od okuzene tocke
                            dict_sosedov = ali_je_sosed(j, k, tocke, radij, dict_sosedov)
                        if koliko_dni_se_kuzna == 1:
                            ### Če je to zadnji dan, ko je oseba se kuzna, popravimo seznam sosedov,
                            ### kajti ta tocka (j) ne bo vec soseda od okuzene tocke (k)
                            try:
                                dict_sosedov[j].remove(k)
                            except:
                                pass
                    if koliko_dni_se_kuzna == 1:
                        tocke[k][3] = 1

                    ### Na koncu se popravimo, koliko dni bo se kuzna.
                    tocke[k][2] -= 1
                ### stevilo_trenutno_bolnih nam šteje število okuženih točk
                if koliko_dni_se_kuzna > 1:
                    stevilo_trenutno_bolnih +=1
                ### Preboleli je število prebolelih
                if koliko_dni_se_kuzna == 1:
                    preboleli += 1
            else:
                preboleli += 1
        ### Narisemo stanje, samo če je ali_risem_slike = True
        if ali_risem_slike:
            if koraki % koraki_do_slike == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)

            if koraki % 10 == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))
        
            if (stevilo_trenutno_bolnih)/n == 1:
                print("stevilo okuzenih pri {0} koraku je: {1}".format(koraki, stevilo_trenutno_bolnih))
                print("Delez okuzenih je: {}".format(stevilo_trenutno_bolnih/n))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)
                return(ze_poznane_slike)

            if (stevilo_trenutno_bolnih)/n == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)
                return(ze_poznane_slike)
       ### Če ne želimo da riše slike, tukaj nadaljuje:
        if (stevilo_trenutno_bolnih)/n == 1:
            return (stevilo_trenutno_bolnih, preboleli, koraki)
        if (stevilo_trenutno_bolnih)/n == 0:
            return (stevilo_trenutno_bolnih, preboleli, koraki)
    return (stevilo_trenutno_bolnih, preboleli, koraki)
            
def generiraj():
    verjetnost = 0.02
    radij = 0.02
    datoteka = "generirani_podatki2.csv"
    with open(datoteka, 'a', newline='') as data:
        writer = csv.DictWriter(data, fieldnames =["Verjetnost", "Radij", "Okuženi", "Preboleli", "Koraki"])
        writer.writeheader()
    for j in range(0,4):
        radij = 0.02 + j*0.02
        for h in range(0, 5):
            verjetnost = 0.02 + h*0.02
            for i in range(0,100):
                steviloo, preboleli, koraki = okuzi_sosede(2000, 1, verjetnost, 14, 1000, radij,1, False)
                print(i, radij, verjetnost, steviloo, preboleli, koraki)
                with open(datoteka, 'a', newline='') as data:
                    writer = csv.DictWriter(data, fieldnames =["Verjetnost", "Radij", "Okuženi", "Preboleli", "Koraki"])
                    writer.writerow({"Verjetnost":"{0}".format(verjetnost), "Radij":"{0}".format(radij), "Okuženi": "{0}".format(steviloo), "Preboleli": "{0}".format(preboleli), "Koraki": "{0}".format(koraki)})







#tocke = generiraj_n_tock(2000)
#### TESTI
#a,b,c = narisi_m_okuzenih_tock(2000, 1, tocke, 10, 0.2)
#for i,v in c.items():
#    print(v)
#b = narisi_m_okuzenih_tock(200, 2, tocke, 10, 0.2)
#
#b = okuzi_sosede(2000, 1, 0.01, 14, 1000, 0.05, 2)
#countt = 0
#for i in b:
#    if b["{}".format(i)][3] == 0:
#        countt +=1
#        #print(i)
