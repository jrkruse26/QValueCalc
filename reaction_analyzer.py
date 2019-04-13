# Calculates a reaction Q value given reactants and products
import csv
import tkinter

window = tkinter.Tk()

# open existing mass database
with open('isotopes.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    isotopes = {row[0].lower(): [int(row[1]), int(row[2]), float(row[3])] for row in reader}
print('Welcome to Jordan\'s Nuclear Reaction Calculator!')
run = True
exceptions = ['n', 't', 'd']


# define Q value calculation function
def QCalc(reactants, products):
    reactant_mass = 0
    for a in reactants:
        a = str(a)
        reactant_mass += isotopes[a][2]
    product_mass = 0
    for a in products:
        product_mass += isotopes[a][2]
    reactant_e = reactant_mass * 931.4941
    product_e = product_mass * 931.4941
    Q = reactant_e - product_e
    return Q


# define min neutron KE function
# mc^2 must be >> Q
def KE_thresh(proj_mass, target_mass, Q):
    if Q >= 0:
        return 0
    else:
        thresh = -(1 + (proj_mass / target_mass)) * Q
        return thresh


# def Coulombic Threshold function
def CE_thresh(proj, targ):
    Z_targ = isotopes[targ][1]
    Z_proj = isotopes[proj][1]
    A_targ = isotopes[targ][0]
    A_proj = isotopes[proj][0]
    CE = 1.2 * ((Z_proj * Z_targ) / ((A_proj ** (1 / 3)) + (A_targ ** (1 / 3))))
    return CE


while run == True:
    restart = False
    # prompt for reactants, convert to lowercase, check that inputs exist in data base
    print()
    print('Enter each reactant, separated by a space [ex. O16 n]')
    reactant_input = input('Reactants: ')
    print()
    reactants = reactant_input.split(' ')
    reactants = [a.lower() for a in reactants]
    for a in reactants:
        if not (a in list(isotopes) or a in exceptions):
            restart = True
            print('WARNING: Isotope {0} not in database'.format(a))
            input('Press Enter to restart')
            print()
        elif a == '':
            reactants.remove(a)
    if restart:
        continue

    # prompt for products, convert to lowercase, check that inputs exist in data base
    print('Enter your products separated by a space')
    product_input = input('Products: ')
    print()
    products = product_input.split(' ')
    products = [a.lower() for a in products]
    for a in products:
        if not (a in list(isotopes) or a in exceptions):
            restart = True
            print('WARNING: Isotope {0} not in database'.format(a))
            input('Press Enter to restart')
            print()
        elif a == '':
            products.remove(a)
    if restart:
        continue

    str_reactants = ''
    for idx, a in enumerate(reactants):
        astr = ''
        for idy, c in enumerate(a):
            cstr = ''
            if idy == 0 and a != 'n' and a != 'n1':
                cstr = c.upper()
            else:
                cstr = c
            astr += cstr
        if idx == 0:
            str_reactants += astr
        else:
            str_reactants += ' + ' + astr

    str_products = ''
    for idx, a in enumerate(products):
        astr = ''
        for idy, c in enumerate(a):
            cstr = ''
            if idy == 0 and a != 'n' and a != 'n1':
                cstr = c.upper()
            else:
                cstr = c
            astr += cstr
        if idx == 0:
            str_products += astr
        else:
            str_products += ' + ' + astr

    string = '    ' + str_reactants + ' --> ' + str_products
    print(string)
    print()

    # convert any exceptions
    for idx, a in enumerate(reactants):
        if a == 'n':
            reactants[idx] = 'n1'
        elif a == 'd':
            reactants[idx] = 'h2'
        elif a == 't':
            reactants[idx] = 'h3'
    for idx, a in enumerate(products):
        if a == 'n':
            products[idx] = 'n1'
        elif a == 'd':
            products[idx] = 'h2'
        elif a == 't':
            products[idx] = 'h3'
    # execute calculation, print value
    Q = QCalc(reactants, products)
    Q = round(Q, 4)
    print('    Q value is {0} MeV'.format(Q))

    # Calculate threshold scenarios
    if len(reactants) == 2 and ('n1' in reactants) == True and Q < 0:
        mass_number = ''
        for a in reactants:
            if a != 'n1':
                mass_number = isotopes[a][0]
        KE = KE_thresh(1, mass_number, Q)
        KE = round(KE, 4)
        print('    Neutron Threshold Energy of {} MeV Required'.format(KE))
    elif len(reactants) == 2 and ('n1' in reactants) == True and Q > 0:
        print('    0 Threshold Energy')
    elif len(reactants) == 2 and Q < 0:
        if isotopes[reactants[0]][0] > isotopes[reactants[1]][0]:
            proj = reactants[1]
            targ = reactants[0]
        else:
            proj = reactants[0]
            targ = reactants[1]
        KE = KE_thresh(isotopes[proj][0], isotopes[targ][0], Q)
        KE = round(KE, 4)
        CE = CE_thresh(proj, targ)
        CE = round(CE, 4)
        TE = max(KE, CE)
        print('    Kinetic Threshold of {} MeV'.format(KE))
        print('    Coulombic Threshold of {} MeV'.format(CE))
        print('    Threshold of {} MeV Required'.format(TE))
    elif len(reactants) == 2 and Q > 0:
        if isotopes[reactants[0]][0] > isotopes[reactants[1]][0]:
            proj = reactants[1]
            targ = reactants[0]
        else:
            proj = reactants[0]
            targ = reactants[1]
        CE = CE_thresh(proj, targ)
        CE = round(CE, 4)
        print('    Coulombic Threshold of {} MeV'.format(CE))
    print()
    action = input('Enter \'n\' for new reaction, enter any other key to exit: ')
    if action != 'n':
        run = False
    else:
        print()
