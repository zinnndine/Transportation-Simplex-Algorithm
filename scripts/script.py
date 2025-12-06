import copy

def qmini(cout,A,base):
    s =1000000
    k=-1
    h=-1
    for i in range(len(cout)):
        for j in range (len(cout[i])):
            if  cout[i][j] < s and [i,j] not in base:
                s=cout[i][j]
                k=i
                h=j
    return k,h

def test_opt(A,C,n,m,la_base):   
    u=[None for i in range(n)]
    v=[None for j in range(m)]
    u[0]=0
    while(None in (u and v)):
        for i in range(0,n):
            for j in range(0,m):
                if ([i,j] in la_base) and u[i]!=None and v[j]==None:
                        v[j]=C[i][j]-u[i]
        for i in range(0,n):
            for j in range(0,m): 
                if ([i,j] in la_base) and v[j]!=None and u[i]==None:      
                        u[i]=C[i][j]-v[j]
    
    for i in range(0,n):
        for j in range(0,m):
            if A[i][j]==0 and [i,j] not in la_base:
                if C[i][j]-u[i]-v[j] < 0 :
                        return False
    return True


def court_nord(C,n,m,offre,demande):
    A=[[ 0 for i in range(m)]  for j in range(n)]
    dans_base = []
    i=0
    j=0
    offre_copie = offre.copy()
    demande_copie = demande.copy()
    
    while sum(offre_copie) > 0 and sum(demande_copie) > 0 and i < n and j < m:
        A[i][j] = min(offre_copie[i], demande_copie[j])
        dans_base.append([i,j])
        if (A[i][j] == offre_copie[i] and A[i][j] == demande_copie[j] and 
            demande_copie[j] > 0 and offre_copie[i] > 0 and len(dans_base) < n+m-1):
            k, h = qmini(C, A,dans_base)
            if k >= 0 and h >= 0:
                A[k][h] = 0
                dans_base.append([k,h])
            offre_copie[i] = 0
            demande_copie[j] = 0
            i = i + 1
            j = j + 1
        elif A[i][j] == offre_copie[i] and offre_copie[i] > 0:
            demande_copie[j] = demande_copie[j] - A[i][j]
            offre_copie[i] = 0
            i = i + 1
        elif A[i][j] == demande_copie[j] and demande_copie[j] > 0:
            offre_copie[i] = offre_copie[i] - A[i][j]
            demande_copie[j] = 0
            j = j + 1 
    return A, dans_base


def moind_cout(C,m,n,offre,demande):
    A = [[0] * m for _ in range(n)]
    dans_base = []
    c_copy = copy.deepcopy(C)
    offre_copie = offre.copy()
    demande_copie = demande.copy()
    while(sum(demande_copie)>0):
        k,h=qmini(c_copy,A,dans_base)
        if(demande_copie[h]>0 and offre_copie[k]>0 ):
            A[k][h]=min(offre_copie[k],demande_copie[h])
            dans_base.append([k,h])
            a=0
            b= 0
            if (offre_copie[k]==demande_copie[h] and len(dans_base)<n+m-1):
                a,b=qmini(C,A,dans_base)
                dans_base.append([a,b])
            demande_copie[h] = demande_copie[h] - A[k][h]
            offre_copie[k] = offre_copie[k] - A[k][h]
        else:
            c_copy[k][h]= 1000000
    return A ,dans_base


def new_entry(A,C,n,m,base):
    u=[None for i in range(n)]
    v=[None for j in range(m)]
    u[0]=0
    while(None in (u and v)):
        for i in range(0,n):
            for j in range(0,m):
                if ([i,j] in base) and u[i]!=None and v[j]==None:
                        v[j]=C[i][j]-u[i]
        for i in range(0,n):
            for j in range(0,m): 
                if ([i,j] in base) and v[j]!=None and u[i]==None:      
                        u[i]=C[i][j]-v[j]
    new_val = 10000
    k=-1
    h =-1
    for i in range(0,n):
        for j in range(0,m):
            if A[i][j]==0 and [i,j] not in base:
                if C[i][j]-u[i]-v[j] < new_val :
                     new_val = C[i][j]-u[i]-v[j]
                     k=i
                     h=j
    return k , h


def ver_search(k,h,A,tb,base,cy,m):
    tab = [x[0] for x in tb]
    for j in range(m):
        if ([k,j] in base and [k,j] not in tab) or (len(cy) > 2 and [k,j]==tab[0]) :
            return j
    return "no_sol"

def hor_search(k,h,A,tb,base,cy,n):
    tab = [x[0] for x in tb]
    for i in range(n):
        if ([i,h] in base and [i,h] not in tab) or (len(cy) > 2 and [i,h]==tab[0]) :
            return i
    return "no_sol"

