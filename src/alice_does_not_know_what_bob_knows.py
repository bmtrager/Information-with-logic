import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.cm as cm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.offsetbox import (TextArea, DrawingArea, AnchoredOffsetbox)
from readjson import *

def h(a):
    return -np.multiply(a,np.log2(a)) - np.multiply(1-a,np.log2(1-a))

def lam(a,b):
    return np.multiply(a , np.log2( np.divide(a+b,a) )) + np.multiply(b , np.log2( np.divide(a+b,b) ))

opr = 0.5
ps = 0.075

pql = [.475,.425,.375,.325,.275,.225,.175,.125]

pql1 = [.375, .475,.425]
pql2 = [.325,.275,.225,.175,.125]

fn = "../data/test_set_"
def get_data_field (field, pql) :
    print ([[fn, ps, pq, opr] for pq in pql])
    return [get_compressed_data(fn, ps, pq, opr)[field] for pq in pql]


delta = 0.001

ps = 0.075
pr = np.arange(ps+delta, 0.5, delta)
z = lam(ps, pr - ps)

fig, ax = plt.subplots()

z2 = np.ones(len(pr))*h(ps)
z3 = pr
ax.plot(pr,z,'k',label=r'$\Lambda(p_s,p_r-p_s)$')
#ax.plot(pr,z2,linestyle='dashed',lw=0.75,label='$H_{bin}(p_s)$')
z22 = np.ones(len(pr))*lam(ps, 1-ps)
ax.plot(pr,z22,':g',lw=0.75,label=r'$\Lambda(p_s, 1 - p_s)$')

#ax.plot(pr,z22,linestyle='dashed',lw=0.75,label=r'$\lambda(p_s, p_r-p_s)$')
ax.plot(pr,z3,':b',lw=0.75,label='Linear code')

print(pql)
pts1 = get_data_field('hash_sq_mean_normalized', pql1)
pts2 = get_data_field('hash_sq_mean_normalized', pql2)
ax.plot(pql1, pts1,'b.',ms=2)
ax.plot(pql2, pts2,'b.')

pts1 = get_data_field('enum_sender_only_mean_normalized', pql1)
pts2 = get_data_field('enum_sender_only_mean_normalized', pql2)
ax.plot(pql1, pts1,'g.')
ax.plot(pql2, pts2,'g.',ms=2)

ax.set_xlabel('$p_r$',fontsize=16,labelpad=16)
ax.set_ylabel('Normalized average bits',fontsize=16,labelpad=16)
ax.set_title('$p_s = p_q = .075$',fontsize=16,pad=16)
ax.legend(loc='lower right',fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=16)

#ax.set_xlim([0,1.0])
#ax.set_ylim([-0.1,1.1])
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
#plt.show()
#plt.savefig('alice_does_not_know_what_bob_knows.png',dpi=300)
plt.savefig('methods_no_need_to_know.png',dpi=300,bbox_inches='tight')


