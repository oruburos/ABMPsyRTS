##exp 3

# import pandas as pd
#
# data =[]
# for i in range(1,7):
#
#     data.append( pd.read_csv("model_paramsTEx3cond{}.csv".format(i)) )
#
#
# datafinal  = pd.concat(data)
#
# print(datafinal.shape)
#
# datafinal.to_csv("PsyRTSEx3Synth.csv")
#
#
import pandas as pd

data =[]
for i in range(3,6):

    data.append( pd.read_csv("model_paramsTEx1cond{}.csv".format(i)) )

datafinal  = pd.concat(data)

print(datafinal.shape)

datafinal.to_csv("PsyRTSEx1Synth.csv")