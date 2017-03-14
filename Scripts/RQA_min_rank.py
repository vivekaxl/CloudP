from __future__ import division
import matplotlib.pyplot as plt
import pickle
import numpy as np


def draw_graph(data):
    files = data.keys()

    names = ['SS'+ str(i+1) for i in xrange(len(data.keys()))]
    print names

    new_data = []
    for file in files:
        new_data.append([file.split('/')[-1]] + [
            np.mean(data[file]['RankProgressive']['min_rank']),
            np.mean(data[file]['UseAll']['min_rank']),
            np.mean(data[file]['FactorialDesign']['min_rank']),
            np.mean(data[file]['MMREProgressive']['min_rank']),

                                  ])
    for i,nd in enumerate(new_data): print i, nd

    gap = 35
    left, width = .53, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height

    f, ((ax1, ax2, ax3, ax4)) = plt.subplots(1, 4)

    # for dumb learner
    ax1.scatter([gap*(i+1) for i in xrange(len(files))], [d[1] for d in new_data], color='b', marker='v', s=34)

    ax1.tick_params(axis=u'both', which=u'both',length=0)
    ax1.set_title('Rank-based', fontsize=16)
    ax1.set_ylabel("Rank Difference (RD)", fontsize=16)


    # ax2.set_ylim(-2,25)
    # ax2.set_xlim(10, 900)
    ax2.scatter([gap*(i+1) for i in xrange(len(files))], [d[2] for d in new_data], color='b', marker='v', s=34)

    ax2.tick_params(axis=u'both', which=u'both',length=0)
    ax2.set_title('UseAll', fontsize=16)
    ax2.set_ylabel("Rank Difference (RD)", fontsize=16)
    # ax2.set_xlabel("Accuracy")

    # ax3.set_ylim(-2,14)
    # ax3.set_xlim(10, 900)
    ax3.scatter([gap*(i+1) for i in xrange(len(files))], [d[3] for d in new_data], color='b', marker='v', s=34)

    ax3.tick_params(axis=u'both', which=u'both',length=0)
    ax3.set_title('Factorial Design', fontsize=16)
    ax3.set_ylabel("Rank Difference (RD)", fontsize=16)
    # ax3.set_xlabel("Accuracy")

    ax3.scatter([gap*(i+1) for i in xrange(len(files))], [d[3] for d in new_data], color='b', marker='v', s=34)

    ax3.tick_params(axis=u'both', which=u'both',length=0)
    ax3.set_title('Factorial Design', fontsize=16)
    ax3.set_ylabel("Rank Difference (RD)", fontsize=16)

    ax4.scatter([gap*(i+1) for i in xrange(len(files))], [d[4] for d in new_data], color='b', marker='v', s=34)

    ax4.tick_params(axis=u'both', which=u'both',length=0)
    ax4.set_title('MMREProgressive', fontsize=16)
    ax4.set_ylabel("Rank Difference (RD)", fontsize=16)

    from matplotlib.lines import Line2D

    # circ3 = Line2D([0], [0], linestyle="none", marker="x", alpha=0.3, markersize=10, color="r")
    # circ1 = Line2D([0], [0], linestyle="none", marker="v", alpha=0.4, markersize=10, color="g")
    # circ2 = Line2D([0], [0], linestyle="none", marker="o", alpha=0.3, markersize=10, color="y")
    # circ4 = Line2D([0], [0], linestyle="none", marker="h", alpha=0.3, markersize=10, color="violet")

    plt.sca(ax1)
    plt.xticks([gap], names, rotation=90, fontsize=12)

    plt.sca(ax2)
    plt.xticks([gap], names, rotation=90, fontsize=12)

    plt.sca(ax3)
    plt.xticks([gap], names, rotation=90, fontsize=12)

    plt.sca(ax4)
    plt.xticks([gap], names, rotation=90, fontsize=12)
    #
    # plt.figlegend((circ1, circ2, circ3, circ4), ('<5%', '5%<MMRE<10%', '10%<MMRE<100%', '>100%'), frameon=False, loc='lower center',
    #               bbox_to_anchor=(0.4, -0.04),fancybox=True, ncol=4, fontsize=16)

    f.set_size_inches(22, 5.5)
    # plt.show()

    plt.savefig('RQE_min_rank', bbox_inches='tight')


data = pickle.load(open("../PickleLocker/RQA.p"))
data1 = pickle.load(open("../PickleLocker/RQA_rank.p"))

data['/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_AverageSLA']['RankProgressive'] = data1['/Users/viveknair/GIT/CloudP/Data/Client/collector.csv_AverageSLA']['RankProgressive']

draw_graph(data)
filenames = data.keys()
for filename in filenames:
    methods = data[filename].keys()
    print filename
    for method in methods:
        min_rank = np.mean(data[filename][method]['min_rank'])
        training_size = np.mean(data[filename][method]['training_size'])
        mmre = np.mean(data[filename][method]['mmre'])
        abs_diff = np.mean(data[filename][method]['abs_diff'])

        print method, min_rank, training_size, mmre, abs_diff
    print