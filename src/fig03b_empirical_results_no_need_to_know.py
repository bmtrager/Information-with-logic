"""Fig. 3(b): relative compression when there is no need to know (p_s = p_q = .075).

Bars show the best new practical code and the classic decision-tree baseline,
each as a multiple of the fundamental limit Lambda, across receiver kernel sizes.
"""

import matplotlib.pyplot as plt
import numpy as np

from readjson import get_compressed_data


def lam(a, b):
    return a*np.log2(np.divide(a+b, a)) + b*np.log2(np.divide(a+b, b))


pr = .5
ps = .075
prl = (.25/2, .35/2, .45/2, .55/2, .65/2, .75/2, .85/2)

shannon_size = lam(ps, np.array(prl)-ps)

fn = "../data/test_set_"
compressed_data = [get_compressed_data(fn, ps, pq, pr) for pq in prl]


def get_min_code(data):
    nvars = data["num_vars"]
    rkern_cost = nvars
    return rkern_cost / (2 ** nvars) + min([data['hash_sq_mean_normalized'], data['enum_sender_only_mean_normalized']])


compress_sizes = {
    'New practical algorithms': [get_min_code(data) for data in compressed_data],
    'Decision Tree (classic)': [data['normed_min_tnf'] for data in compressed_data]
}


x = np.arange(len(prl))  # the label locations
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
ax.set_title('Relative compression ($p_s = p_q = .075$)', fontsize=fs)
ax.set_xlabel('Normalized Receiver Kernel Size ($p_r$)', fontsize=fs)
ax.set_ylabel(r'Multiple of $\Lambda$', fontsize=fs)
ax.set_xticks(x + width, prl, fontsize=fs-3)
ylim = 11
ax.set_yticks(tuple(i+1 for i in range(ylim-1)), tuple(i+1 for i in range(ylim-1)), fontsize=fs)
ax.legend(loc='upper right', fontsize=fs * 0.875)  # matches fig05's label:legend ratio (16:14)
ax.set_ylim(0.0, ylim)

plt.savefig('fig03b_empirical_results_no_need_to_know.pdf')
