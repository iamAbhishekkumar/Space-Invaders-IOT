with open('scripts/image.pbm', 'rb') as f:
    f.readline()
    f.readline()  # Creator comment
    f.readline()  # Dimensions
    data = bytearray(f.read())
    print(data)
