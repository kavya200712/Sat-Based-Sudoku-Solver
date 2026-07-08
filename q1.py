"""
sudoku_solver.py

Implement the function `solve_sudoku(grid: List[List[int]]) -> List[List[int]]` using a SAT solver from PySAT.
"""

from pysat.formula import CNF
from pysat.solvers import Solver
from typing import List

def solve_sudoku(grid: List[List[int]]) -> List[List[int]]:
    """Solves a Sudoku puzzle using a SAT solver. Input is a 2D grid with 0s for blanks."""

    # TODO: implement encoding and solving using PySAT
    n=9
    block_n=3
    # for unique representation of proposition p(i,j,k) as a 3 digit number ijk
    def p(i,j,k):
        return 100*i+10*j+k
    
    cnf=CNF()
    
    #adding initial clues
    for i in range(1,n+1):
        for j in range(1,n+1):
            k=grid[i-1][j-1]
            if k!=0:
                cnf.append([p(i,j,k)])

    # each cell(i,j) is not empty
    for i in range(1,n+1):
        for j in range(1,n+1):
            cnf.append([p(i,j,k) for k in range(1,n+1)])
            
    # each cell(i,j) has atmost one number
    for i in range(1,n+1):
        for j in range(1,n+1):
            for k1 in range(1,n+1):
                for k2 in range(k1+1,n+1):
                    cnf.append([-p(i,j,k1),-p(i,j,k2)])
                    
    #each digit appears atleast once in a row
    for i in range(1,n+1):
        for k in range(1,n+1):
            cnf.append([p(i,j,k) for j in range(1,n+1)])
    
    #each digit appears atleast once in a column
    for k in range(1,n+1):
        for j in range(1,n+1):
            cnf.append([p(i,j,k) for i in range(1,n+1)])
    
    #each digit appears atmost once in a row
    for i in range(1,n+1):
        for k in range(1,n+1):
            for j1 in range(1,n+1):
                for j2 in range(j1+1,n+1):
                    cnf.append([-p(i,j1,k),-p(i,j2,k)])

    #each digit appears atleast once in a column                    
    for k in range(1,n+1):
        for j in range(1,n+1):
            for i1 in range(1,n+1):
                for i2 in range(i1+1,n+1):
                    cnf.append([-p(i1,j,k),-p(i2,j,k)])
                    
    #each digit appears atleast and atmost once in block(3*3)
    for blocki in range(1,block_n+1):
        for blockj in range(1,block_n+1):
            for k in range(1,n+1):
                block=[p(i,j,k) for i in range(((blocki-1)*block_n)+1,blocki*block_n+1) for j in range(((blockj-1)*block_n)+1,blockj*block_n+1) ]
                cnf.append(block)
                for b1 in range(len(block)):
                    for b2 in range(b1+1,len(block)):
                        cnf.append([-block[b1],-block[b2]])
                
    with Solver(name='glucose3') as solver:
        solver.append_formula(cnf.clauses)
        if solver.solve():
            model = solver.get_model()
            solution=[[0]*n for l in range(n)]
            for i in range(1,n+1):
                for j in range(1,n+1):
                    for k in range(1,n+1):
                        if p(i,j,k) in model:
                            solution[i-1][j-1]=k
            return solution
        else:
            raise ValueError("UNSAT")
# 