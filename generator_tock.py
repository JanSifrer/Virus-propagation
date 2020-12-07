import random
import matplotlib.pyplot as plt
import numpy as np
import csv
import os.path
import io, urllib, base64

### Najprej uvozimo potrebne pakete.
### Definiramo funckijo, ki nam nakljucno določi koordinate točk, 
### ter hkrati se zabeleži, da točka ni ne aktivno okužena, in da še ni 
### prebolela virusa.

def koordinate_tocke():
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    koliko_dni_se_kuzna = 0
    ze_prebolela = 0
    return [x,y,koliko_dni_se_kuzna, ze_prebolela]

### Definiramo funckijo, ki nam zgenerira n tock.

def generiraj_n_tock(n):
    prva_tocka = koordinate_tocke()
    tocke = {0: prva_tocka}
    for i in range(1,n):
        koordinate = koordinate_tocke()
        tocke.update({i:koordinate})
    return tocke

### Definiramo funkcijo, ki nam ustvari slovar sosedov, 
### pogledamo najprej ali je kandidat sosed od neke določene okužene točke,
### če je, dodamo to točko v seznam sosedov od kandidata.

def ali_je_sosed(kandidat, tocka, tocke, radij, dict_sosedov):
    x_tocke, y_tocke = tocke[tocka][0:2]
    x_kandidat, y_kandidat = tocke[kandidat][0:2]
    if (x_kandidat-x_tocke)**2 + (y_kandidat-y_tocke)**2 < radij**2:
        if tocka in dict_sosedov[kandidat]:
            pass
        else:
            dict_sosedov[kandidat] += [tocka]
    return dict_sosedov

### Definiramo funckijo, ki nam shrani slike, da jih potem lahko narišemo
### v datoteki zacetna.html.
def za_risanje_tock(n,tocke, dict_sosedov, korak_slike, ze_poznane_slike):
    ### Najprej pobrišemo vse slike, ki jih je do sedaj že narisal (to prav pride, 
    ### če program večkrat zaženemo).
    plt.clf()
    for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
        ### Če je točka že prebolela virus jo pobarvamo z modro.
        if ze_prebolela == 1:
            plt.plot(x, y, 'o', color="blue")
        else:
            ### Okužene pobarvamo z rdečo.
            if koliko_dni_se_kuzna > 0:
                plt.plot(x, y, 'o', color="red")
            else:
                ### Sosede pobarvamo zeleno.
                if len(dict_sosedov[k]) > 0:
                    plt.plot(x, y, 'o', color="green")
                ### Če točka ni ne prebolela okužbe, ni ne aktivno okuzena, 
                ### in ni ne sosed kake okužene, jo pobarvamo s črno.
                else:
                    plt.plot(x, y, 'o', color="black")
    ### Dodamo še naslov slike.
    plt.suptitle("slika na {} koraku".format(korak_slike))
    korak_slike = io.BytesIO()
    plt.savefig(korak_slike, format="png")
    korak_slike.seek(0)
    string = base64.b64encode(korak_slike.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    ### Slovar poznanih slik posodobimo z novo sliko.
    ze_poznane_slike.update({korak_slike:uri})
    return ze_poznane_slike

def narisi_m_okuzenih_tock(n, m, tocke, T, radij):
    ### Najprej definiramo slovar sosedov, in zapišem, da nobena točka ni sosed od kere okužene.
    dict_sosedov = {}
    for i in range(0,n):
        dict_sosedov.update({i:[]})
    for i in range(0,m):
        ### Izberemo neko naključno okuženo točko, in nastavimo da bo kužna še T dni.
        okuzena_tocka = random.randrange(n)
        tocke[okuzena_tocka][2] = T
        for j in range(0,n):
            ### Za vse točke preverimo, ali so sosedi okužene točke.
            dict_sosedov = ali_je_sosed(j, okuzena_tocka, tocke, radij, dict_sosedov)
    ### Narišemo oziroma shranimo prvo stanje - ena točka bo rdeča, nekaj jih bo zelenih, ostale bodo črne.
    ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, 1, {})
    return tocke, dict_sosedov, ze_poznane_slike

