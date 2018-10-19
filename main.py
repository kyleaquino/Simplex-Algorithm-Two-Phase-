from Artificial import ArtificialModule as am
import os

def main():
    c,b,cons = [],[],[]
    cons_no=int(input("Enter number of constraints: "))
    x_no=int(input("Enter number of x: "))

    for i in range (x_no):
        c_val=float(input("Enter Xr{}: ".format(i+1)))
        c.append(c_val)
    for i in range(cons_no):
        b_val=float(input("Enter b{}: ".format(i+1)))
        b.append(b_val)
    for i in range(cons_no):
        temp = []
        print("Constraint {}".format(i+1))
        for i in range(x_no):
            temp.append(float(input("Enter x{}: ".format(i+1))))
        cons.append(temp)

    clearScreen()

    artificialMod = am(c, b, cons)

    print('Original Tableu:')
    tableu = artificialMod.parseTableu()
    printTableu(tableu)

    print('Phase One Tableu:')
    tableu, opt, unbounded = artificialMod.phaseOne_Simplex(tableu)
    printTableu(tableu)

    print('Phase Two Tableu:')
    tableu, infeasible, opt, unbounded = artificialMod.phaseTwo_Simplex(tableu)
    printTableu(tableu)

    print("Is Optimal: ", opt)
    print("Is Infeasible: ", infeasible)
    print("Is Unbounded: ", unbounded)

    print ('Z(x*) = {}'.format( -tableu[0][0]))


def printTableu(tableu):
    print ('----------------------')
    for row in tableu:
        print (" ",row)
    print ('----------------------')
    return

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":main()
