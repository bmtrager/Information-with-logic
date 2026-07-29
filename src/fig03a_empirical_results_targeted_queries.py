import matplotlib.pyplot as plt
import numpy as np
from readjson import *

pr = .5
ps = .075
pql = (.25/2, .35/2, .45/2, .55/2, .65/2, .75/2, .85/2)

def lam(a,b) :
    return a*np.log2( (a+b)/a ) + b*np.log2( (a+b)/b )

#shannon_size = (.59, .56, .52, .49, .44, .38, .30)

shannon_size = [lam(ps, pr-pq) for pq in pql]
#print(shannon_size)

fn = "../data/test_set_"
compressed_data = [get_compressed_data(fn, ps, pq, pr) for pq in pql]

def get_min_code(data) :
    return min([data['partition_mean_normalized'], data['enum_sender_mean_normalized'], data['enum_query_compl_mean_normalized']])

compress_sizes = {
#    r'New fundamental limit $\Lambda$' : shannon_size,
    'New practical algorithms': [get_min_code(data) for data in compressed_data],
#    'Receiver_informed' : [data['normed_min_riquery_tnf'] for data in compressed_data],
    'Decision Tree (classic)': [data['normed_min_tnf'] for data in compressed_data]
}

#print(compress_sizes)


x = np.arange(len(pql))  # the label locations
width = 0.25  # the width of the bars
multiplier = .5

fig, ax = plt.subplots(layout='constrained')
fig.set_figheight(6)
fig.set_figwidth(7)

shan_ones = tuple(1.0 for z in shannon_size)

def normalize (vec):
    return tuple(vec[i]/shannon_size[i] for i in range(len(vec)))

mycolors_hatch = (('tab:cyan', ''), ('tab:cyan', 'xx'), ('tab:orange', ''), ('tab:orange', 'xx'))
#mycolors = ['tab:blue', 'tab:cyan', 'tab:pink', 'tab:red']
#mycolors = ['tab:cyan', 'tab:pink', 'tab:red']
mycolors = ['tab:cyan', 'tab:red']

# Horizontal line at y=1
ax.axhline(y=1, color='tab:grey', linestyle='--', label=r'New fundamental limit $\Lambda$')

for ((attribute, measurement), col) in zip(compress_sizes.items(), mycolors):
    offset = width * multiplier
    rects = ax.bar(x + offset, normalize(measurement), width, label=attribute, color=col)
    multiplier += 1


fs=20
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Relative compression ($p_r = .5$, $p_s = .075$)',fontsize=fs)
ax.set_xlabel('Normalized Query Kernel Size ($p_q$)',fontsize=fs)
ax.set_ylabel(r'Multiple of $\Lambda$',fontsize=fs)
ax.set_xticks(x + width, pql, fontsize=fs-3)
ylim = 11
ax.set_yticks(tuple(i+1 for i in range(ylim-1)),tuple(i+1 for i in range(ylim-1)),fontsize=fs)
ax.legend(loc='upper left',fontsize=fs)#, ncols=3)
ax.set_ylim(0, ylim)

#print("Dot per inch(DPI) for the figure is: ", fig.dpi)
#bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
#width, height = bbox.width, bbox.height
#print("Axis sizes are(in pixels):", width, height)




#plt.show()
plt.savefig('fig03a_empirical_results_targeted_queries.png')
