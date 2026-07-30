"""Fig. 3(a): relative compression for targeted queries (p_r = .5, p_s = .075).

Bars show the best new practical code and the classic decision-tree baseline,
each as a multiple of the fundamental limit Lambda, across query kernel sizes.
"""

import matplotlib.pyplot as plt
import numpy as np

from readjson import get_compressed_data

pr = .5
ps = .075
pql = (.25/2, .35/2, .45/2, .55/2, .65/2, .75/2, .85/2)


def lam(a, b):
    return a*np.log2((a+b)/a) + b*np.log2((a+b)/b)


shannon_size = [lam(ps, pr-pq) for pq in pql]

fn = "../data/test_set_"
compressed_data = [get_compressed_data(fn, ps, pq, pr) for pq in pql]


def get_min_code(data):
    return min([data['partition_mean_normalized'], data['enum_sender_mean_normalized'], data['enum_query_compl_mean_normalized']])


compress_sizes = {
    'New practical algorithms': [get_min_code(data) for data in compressed_data],
    'Decision Tree (classic)': [data['normed_min_tnf'] for data in compressed_data]
}


x = np.arange(len(pql))  # the label locations
width = 0.25  # the width of the bars
multiplier = .5

fig, ax = plt.subplots(layout='constrained')
fig.set_figheight(6)
fig.set_figwidth(7)


def normalize(vec):
    return tuple(vec[i]/shannon_size[i] for i in range(len(vec)))


mycolors = ['tab:cyan', 'tab:red']

# Horizontal line at y=1
ax.axhline(y=1, color='tab:grey', linestyle='--', label=r'New fundamental limit $\Lambda$')

for ((attribute, measurement), col) in zip(compress_sizes.items(), mycolors):
    offset = width * multiplier
    ax.bar(x + offset, normalize(measurement), width, label=attribute, color=col)
    multiplier += 1


fs = 20
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Relative compression ($p_r = .5$, $p_s = .075$)', fontsize=fs)
ax.set_xlabel('Normalized Query Kernel Size ($p_q$)', fontsize=fs)
ax.set_ylabel(r'Multiple of $\Lambda$', fontsize=fs)
ax.set_xticks(x + width, pql, fontsize=fs-3)
ylim = 11
ax.set_yticks(tuple(i+1 for i in range(ylim-1)), tuple(i+1 for i in range(ylim-1)), fontsize=fs)
ax.legend(loc='upper left', fontsize=fs)
ax.set_ylim(0, ylim)

plt.savefig('fig03a_empirical_results_targeted_queries.png')
