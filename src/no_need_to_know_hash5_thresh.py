import matplotlib.pyplot as plt
import numpy as np
from readjson import *
from elias_delta import *

def lam(a,b):
    return a*np.log2( np.divide(a+b,a) ) + b*np.log2( np.divide(a+b,b) )

pr = .5
ps = .075
prl = (.25/2, .35/2, .45/2, .55/2, .65/2, .75/2, .85/2)

shannon_size = lam(ps,np.array(prl)-ps)


ps_size = lam(ps,1-ps)

fn = "../data/test_set_"
compressed_data = [get_compressed_data(fn, ps, pq, pr) for pq in prl]

def get_min_code(data) :
    nvars = data["num_vars"]
    rkern_cost = nvars
    npr = data["p_query"]
    # alt def of cost of transmitting r kernel size, increases from 10 -> 14
    # rkern_cost = len(EliasDeltaEncode(int(npr*(2**nvars))))
    return rkern_cost / (2 ** nvars) + min([data['hash_sq_mean_normalized'], data['enum_sender_only_mean_normalized']])

compress_sizes = {
#    r'Shannon $\Lambda$ (semantic)' : shannon_size,
    'New practical algorithms': [get_min_code(data) for data in compressed_data],
    'Decision Tree (classic)': [data['normed_min_tnf'] for data in compressed_data]
}
print(compress_sizes)
print(prl)

print("shannon", shannon_size)
print("hash", [data['hash_sq_mean_normalized'] for data in compressed_data])
print("sender", [data['enum_sender_mean_normalized'] for data in compressed_data])
nvars = 10
print("rkern", [len(EliasDeltaEncode(int(data["p_query"]*(2**nvars))))/(2**nvars) for data in compressed_data])


x = np.arange(len(prl))  # the label locations
width = 0.25  # the width of the bars
multiplier = .5

fig, ax = plt.subplots(layout='constrained')
fig.set_figheight(6)
fig.set_figwidth(7)

shan_ones = tuple(1.0 for z in shannon_size)


def normalize (vec) :
    return tuple(vec[i]/shannon_size[i] for i in range(len(vec)))

mycolors = ['tab:cyan', 'tab:red']

# Horizontal line at y=1
ax.axhline(y=1, color='tab:grey', linestyle='--', label=r'New fundamental limit $\Lambda$')

for ((attribute, measurement), col) in zip(compress_sizes.items(), mycolors):
    offset = width * multiplier
    rects = ax.bar(x + offset, normalize(measurement), width, label=attribute, color=col)
    multiplier += 1

fs=20

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Relative compression ($p_s = p_q = .075$)',fontsize=fs)
ax.set_xlabel('Normalized Receiver Kernel Size ($p_r$)',fontsize=fs)
ax.set_ylabel(r'Multiple of $\Lambda$',fontsize=fs)
ax.set_xticks(x + width, prl, fontsize=fs-3)
ylim = 11
ax.set_yticks(tuple(i+1 for i in range(ylim-1)),tuple(i+1 for i in range(ylim-1)),fontsize=fs)
ax.legend(loc='upper right',fontsize=fs)#, ncols=3)
ax.set_ylim(0.0, ylim)

#print("Dot per inch(DPI) for the figure is: ", fig.dpi)
#bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
#width, height = bbox.width, bbox.height
#print("Axis sizes are(in pixels):", width, height)




#plt.show()
plt.savefig('no_need_to_know_hash_5_thresh.png')
