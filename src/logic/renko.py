import logic
from datas import datas
import numpy as np

df = datas.toDataFrame("./","amzn.h5","amzn")
#print df

def _renko(df):
    atr = logic.ATR(df, 22)
    brick = int(np.mean(atr.tail(55)))
    print brick

if __name__ == '__main__':
    _renko(df)