import matplotlib.pyplot as plt
import numpy as np
import math
 
from readjson import *

pr = 0.5
ps = 0.075
pq = np.linspace(ps, pr, 1000, endpoint=False)

def lam(a,b) :
    return a*np.log2( (a+b)/a ) + b*np.log2( (a+b)/b )

fn = "../data/test_set_"
def get_data_field (field, pql) :
    return [get_compressed_data(fn, ps, pq, pr)[field] for pq in pql]

# plot the data                                                                      
# case p_r = 0.5
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title("$p_r = 0.5$, $p_s = .075$",fontsize=16,pad=16)
ax.set_xlabel('$p_q$',fontsize=16,labelpad=16)
ax.set_ylabel('Normalized average bits',fontsize=16,labelpad=16)

#ax.plot(pq,lam(ps, pr-pq), color='tab:blue', linewidth=1.0)
ax.plot(pq,lam(ps, pr-pq), 'k', label = r'$\Lambda(p_s, p_r - p_q)$', linewidth=1.0)
ax.plot(pq,lam(pq, pr - pq), ':r', label = r'$\Lambda(p_q, p_r - p_q)$', linewidth=0.5)    
ax.plot(pq, lam(ps, pr-ps) + 0*pq, ':g', label = r'$\Lambda(p_s, p_r-p_s)$', linewidth=0.5)
ax.plot(pq,pr + ps - pq,  ':b', label = 'Linear Code', linewidth=0.5)

# partition code
pql = [.485,.475,.425,.375,.325]
pts = get_data_field('partition_mean_normalized', pql)
ax.plot(pql, pts,'b.')

pql = [.275, .225,.175,.125]
pts =  get_data_field('partition_mean_normalized',pql)
ax.plot(pql, pts,'b.', ms=2)

#enumerate sender
pql = [.475,.425,.375,.325]
pts = get_data_field('enum_sender_mean_normalized', pql)
ax.plot(pql,pts,'g.', ms=2)

pql = [.275,.225,.175,.125]
pts = get_data_field('enum_sender_mean_normalized', pql)
ax.plot(pql, pts,'g.')

#enumerate query complement

pql = [.485, .48, .475, .425,.375,.325,.275,.225,.175,.125]
pts = get_data_field('enum_query_compl_mean_normalized', pql)
ax.plot(pql,pts,'r.', ms=2)

pql = [.495,.49]
pts = get_data_field('enum_query_compl_mean_normalized', pql)
ax.plot(pql, pts, 'r.')

ax.legend(loc = 'lower left',fontsize=14)

#plt.show()
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.savefig('methods_targeted_queries.png',dpi=300,bbox_inches='tight') 
