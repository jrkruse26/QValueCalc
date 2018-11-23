# Calculates a reaction Q value given reactants and products
import csv

# open existing mass database
with open('isotopes.csv') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  isotopes = {row[0].lower() : float(row[1]) for row in reader}

# define Q value calculation function
def QCalc(reactants, products):
  reactant_mass = 0
  for a in reactants:
    reactant_mass += isotopes[a]
  product_mass = 0
  for a in products:
    product_mass += isotopes[a]
  reactant_e = reactant_mass*931.4941
  product_e = product_mass*931.4941
  Q = reactant_e - product_e
  return Q

print('Welcome to Jordan\'s Q Value Calculator!')
print()
# prompt for reactants, convert to lowercase, check that inputs exist in data base
print('Enter your reactants separated by a space')
reactant_input = input('Reactants: ')
print()
reactants = reactant_input.split(' ')
reactants = [a.lower() for a in reactants]
for a in reactants:
    if (a in isotopes) == False and a != 'n':
        print('WARNING: Isotope {0} not in database'.format(a))
        input('Press Enter to continue')
        print()

# prompt for products, convert to lowercase, check that inputs exist in data base
print('Enter your products separated by a space')
product_input = input('Products: ')
print()
products = product_input.split(' ')
products = [a.lower() for a in products]
for a in products:
    if (a in isotopes) == False and a != 'n':
        print('WARNING: Isotope {0} not in database'.format(a))
        input('Press Enter to continue')
        print()

# convert any n inputs to n1
for idx, a in enumerate(reactants):
    if a == 'n':
        reactants[idx] = 'n1'
for idx, a in enumerate(products):
    if a == 'n':
        products[idx] = 'n1'

# execute calculation, print value
Q = QCalc(reactants,products)
Q = round(Q,4)
print('Q value is {0} MeV'.format(Q))
print()
input('Press Enter to exit')
