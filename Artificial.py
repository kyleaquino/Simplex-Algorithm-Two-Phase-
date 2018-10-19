class ArtificialModule:

    def __init__(self, c, b, cons):
        self.c = c
        self.b = b
        self.cons = cons

    def parseTableu(self):
        c, b, cons = self.c, self.b, self.cons
        tableu, artificial = [],[]
        m, n = len(cons), len(c)
        sigma = [0.0]

        c.insert(0, 0.0)

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
        return tableu

    def phaseOne_Simplex(self,tableu):
        THETA_INFINITE = -1
        opt, unbounded = False, False
        n, m = len(tableu[0]), len(tableu) - 2

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
                continue

            tableu = self.pivotOn(tableu, pivotRow, pivotCol)
        return tableu, opt, unbounded

    def phaseTwo_Simplex(self, tableu):
        tableu, opt, unbounded = self.phaseOne_Simplex(tableu)

        infeasible  = False
        sigma = tableu[1][0]

        if (sigma > 0):
            infeasible  = True
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
            tableu, opt, unbounded = self.simplex(tableu)

        return tableu, infeasible, opt, unbounded

    def simplex(self, tableu):
        THETA_INFINITE = -1
        opt, unbounded = False, False
        n, m = len(tableu[0]), len(tableu) - 1

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
                continue
            tableu = pivotOn(tableu, pivotRow, pivotCol)
        return tableu, opt, unbounded

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
