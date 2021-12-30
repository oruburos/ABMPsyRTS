import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



humandatafile = "humanE1.csv"
synthdatafile = "synthE1.csv"


pd.set_option("display.max_colwidth", None)

human_data = pd.read_csv(humandatafile)
synth_data = pd.read_csv(synthdatafile)

print(human_data.shape)
print(synth_data.shape)

print(human_data.columns)
print(synth_data.columns)


metrics = { "resources":1,
            "exploration" :3,
            "exploitaation":2,
            "balance":4,
            "performance":5
            }

def get_means( metric):
    x_values = human_data.iloc[metrics[metric] +2]
    y_values = synth_data.iloc[metrics[metric] + 2]

    return x_values, y_values





#resources for visibility

x_values = [0.479, 0.350, 0.555 , 0.438 , 0.883, 0.795]
y_values = [0.429 ,0.320,0.523,0.603 ,0.664,0.806]

correlation_matrix = np.corrcoef(x_values, y_values)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2

print("R for Resources {}".format(r_squared))

#Exploitation
x_values = [0.178,0.110,
0.231,
0.132,
0.383,
0.256
]
y_values = [0.173,
0.109,
0.208,
0.178,
0.227,
0.227
]

correlation_matrix = np.corrcoef(x_values, y_values)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2


print("R for Exploitation {}".format(r_squared))


#Exploration
x_values = [0.084,
0.143,
0.116,
0.182,
0.178,
0.292

]
y_values = [0.0899,
0.113,
0.116,
0.242,
0.199,
0.327
]

correlation_matrix = np.corrcoef(x_values, y_values)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2


print("R for Exploration {}".format(r_squared))


#Balance
x_values = [-0.016,
0.354,
0.081,
0.387,
-0.227,
0.104
]
y_values = [-0.289,
0.0497,
-0.270,
0.159,
-0.0587,
0.182,
]

correlation_matrix = np.corrcoef(x_values, y_values)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2


print("R for Balance {}".format(r_squared))


#Performance
x_values = [0.260,
0.253,
0.341,
0.312,
0.535,
0.534,

]
y_values = [0.262,
0.222,
0.324,
0.420,
0.426,
0.554,
]

correlation_matrix = np.corrcoef(x_values, y_values)
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2


print("R for Performance {}".format(r_squared))

from sklearn.metrics import r2_score
print(r2_score(x_values, y_values))
fig, ax = plt.subplots()
ax.scatter(x_values, y_values)
ax.plot([0, 1], [0,1], lw=1)
ax.set_xlabel('Human')
ax.set_ylabel('Model')

plt.show()

import seaborn as sns
sns.set_style("darkgrid")


f = sns.scatterplot( x_values, y_values)
f.plot([0,1], [0,1],':r')
'''
ax = sns.regplot(x=x_values,
                 y=y_values,
                 marker='X',
                 color="purple",
                 line_kws={'color':'blue'})
ax.axhline(2)

'''
f.set_xlabel("Participants Mean", fontsize=14)
f.set_ylabel("Generative Model Mean", fontsize=14)

plt.legend(labels=["Line Best Fit","Instance"], title= "R\u00b2: {:.2f}".format(r_squared), loc = 2, bbox_to_anchor = (1,1), fontsize= 12)
f.set(ylim=(-0.02, 1))
f.set(xlim=(-0.02, 1))
plt.title("Comparison  Model for Performance (R\u00b2)")

plt.setp(f.get_legend().get_texts(), fontsize='12')

# for legend title
plt.setp(f.get_legend().get_title(), fontsize='16')

plt.tight_layout()
plt.savefig('../figures/r2Performance.png')
plt.show()

