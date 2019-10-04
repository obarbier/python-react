import pandas as pd
import matplotlib.pyplot as plt

plt.interactive(False)
import numpy as np


def graph(ax: object,  blood_pressure: object, inter_beat: object) -> object:
    out = ax.scatter(blood_pressure, inter_beat)
    z = np.polyfit(blood_pressure, inter_beat, 1)
    p = np.poly1d(z)
    plt.plot(blood_pressure, p(blood_pressure), "r--")
    plt.savefig('foo.pdf')
    return {'blood_pressure': [",".join([str(i) for i in blood_pressure])],
                         'inter_beat': [','.join([str(i) for i in inter_beat])],
                         'slope': [z[0]]}


if __name__ == '__main__':
    df = pd.read_csv("data.csv")
    df.columns = ['blood_pressure', 'inter_beat']
    current_blodd_pressure_max = df['blood_pressure'][0]
    current_inter_beat_max = df['inter_beat'][0]
    idx_tracker = []
    count: int = 1
    for index, row in df.iterrows():
        if (row[0] > current_blodd_pressure_max and row[1] > current_inter_beat_max):
            if count == 4:
                idx_tracker.append(index - 3)
            current_blodd_pressure_max = row[0]
            current_inter_beat_max = row[1]
        else:
            current_blodd_pressure_max = row[0]
            current_inter_beat_max = row[1]
            count = 1
        if count == 4:
            count = 1
        else:
            count = count + 1
    fig, (ax1) = plt.subplots(1, 1)
    summary = pd.DataFrame(columns=['blood_pressure', 'inter_beat','slope'])
    for idx in idx_tracker:
        summary.loc[len(summary)] = graph(ax1, df['blood_pressure'][idx:idx + 4], df['inter_beat'][idx:idx + 4])
    summary.to_csv("output.csv",sep=",")
