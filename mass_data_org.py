import csv
with open('mass_nist.txt') as mass_file:
    lines = mass_file.readlines()
    isotopes = {}
    for line in lines:
        if ('Atomic Number' in line) == True:
            c = -1
            while line[c] != ' ':
                c -= 1
            an = int(line[c+1:-1])
        elif ('Atomic Symbol' in line) == True:
            c = -1
            while line[c] != ' ':
                c -= 1
            asym = line[c+1:-1]
        elif ('Mass Number' in line) == True:
            c = -1
            while line[c] != ' ':
                c -= 1
            mn = int(line[c+1:-1])
        elif ('Relative Atomic Mass' in line) == True:
            c = -1
            while line[c] != ' ':
                c -= 1
            rel_full = line[c + 1:-1]
            n = 0
            while rel_full[n] != '(':
                n += 1
            mass = float(rel_full[:n])
            key = asym + str(mn)
            isotopes[key] = {}
            isotopes[key]['Atomic Mass'] = mass
            an = 0
            asym = 0
            mn = 0
            mass = 0

with open('isotopes.csv','w',newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for isotope in isotopes:
        atomic_mass = isotopes[isotope]['Atomic Mass']
        writer.writerow([isotope,atomic_mass])