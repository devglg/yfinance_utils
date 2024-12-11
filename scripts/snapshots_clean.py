import os

for filename in os.listdir('datasets'):
    print(filename)
    if os.path.isfile(filename) or os.path.islink(filename):
        os.unlink(filename)