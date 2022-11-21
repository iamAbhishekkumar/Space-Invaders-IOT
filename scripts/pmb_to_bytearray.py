with open('image.pbm', 'rb') as f:
    print(f.readline())  # Magic number
    # f.readline()  # Creator comment
    # f.readline()  # Dimensions
    data = bytearray(f.read())
    print(data)
