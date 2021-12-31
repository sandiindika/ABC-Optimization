
# Imported Module
import sys
import copy
import random
from math import *


random.seed(42)
INACTIVE_BEE = 0
EMPLOYEE_BEE = 1
ONLOOKER_BEE = 2


# Fuction and Class
def show_path(path, data_population): #fungsi untuk menampilkan path terbaik
    print(path)
    for i in range(len(path)):
        for dp in data_population:
            if dp.id == path[i]:
                print("%02d. %s (%s)" % (i, dp.name, dp.id))


def calc_fitness(path, data_population):
    d = 0.0  # variabel jarak sebelum kota
    for i in range(len(path)-1):
        for dp in data_population:
            if dp.id == path[i]:
                siteA = dp
            if dp.id == path[i+1]:
                siteB = dp
        d += siteA.jarak(siteB)
    return d

def calc_random_path(path):
    temp = path[1:]
    random.shuffle(temp)
    path = [path[0]] + temp
    return path

class Bee:
    def __init__(self, data_population): # Creating Bee Class
        self.status = INACTIVE_BEE  # 0 = inactive, 1 = active, 2 = scout
        self.limit = 0
        self.data_population = data_population
        self.population_size = len(self.data_population)
        self.path = [dp.id for dp in self.data_population]  # potensi solusi
        self.path = calc_random_path(self.path)
        self.fitness = calc_fitness(self.path, self.data_population)


class Wisata:
    def __init__(self, id, name, lat, long):
        self.id = id
        self.name = name
        self.lat  = lat
        self.long = long
    
    def jarak(self, Wisata):
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [self.long, self.lat, Wisata.long, Wisata.lat])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r


def run_bee_colony(start_population, data_population, colony_size, max_iter):
    # Langkah 2 - Fase inisial
    data_population = [start_population]+data_population
    population_size = len(data_population)
    solution = [Bee(data_population) for _ in range(colony_size)]

    best_fitness = sys.float_info.max  # mencari nilai max float dari sistem
    for i in range(colony_size):  # perulangan pengecekan random lebah
        if solution[i].fitness < best_fitness:
            best_fitness = solution[i].fitness
            best_path = copy.copy(solution[i].path)

    # memberikan inisialisasi status
    ketentuanAktif = int(colony_size * 0.50)
    ketentuanTetangga = int(colony_size * 0.25) #scout atau gerombolan
    ketentuanTidakAktif = colony_size - (ketentuanAktif + ketentuanTetangga)
    for i in range(colony_size):
        if i < ketentuanTidakAktif:
            solution[i].status = INACTIVE_BEE
        elif i < ketentuanTidakAktif + ketentuanTetangga:
            solution[i].status = ONLOOKER_BEE
        else:
            solution[i].status = EMPLOYEE_BEE
        
    # Langkah 3
    epoch = 0
    while epoch < max_iter:
        if best_fitness == 0.0: break
        for i in range(colony_size):  # proses setiap lebah
            if solution[i].status == EMPLOYEE_BEE:    # lebah aktif
                # Mencari jalur neighbor dan mencari keterkaitan masalah
                neighbor_path = copy.copy(solution[i].path)
                ri = random.randint(1, population_size-1)  # acak index
                ai = 1  # index yang berdekatan asumsikan terakhir->pertama
                if ri < population_size-1: ai = ri + 1
                neighbor_path[ri], neighbor_path[ai] = neighbor_path[ai], neighbor_path[ri]
                # print("EB:", neighbor_path)
                neighbor_fitness = calc_fitness(neighbor_path, data_population)

                # cek jika jalur neighbor lebih baik
                p = random.random()  # [0.0 to 1.0)
                if (neighbor_fitness < solution[i].fitness or
                (neighbor_fitness >= solution[i].fitness and p < 0.05)):
                    solution[i].path = neighbor_path
                    solution[i].fitness = neighbor_fitness

                    # new best? cek apakah ada yang baru terbaik
                    if solution[i].fitness < best_fitness:
                        best_fitness = solution[i].fitness
                        best_path = solution[i].path
                        print("EB: term = " + str(epoch) +
                        " jalur terbaik ditemukan ", end="")
                        print("dengan fitness = " + str(best_fitness))

            elif solution[i].status == ONLOOKER_BEE:  # kawanan lebah
                # Membuat jalur acak dan fitness
                random_path = [dp.id for dp in data_population]
                random_path = calc_random_path(random_path)
                # print("OB:", random_path)
                random_fitness = calc_fitness(random_path, data_population)
                # cek jika lebih baik
                if random_fitness < solution[i].fitness:
                    solution[i].path = random_path
                    solution[i].fitness = random_fitness
                    # cek jika terbaik
                    if solution[i].fitness < best_fitness:
                        best_fitness = solution[i].fitness
                        best_path = solution[i].path
                        print("OB: term = " + str(epoch) +
                        " jalur terbaik ditemukan ", end="")
                        print("dengan fitness = " + str(best_fitness))

            elif solution[i].status == INACTIVE_BEE:  # Tidak Aktif
                pass  # null statement

        # for-each bee
        
        epoch += 1
        # while
    
    print("\nJalur Terbaik Ditemukan:")
    show_path(best_path, data_population)
    print("\Total Jarak dari jalur terbaik = " + str(best_fitness))

def show_menu():
    print("Menu Program: ")
    print("1. Show Menu")
    print("2. Show Data Wisata")
    print("3. Run Bee Colony")
    print("9. Exit Program\n")


# Langkah 1 - Inisial Variabel
data_wisata     = [
    Wisata(0, "Alun-alun Kota Malang", -7.982591581835677, 112.63082170534167),
    Wisata(1, "Toko Oen", -7.980671378497223, 112.63033201050185),
    Wisata(2, "Mie Gajah Mada Malang", -7.985213899661343, 112.6315864920253),
    Wisata(3, "Bakso Presiden Malang", -7.96233073705116, 112.63711048423262),
    Wisata(4, "Inggil Museum Resto", -8.001735509661026, 112.72975628427514),
    Wisata(5, "Warung Ronde Titoni", -7.982246215774669, 112.63463533858751),
    Wisata(6, "Rumah Makan Cairo", -7.978191744955507, 112.6289725924316),
    Wisata(7, "Pecel Kawi", -7.975435617656789, 112.62005115539715),
    Wisata(8, "Sate Landak Bu Ria", -7.952168281433658, 112.68109023330793),
    Wisata(9, "Depot Hok Lay", -7.984491335134968, 112.63423403739756),
    Wisata(10, "Puthu Lanang Celaket", -7.966255362993997, 112.63362819772574),
]

m = '1'
while m in ['1', '2', '3']:
    if m == '1':
        show_menu()
    elif m == '2':
        print("Daftar Wisata:")
        for i, wisata in enumerate(data_wisata):
            print("%02d. %s" % (i, wisata.name))
        print()
        show_menu()
    elif m == '3':
        start_wisata = input("- Masukkan index start kunjungan wisata (default: 0): ")
        idx_wisata = list(map(int, input("- Masukkan index wisata (separate by comma): ").replace(' ', '').split(',')))
        data_wisata_sel = [data_wisata[i] for i in idx_wisata]
        colony_size = int(input("- Masukkan Colony Size (int): "))
        max_iter = int(input("- Masukkan jumlah maksimum Iterasi (int): "))
        try:
            start_wisata = data_wisata[int(start_wisata)]
        except:
            start_wisata = data_wisata[0]
        run_bee_colony(start_wisata, data_wisata_sel, colony_size, max_iter)
        print()
    m = input("Masukkan pilihan menu: ")
            

print("Program Bee Colony Exit Succesfully.")
