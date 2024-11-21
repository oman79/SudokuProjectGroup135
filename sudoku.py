import sudoku_generator

if __name__ == "__main__":
    print("yo")
    b = sudoku_generator.generate_sudoku(9, 10)
    #temp board print
    for row in b:
        print(row)