def pop_element(cycle,tabau):
    if len(cycle) < 1:
        return cycle
    else : 
        cycle.pop(-1)
        return cycle


def delta(k:int, h:int, A:list[list[int]], n:int, m:int, offre:list[int], demande:list[int], base:list[list[int]]):
    base.append([k,h])
    cycle = [[k,h]]
    tabau = []
    tabau.append([[k,h],0])
    posk = k
    posh = h
    next_element_is = "ver"
    while True:
        if next_element_is == "ver":
            b = ver_search(posk, posh, A, tabau, base, cycle, m)
            if b == "no_sol":
                cycle = pop_element(cycle, tabau)
                if len(cycle) == 0:
                    return None
                posk, posh = cycle[-1]
                next_element_is = "hor"
            else:
                next_element_is = "hor"
                posh = b
                cycle.append([posk, posh])
                tabau.append([[posk, posh], 0])
        
        if next_element_is == "hor":
            b = hor_search(posk, posh, A, tabau, base, cycle, n)
            if b == "no_sol":
                cycle = pop_element(cycle, tabau)
                if len(cycle) == 0:
                    return None
                posk, posh = cycle[-1]
                next_element_is = "ver"
            else:
                next_element_is = "ver"
                posk = b
                cycle.append([posk, posh])
                tabau.append([[posk, posh], 0])
        
        if cycle[-1] == [k, h] and len(cycle) > 1:
            return cycle


def out_o_base(k,h,cycle,A,base):
    u=-1
    v=-1
    mnin = 10000000
    n=0
    for vec in cycle:
        n=n+1
        if n%2==0:
            if A[vec[0]][vec[1]] < mnin and vec !=[k,h]:
                mnin = A[vec[0]][vec[1]]
                u = vec[0]
                v=vec[1]
    return  u ,v


def update_base(k,h,u,v,base):
    out=base.index([u,v])
    base.pop(out)
    base.append([k,h])
    return base

def adjust_matrix(cycle,A,u,v):
    delta_calc = A[u][v]
    A[cycle[0][0]][cycle[0][1]] = A[cycle[0][0]][cycle[0][1]] + delta_calc
    cycle.pop(0)
    cycle.pop(-1)
    n=0
    for vec in cycle:
        n=n+1
        if n%2==1:
            A[vec[0]][vec[1]] = A[vec[0]][vec[1]] - delta_calc 
        if n%2==0:
            A[vec[0]][vec[1]] = A[vec[0]][vec[1]] + delta_calc 
    return A

def algorithme_de_tronsport(C, n, m, offre, demande):
    ch = -1
    aff = []
    chosen = []
    while(ch != 1 and ch != 2):
        ch = int(input("Choose heuristic for initial solution (1=court_nord, 2=moind_cout): "))
        if ch == 1:
            aff, chosen = court_nord(C, n, m, offre, demande)
        elif ch == 2:
            aff, chosen = moind_cout(C, m, n, offre, demande)
    iteration = 0
    MAX_ITERATIONS = 50
    while(test_opt(aff, C, n, m, chosen) == False and iteration < MAX_ITERATIONS):
        iteration += 1
        if iteration >= MAX_ITERATIONS:
            break
        k, h = new_entry(aff, C, n, m, chosen)
        cycle = delta(k, h, aff, n, m, offre, demande, chosen.copy())
        if not cycle:
            break 
        u, v = out_o_base(k, h, cycle, aff, chosen)
        if u == -1 or v == -1:
            break
        chosen = update_base(k, h, u, v, chosen)
        aff = adjust_matrix(cycle, aff, u, v)
    return aff, chosen

def calculate_total_cost(aff, C):
    total = 0
    n = len(aff)
    m = len(aff[0]) if n > 0 else 0
    for i in range(n):
        for j in range(m):
            total += aff[i][j] * C[i][j]
    return total

def cost_matrix(C, m, n, integer):
    if integer == 0:
        print(f"  [cost_matrix] Adding dummy row with {m} zeros")
        C.append([0 for i in range(m)])
        print(f"  New matrix dimensions: {len(C)}x{len(C[0])}")
    elif integer == 1:
        print(f"  [cost_matrix] Adding dummy column with {n} zeros")
        for i in range(len(C)): 
            C[i].append(0)
        print(f"  New matrix dimensions: {len(C)}x{len(C[0])}")
    return C

