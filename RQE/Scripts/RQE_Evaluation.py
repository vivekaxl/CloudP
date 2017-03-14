import numpy as np
import matplotlib.pyplot as plt

def draw_graph(data):
    files = data.keys()

    names = ['SS'+ str(i+1) for i in xrange(len(data.keys()))]
    print names

    new_data = []
    for file in files:
        new_data.append([file.split('/')[-1]] + [
            np.mean(data[file]['RankProgressive']['training_size']),
            np.mean(data[file]['UseAll']['training_size']),
            np.mean(data[file]['FactorialDesign']['training_size']),
            np.mean(data[file]['MMREProgressive']['training_size']),

                                  ])
    for i,nd in enumerate(new_data): print i, nd

    data = sorted(data, key=lambda x: x[-1])
    N = len(data)
    dumb_evals = [d[1] for d in new_data]
    useall_evals = [d[2] for d in new_data]
    fact_evals = [d[3] for d in new_data]
    mmre_evals = [d[4] for d in new_data]

    # converting to ratios
    dumb_evals = [(d/proj)*100 for d, proj in zip(dumb_evals, useall_evals)]
    fact_evals = [(d/proj)*100 for d, proj in zip(fact_evals, useall_evals)]
    mmre_evals = [(d/proj)*100 for d, proj in zip(mmre_evals, useall_evals)]
    useall_evals = [100 for _ in useall_evals]

    space = 7
    ind = np.arange(space, space*(len(data)+1), space)  # the x locations for the groups
    width = 1.5        # the width of the bars

    fig, ax = plt.subplots()
    ax.plot([i for i in xrange(3, 50)], [100 for _ in xrange(3, 50)], linestyle='--', color='black', label='UseAll')
    rects1 = ax.bar(ind, dumb_evals, width, color='#f0f0f0', label='Rank-based')
    rects2 = ax.bar(ind + 1 * width, fact_evals, width, color='#bdbdbd', label='FullFactorial')
    rects3 = ax.bar(ind + 2 * width, mmre_evals, width, color='#636363', label='Projective Sampling')

    ax.set_ylabel('Evaluations as % of UseAll')
    # ax.set_title('Scores by group and gender')

    ax.set_xticks(ind + 2*width / 2)
    ax.set_xticklabels(['SS'+str(x+1) for x in xrange(len(data))], rotation='vertical')

    ax.set_xlim(3, 50)
    ax.set_ylim(1, 105)

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3, fancybox=True, frameon=False)

    handles, labels = ax.get_legend_handles_labels()
    print handles
    print labels
    plt.legend([handles[1], handles[2], handles[3], handles[0]], [labels[1], labels[2], labels[3], labels[0]], bbox_to_anchor=(0.85, 1.1), ncol=4, fancybox=True, frameon=False)

    fig.set_size_inches(14, 5)
    # plt.show()
    plt.savefig('RQE_Evaluations.png', bbox_inches='tight')


import pickle
data = pickle.load(open("../PickleLocker/RQE.p"))
draw_graph(data)