### Sedaj pa definirajmo še glavno funckijo, ki bo združevala vse prejšnje, in nam bo omogočala zagon same simulacije.
### Kot vhodne podatke moramo vnesti na koliko točkah želimo simulacijo, koliko želimo imeti na začetku okuženih,
### kakšna je verjetnost prenosa okužbe, koliko dni je točka lahko kužna, maksimalno število korakov simulacije,
### na kakšni razdalji so sosedi od okužene točke, na koliko korakov želimo videti stanje, in ali sploh želimo videti stanje oz. sliko.
def okuzi_sosede(n, koliko_zacetnih_okuzenih, verjetnost, T, max_st_ponovitev, radij, koraki_do_slike, ali_risem_slike):
    tocke = generiraj_n_tock(n)
    tocke, dict_sosedov, ze_poznane_slike = narisi_m_okuzenih_tock(n, koliko_zacetnih_okuzenih, tocke, T, radij)
    koraki = 0
    while max_st_ponovitev > 0:
        max_st_ponovitev -= 1
        koraki += 1
        ### Gremo po vseh točkah iz slovarja in preberemo vse njihove podatke.
        for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
            ### Če je točka že prebolela virus, ne naredimo ničesar.
            if ze_prebolela < 1:
                ### Če je točka že okužena, ne naredimo ničesar.
                if koliko_dni_se_kuzna < 1:
                    ### Najprej preverimo, če je soseda od kaksne okužene točke, in če je, od koliko točk je soseda.
                    kolikokart_sosed = len(dict_sosedov[k])
                    if kolikokart_sosed > 0:
                        ### Toliko kolikor ima okuženih sosedov, tolikokrat je lahko z določeno verjetnostjo okužena.
                        ali_se_okuzi = np.random.binomial(size=kolikokart_sosed, n=1, p=verjetnost)
                        ali_se_okuzi = max(ali_se_okuzi)
                        if ali_se_okuzi > 0:
                            ### Če se okuži, nastavimo čas kužnosti na T+1 (T je cas kužnosti, +1 pa nam v naslednji dveh 
                            ### for zankah omogoča, da popravim sosede od nje...).
                            tocke[k][2] = T+1
        ### Definirajmo še dve spremenljivki, ki nam bosta šteli koliko je aktivno okuženih, in koliko je virus že prebolelo.
        stevilo_trenutno_bolnih = 0
        preboleli = 0
        for k, (x, y, koliko_dni_se_kuzna, ze_prebolela) in tocke.items():
            ### Z naslednjima dvema if stavkama samo poskrbimo, da obravnavamo samo točke, ki še niso prebolele virusa, in ki so okužene.
            if ze_prebolela < 1:
                if koliko_dni_se_kuzna > 0:
                    for j in range(0,n):
                        if koliko_dni_se_kuzna > 1:
                            ### Če bo točka okužena še več kakor 1 dan, potem za vse druge točke pogledam,
                            ### če je katera soseda od te okužene točke.
                            dict_sosedov = ali_je_sosed(j, k, tocke, radij, dict_sosedov)
                        if koliko_dni_se_kuzna == 1:
                            ### Če je to zadnji dan, ko je točka še kužna, popravimo seznam sosedov,
                            ### kajti ta tocka (j) ne bo vec soseda od okužene točke (k).
                            try:
                                dict_sosedov[j].remove(k)
                            except:
                                pass
                    ### Če je točka kužna samo še en dan, še nastavimo, da je prebolela virus.
                    if koliko_dni_se_kuzna == 1:
                        tocke[k][3] = 1
                    ### Na koncu še popravimo, koliko dni bo še kužna.
                    tocke[k][2] -= 1
                ### stevilo_trenutno_bolnih nam šteje število okuženih točk.
                if koliko_dni_se_kuzna > 1:
                    stevilo_trenutno_bolnih +=1
                ### Preboleli nam šteje koliko točk je virus prebolelo.
                if koliko_dni_se_kuzna == 1:
                    preboleli += 1
            else:
                preboleli += 1
        ### Narišemo oziroma si shranimo stanje ampak samo če je ali_risem_slike = True.
        if ali_risem_slike:
            ### Za sledenje kje je program, še nastavimo da na določenih korakih izpisuje razmere - koliko je trenutno okuženih in koliko
            ### točk je virus prebolelo.
            if koraki % koraki_do_slike == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)

            if koraki % 10 == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))

            ### Še robna primera, če so vse točke okužene, ali pa če ni nobena več, se program ustavi.
            if (stevilo_trenutno_bolnih)/n == 1:
                print("stevilo okuzenih pri {0} koraku je: {1}".format(koraki, stevilo_trenutno_bolnih))
                print("Delez okuzenih je: {}".format(stevilo_trenutno_bolnih/n))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)
                return(ze_poznane_slike)

            if (stevilo_trenutno_bolnih)/n == 0:
                print("stevilo okuzenih pri {0} koraku je: {1}, zdravih pa {2}".format(koraki, stevilo_trenutno_bolnih, preboleli))
                ze_poznane_slike = za_risanje_tock(n, tocke, dict_sosedov, koraki, ze_poznane_slike)
                return(ze_poznane_slike)
       ### Če ne želimo da riše slike, nadaljujemo samo z robnima primeroma (uporabno če animacijo velikokrat poženemo, 
       ### tako kot npr. v funckiji generiraj()).
        if (stevilo_trenutno_bolnih)/n == 1:
            return (stevilo_trenutno_bolnih, preboleli, koraki)
        if (stevilo_trenutno_bolnih)/n == 0:
            return (stevilo_trenutno_bolnih, preboleli, koraki)
    return (stevilo_trenutno_bolnih, preboleli, koraki)
            
