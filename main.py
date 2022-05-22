import itertools
from tqdm import tqdm

# Usage of PYPY is preffered, as for n=5 the time taken without it is 3.5 hours
# Actually this script can work only for 2 <= n <= 5, with n=6 itertools fail to generate all of the permutations
n = 5

vertices = list(range(n))

edges = []
# Generate all edges
for i in vertices:
    for j in vertices:
        if i != j:
            edges.append((min(i, j), max(i, j)))

edges = set(edges)
perms = list(itertools.permutations(edges))

# Generate permutations with first edge fixed - to reduce amount of calculations
clean_perms = []
for p in perms:
    if (p[0] == (0, 1)):
        clean_perms.append(p)

print(f'available {len(clean_perms)}')

# Generate all possible moves of player B
def generate_B_moves(n):
    if n == 1:
        return [[0], [1]]
    return [x + [0] for x in generate_B_moves(n - 1)] + [x + [1] for x in generate_B_moves(n - 1)]

# Determine whether graph has a fully connected node
def has_complete_node(edges, n, e):
    counter = [0] * (e + 1)
    for edge in edges:
        counter[edge[0]] += 1
        counter[edge[1]] += 1
    
    for c in counter:
        if c == n - 1:
            return True
        if c >= n:
            assert False
    return False

B_CAN_WIN_GLOBALLY = True
B_moves = generate_B_moves(len(edges))
# For each permutation
for perm in tqdm(perms):
    B_CAN_WIN = False
    # Try all possible B moves
    for this_B_moves in B_moves:
        existing_edges = []
        A_WIN = False
        B_WIN = False
        # Apply the moves one by one
        for i in range(len(edges)):
            if this_B_moves[i] == 1:
                existing_edges.append(perm[i])
                # If at some point there is a complete node - determine who has won
                if has_complete_node(existing_edges, n, len(edges)):
                    if i != len(perm) - 1:
                        A_WIN = True
                        break
                    else:
                        B_WIN = True
                        break
        if not B_WIN:
            A_WIN = True
        # If B won it means that for this particular permutation there is a strategy which B can follow to win. Move to the next permutation
        if B_WIN:
            # print("B can win - move to the next permutation")
            B_CAN_WIN = True
            break

    # print("Next perm")

    # If B can't win for at least one of the permutation it means that A has a strategy (exactly this permutation) to win always
    if not B_CAN_WIN:
        print("B can't win")
        B_CAN_WIN_GLOBALLY = False
        break


if B_CAN_WIN_GLOBALLY:
    print("B has a strategy to win")
else:
    print("B has no strategy")