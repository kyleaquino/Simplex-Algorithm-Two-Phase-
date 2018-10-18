from Artificial import ArtificialModule as am
import os

def main():
    c,b,cons,temp = [],[],[],[]

    cons_no=int(input("Enter number of constraints: "))
    x_no=int(input("Enter number of x: "))

    for i in range (x_no):
        c_val=float(input("Enter Xr{}: ".format(i+1)))
        c.append(c_val)
    for i in range(cons_no):
        b_val=float(input("Enter b{}: ".format(i+1)))
        b.append(b_val)
    for i in range(cons_no):
        temp1 = []
        print("Constraint {}".format(i+1))
        for i in range(x_no):
            temp1.append(float(input("Enter x{}: ".format(i+1))))
        temp.append(temp1)

    clearScreen()

    artificalMod = am(c, temp, b)
    originaltableu = artificalMod.getOriginalTableu()
    phaseOnetableu = artificalMod.getPhaseOneTableu()
    phaseTwotableu = artificalMod.getPhaseTwoTableu()

    print('Original Tableu:')
    artificalMod.printTableu(originaltableu)
    print('Phase One Tableu:')
    artificalMod.printTableu(phaseOnetableu)
    print('Phase Two Tableu:')
    artificalMod.printTableu(phaseTwotableu)

    print("Is Optimal:", artificalMod.isOptimal())
    print("Is Infeasible:", artificalMod.isInfeasible())
    print("Is Unbounded:", artificalMod.isUnbounded())

    print ('Z(x*) = {}'.format( -phaseTwotableu[0][0]))

    return None

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

if __name__ == "__main__":main()
