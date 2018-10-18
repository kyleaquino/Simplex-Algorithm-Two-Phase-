import sys

def printTableu(tableu):
 print ('----------------------')
 for row in tableu:
  print (" ",row)
 print ('----------------------')
 return


def pivotOn(tableu, row, col):
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


# assuming tablue in standard form with basis formed in last m columns
def phase_1_simplex(tableu):

 THETA_INFINITE = -1
 opt   = False
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
  tableu = pivotOn(tableu, pivotRow, pivotCol)

 return tableu

def simplex(tableu):

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

def drive_out_artificial_basis(tableu):
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

def two_phase_simpelx(tableu):
 infeasible  = False
 tableu = phase_1_simplex(tableu)
 sigma = tableu[1][0]
 if (sigma > 0):
  infeasible  = True
  print ('Tableu is infeasible')
 else:
  print ('Tableu is feasible')
  #sigma is equals to zero
  tableu = drive_out_artificial_basis(tableu)
  m = len(tableu) - 2
  n = len(tableu[0])
  n -= m
  tableu.pop(1)
  i = 0
  while (i < len(tableu)):
   tableu[i] = tableu[i][:n]
   i += 1
  tableu, opt, unbounded = simplex(tableu)
  print("Optimal is: ", opt)
  print("Unbounded is: ", unbounded)
 return tableu

def getTableu(c, cons, b):
 #assume b >= 0 so if there is any b[i] negative make sure to enter
 #it possitive by multiplying (-1 * eqs[i]) and (-1 * b[i]) for all i
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
 return tableu


#Input Output
c=[]
cons=[]
b=[]
cons_no=int(input("Enter number of constraints: "))
x_no=int(input("Enter number of x: "))
for i in range (x_no):
    c_val=float(input("Enter Xr{}: ".format(i+1)))
    c.append(c_val)
for i in range(cons_no):
    b_val=float(input("Enter b{}: ".format(i+1)))
    b.append(b_val)
temp=[]
for i in range(cons_no):
    print("Constraint {}".format(i+1))
    temp1 = []
    for i in range(x_no):
        temp1.append(float(input("Enter x{}: ".format(i+1))))
    temp.append(temp1)
tableu = getTableu(c, temp, b)
printTableu(tableu)
tableu = phase_1_simplex(tableu)
printTableu(tableu)
tableu = two_phase_simpelx(tableu)
printTableu(tableu)

print ('Z(x*) = {}'.format( -tableu[0][0]))
