import os, pandas

for filename in os.listdir('datasets'):
    print(filename)
    df = pandas.read_csv('datasets/{}'.format(filename))
    if df.empty:
        continue
    df = df.iloc[3:]
    df.to_csv(f'datasets/{filename}')