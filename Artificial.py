class ArtificialModule:
    def __init__(self,c,cons,b):
        self.c = c;
        self.cons = cons;
        self.b = b;
        self.originaltableu = []
        self.phaseOnetableu = []
        self.phaseTwotableu = []
        self.opt = False
        self.unbounded = False
        self.infeasible = False

        self.parseTableu()
        self.phaseOne_Simplex()
        self.phaseTwo_Simplex()

    def getOriginalTableu(self):
        return self.originaltableu

    def getPhaseOneTableu(self):
        return self.phaseOnetableu

    def getPhaseTwoTableu(self):
        return self.phaseTwotableu

    def isUnbounded(self):
        return self.unbounded

    def isOptimal(self):
        return self.opt

    def isInfeasible(self):
        return self.infeasible

    def printTableu(self, tableu):
        print ('----------------------')
        for row in tableu:
            print (" ",row)
        print ('----------------------')
        return

    def parseTableu(self):

        c = self.c
        b = self.b
        cons = self.cons

        tableu = []
        m = len(cons)
        n = len(c)
        c.insert(0, 0.0)
        artificial = []
        sigma = [0.0]
        i = 0
        while (i < n):
            sigma.append(0.0)
            i += 1
        i = 0
        while (i < m):
            artificial.append(0.0)
            sigma.append(1.0)
            i += 1
        c.extend(artificial)
        tableu.append(c)
        tableu.append(sigma)
        i = 0
        for eq in cons:
            eq.insert(0, b[i])
            eq.extend(artificial)
            eq[n+1+i] = 1.0
            tableu.append(eq)
            i += 1
        i = 0
        for xi in tableu:
            if (i > 1):
                j = 0
                for xij in xi:
                    tableu[1][j] -= xij
                    j += 1
            i += 1
        self.originaltableu = tableu

    def phaseOne_Simplex(self):
        THETA_INFINITE = -1
        tableu = self.originaltableu
        opt = False
        unbounded  = False
        n = len(tableu[0])
        m = len(tableu) - 2

        while ((not opt) and (not unbounded)):
            min = 0.0
            pivotCol = j = 1
            while(j < (n-m)):
                cj = tableu[1][j]
                if (cj < min):
                    min = cj
                    pivotCol = j
                j += 1
            if min == 0.0:
                opt = True
                self.opt = True
                continue
            pivotRow = i = 0
            minTheta = THETA_INFINITE
            for xi in tableu:
                if (i > 1):
                    xij = xi[pivotCol]
                    if (xij) > 0:
                        theta = ((xi[0]) / (xij))
                        if (theta < minTheta) or (minTheta == THETA_INFINITE):
                            minTheta = theta
                            pivotRow = i
                i += 1
            if minTheta == THETA_INFINITE:
                unbounded = True
                self.unbounded = True
                continue

            tableu = self.pivotOn(tableu, pivotRow, pivotCol)

        self.phaseOnetableu = tableu

    def phaseTwo_Simplex(self):
        self.phaseOne_Simplex()

        tableu = self.phaseOnetableu
        infeasible  = False
        sigma = tableu[1][0]

        if (sigma > 0):
            infeasible  = True
            self.infeasible = True
        else:
            #sigma is equals to zero
            tableu = self.drive_out_artificial_basis(tableu)
            m = len(tableu) - 2
            n = len(tableu[0])
            n -= m
            tableu.pop(1)
            i = 0
            while (i < len(tableu)):
                tableu[i] = tableu[i][:n]
                i += 1
            tableu = self.simplex(tableu)

        self.phaseTwotableu = tableu

    def simplex(self, tableu):
        THETA_INFINITE = -1
        opt   = False
        unbounded  = False

        n = len(tableu[0])
        m = len(tableu) - 1

        while ((not opt) and (not unbounded)):
            min = 0.0
            pivotCol = j = 0
            while(j < (n-m)):
                cj = tableu[0][j]
                if (cj < min) and (j > 0):
                    min = cj
                    pivotCol = j
                j += 1
            if min == 0.0:
                opt = True
                self.opt = True
                continue
            pivotRow = i = 0
            minTheta = THETA_INFINITE
            for xi in tableu:
                if (i > 0):
                    xij = xi[pivotCol]
                    if xij > 0:
                        theta = (xi[0] / xij)
                        if (theta < minTheta) or (minTheta == THETA_INFINITE):
                            minTheta = theta
                            pivotRow = i
                i += 1
            if minTheta == THETA_INFINITE:
                unbounded = True
                self.unbounded = True
                continue
            tableu = pivotOn(tableu, pivotRow, pivotCol)
        return tableu

    def pivotOn(self, tableu, row, col):
        j = 0
        pivot = tableu[row][col]
        for x in tableu[row]:
            tableu[row][j] = (tableu[row][j]) / (pivot)
            j += 1
        i = 0
        for xi in tableu:
            if i != row:
                ratio = xi[col]
                j = 0
                for xij in xi:
                    xij -= ratio * tableu[row][j]
                    tableu[i][j] = xij
                    j += 1
            i += 1
        return tableu

    def drive_out_artificial_basis(self, tableu):
        n = len(tableu[0])
        j = n - 1
        isbasis = True
        while(j > 0):
            found = False
            i = -1
            row = 0
            for xi in tableu:
                i += 1
                if (xi[j] == 1):
                    if (found):
                        isbasis = False
                        continue
                    elif (i > 1):
                        row = i
                        found = True
                elif (xi[0] != 0):
                    isbasis = False
                    continue
            if (isbasis and found):
                if (j >= n):
                    tableu = pivotOn(tableu, row, j)
                else:
                    return tableu
            j -= 1
        return tableu
