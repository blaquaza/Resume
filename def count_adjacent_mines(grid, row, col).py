def count_adjacent_mines(grid, row, col):
    """
    Count the number of adjacent mines (#) to a given cell (row, col) in the grid.
    """
    rows = len(grid)
    cols = len(grid[0])
    mine_count = 0

    # Define the 8 possible directions (NW, N, NE, W, E, SW, S, SE)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
        (0, -1),         (0, 1),    # W,     E
        (1, -1), (1, 0), (1, 1)     # SW, S, SE
    ]

    # Check all adjacent cells
    for dr, dc in directions:
        adj_row, adj_col = row + dr, col + dc
        if 0 <= adj_row < rows and 0 <= adj_col < cols and grid[adj_row][adj_col] == "#":
            mine_count += 1

    return mine_count


def minesweeper(grid):
    """
    Transform the grid by replacing free spots (-) with the number of adjacent mines.
    """
    # Iterate over each cell in the grid
    rows = len(grid)
    cols = len(grid[0])

    # Create a new grid for the output
    output_grid = [[None for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "#":
                # Leave mines (#) as they are
                output_grid[row][col] = "#"
            else:
                # Replace free spots (-) with the count of adjacent mines
                output_grid[row][col] = str(count_adjacent_mines(grid, row, col))

    return output_grid


# Example usage
input_grid = [
    ["-", "-", "-", "#", "#"],
    ["-", "#", "-", "-", "-"],
    ["-", "-", "#", "-", "-"],
    ["-", "#", "#", "-", "-"],
    ["-", "-", "-", "-", "-"]
]

output_grid = minesweeper(input_grid)

# Print the output grid
for row in output_grid:
    print(" ".join(row))