def equalization(C, offre, demande, n, m):
    C_copy = [row[:] for row in C] 
    offre_copy = offre[:]
    demande_copy = demande[:]
    n_copy = n
    m_copy = m
    
    total_supply = sum(offre_copy)
    total_demand = sum(demande_copy)
    
    if total_supply == total_demand:
        print(f"  Problem is already balanced")
        return C_copy, offre_copy, m_copy, n_copy, demande_copy
    
    elif total_supply < total_demand:
        # Need to add dummy supplier
        plus = total_demand - total_supply
        print(f"  Adding dummy supplier with supply {plus}")
        offre_copy.append(plus)
        n_copy = n_copy + 1
        C_copy = cost_matrix(C_copy, m_copy, n_copy, 0)  # Add dummy row
        
    elif total_supply > total_demand:
        # Need to add dummy consumer
        plus = total_supply - total_demand
        print(f"  Adding dummy consumer with demand {plus}")
        demande_copy.append(plus)
        m_copy = m_copy + 1
        C_copy = cost_matrix(C_copy, m_copy, n_copy, 1)  # Add dummy column
    
    print(f"  After equalization: n={n_copy}, m={m_copy}")
    print(f"  New supply: {offre_copy} (sum={sum(offre_copy)})")
    print(f"  New demand: {demande_copy} (sum={sum(demande_copy)})")
    print(f"  New matrix dimensions: {len(C_copy)}x{len(C_copy[0])}")
    
    return C_copy, offre_copy, m_copy, n_copy, demande_copy

def filling_data():
    print("\n[Filling data]")
    n = int(input("n (number of suppliers): "))
    m = int(input("m (number of consumers): "))
    print(f"\nEnter supply values for {n} suppliers:")
    offre = []
    for i in range(n):
        val = int(input(f"  Supply for offre {i}: "))
        offre.append(val)
    print(f"\nEnter demand values for {m} consumers:")
    demande = []
    for i in range(m):
        val = int(input(f"  Demand for clinet {i}: "))
        demande.append(val)
    
    # Get cost matrix
    print(f"\nEnter cost matrix ({n} rows x {m} columns):")
    A = []
    for i in range(n):
        row = []
        print(f"  Row {i} costs:")
        for j in range(m):
            val = int(input(f"    Cost from offre {i} to clinet {j}: "))
            row.append(val)
        A.append(row)
    
    print(f"\nData collected:")
    print(f"  n={n}, m={m}")
    print(f"  offre: {offre} (total={sum(offre)})")
    print(f"  Demand: {demande} (total={sum(demande)})")
    print(f"  Cost matrix dimensions: {len(A)}x{len(A[0])}")
    
    return A, n, m, offre, demande


if __name__ == "__main__":
    n = 3 
    m = 4  

    C1 = [
        [2, 3, 11, 7],  
        [1, 0, 6, 1],  
        [5, 8, 15, 9]  
    ]

    offre1 = [5, 10, 15]

    demande1 = [7, 8, 6, 9]


    C2 = [
    [-10, -6, -6, -4],
    [2, -6, -7, -6]
    ]
    offre2 = [2500, 2100]  
    demande2 = [1800, 2300, 550, 1750]  
    nn = 2  
    mm = 4  


    print(f"Cost matrix for Ex-1: {C1}")
    print(f"Supply for Ex-1: {offre1}")
    print(f"Demand for Ex-1: {demande1}")
    print("\n-----------------------------\n")
    print(f"Cost matrix for Ex-2: {C2}")
    print(f"Supply for Ex-2: {offre2}")
    print(f"Demand for Ex-2: {demande2}")
    x =int(input("choose between EXample-1 and EXample-2 (1 for Ex-1 , 2 for Ex-2) or press 0 if you want to manually fill:"))
    if x==1:
            C1,offre1,m,n,demande1=equalization(C1,offre1,demande1,n,m)
            result1 = algorithme_de_tronsport(C1, n, m, offre1, demande1)
            print(f"result1: {result1}")

    elif x==2:
            C2,offre2,mm,nn,demande2=equalization(C2,offre2,demande2,nn,mm)
            result1 = algorithme_de_tronsport(C2, nn, mm, offre2, demande2)
            print(f"result1: {result1}")
    elif x==0:
            C2,mm,nn,offre2,demande2=filling_data()
            print(f"Cost matrix for Ex: {C2}")
            print(f"Supply for Ex: {offre2}")
            print(f"Demand for Ex: {demande2}")
            C2,offre2,mm,nn,demande2=equalization(C2,offre2,demande2,nn,mm)
            result1 = algorithme_de_tronsport(C2, nn, mm, offre2, demande2)
            print(f"result1: {result1}")

    else:
        "!!!!wrong input re-do again and enter 1 or 2!!!!"