### Definirajmo še funckijo, ki nam bo zgenerirala podatke.
def generiraj():
    ### Začnemo z verjetnostjo okužbe 0.02 in radijam 0.02.
    verjetnost = 0.02
    radij = 0.02
    datoteka = "generirani_podatki2.csv"
    ### V .csv datoteko zapišemo glavo.
    with open(datoteka, 'a', newline='') as data:
        writer = csv.DictWriter(data, fieldnames =["Verjetnost", "Radij", "Okuženi", "Preboleli", "Koraki"])
        writer.writeheader()
    ### Sprehodimo se čez vse kombinacije radijev 0.02, 0.04 in 0.06 ter verjetnosti 0.02, 0.04, 0.06, 0.08 in 0.1 in
    ### za vsako kombinacijo 100 krat poženemo simulacijo.
    for j in range(0,3):
        radij = 0.02 + j*0.02
        for h in range(0, 5):
            verjetnost = 0.02 + h*0.02
            for i in range(0,100):
                steviloo, preboleli, koraki = okuzi_sosede(2000, 1, verjetnost, 14, 1000, radij,1, False)
                ### Na vsakem koraku še izpišemo podatke, da je čakanje malo bolj prijetno :).
                print(i, radij, verjetnost, steviloo, preboleli, koraki)
                ### Nato pa podatke še zapišemo v .csv datoteko.
                with open(datoteka, 'a', newline='') as data:
                    writer = csv.DictWriter(data, fieldnames =["Verjetnost", "Radij", "Okuženi", "Preboleli", "Koraki"])
                    writer.writerow({"Verjetnost":"{0}".format(verjetnost), "Radij":"{0}".format(radij), "Okuženi": "{0}".format(steviloo), "Preboleli": "{0}".format(preboleli), "Koraki": "{0}".format(koraki)})
