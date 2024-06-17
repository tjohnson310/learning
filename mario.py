height = -1


while height <= 0 or type(height) != int or height > 8:
    try:
        height = int(input("Height: "))
    except ValueError:
        height = -1


num_of_levels = height

for i in range(height):
    this_i = i + 1
    level = num_of_levels - this_i
    spaces = level * " "
    hashes = this_i * "#"
    print(f"{spaces}{hashes}  {hashes}")
