import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score



import seaborn as sns
sns.set_style("darkgrid")

experiment = "E4"
humandatafile = "human{}.csv".format(experiment)
#synthdatafile = "synth{}.csv".format(experiment)
synthdatafile = "e4bisCORTOFINAL.csv"

pd.set_option("display.max_colwidth", None)

human_data = pd.read_csv(humandatafile)
synth_data = pd.read_csv(synthdatafile)


metrics = { "resources":1,
            "exploitation":2,
            "exploration":3,
            "balance":4,
            "performance":5
            }

def get_means( metric):

    x_values = human_data.iloc[:,metrics[metric] + 1]
    y_values = synth_data.iloc[:,metrics[metric] + 1]

    return x_values, y_values



for metric_tuple in metrics.items():

    metric = metric_tuple[0]
    print('metric: {}'.format(metric))
    x_values, y_values = get_means(metric)

    print('x values')
    print(x_values)
    print('y_values')
    print(y_values)

    correlation_matrix = np.corrcoef(x_values, y_values)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    print("r squared a patita " , r_squared)
    #r_squared = r2_score(x_values, y_values)

    fig_dims = (6, 6)
    f, ax = plt.subplots(figsize=fig_dims)

    f = sns.scatterplot( x_values, y_values)
    f.plot([0,1], [0,1],':r')

    f.set_xlabel("Participants Mean Experiment 3", fontsize=14)
    f.set_ylabel("Generative Model Mean Experiment 3", fontsize=14)

    plt.legend(labels=["Line Best Fit","Instance"], title= "R\u00b2: {:.4f}".format(r_squared), fontsize= 12)
    f.set(ylim=(-0.02, 1))
    f.set(xlim=(-0.02, 1))
    plt.title("Comparison  Model for {} (R\u00b2)".format(metric))

    plt.setp(f.get_legend().get_texts(), fontsize='12')

    # for legend title
    plt.setp(f.get_legend().get_title(), fontsize='16')

    plt.tight_layout()
    plt.savefig('figures/{}bisr2_{}.png'.format(experiment , metric))
    plt.show()


