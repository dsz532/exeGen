import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.dpi'] = 600
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['mathtext.fontset'] = 'stix'

xticks_label = ['turbo', 'plus', 'max']

# Single Choice
HR = [0.81, 0.84, 0.82]
Recall = [0.74, 0.78, 0.81]

# Multiple Choice
# HR = [0.82,0.84,0.82]
# Recall = [0.74, 0.77, 0.81]

# Judgment
# HR = [0.62, 0.70, 0.75]
# Recall = [0.73, 0.77, 0.79]

x = [0.7, 1.5, 2.3]
fig, ax1 = plt.subplots(dpi=600, figsize=(5, 3))
fig.subplots_adjust(left=0.07, right=0.7, bottom=0.1, top=0.9)

ax1.set_xlim(0, 3)
ax1.set_xticks(list(x)[::], xticks_label)

ax1.set_ylim([0.61, 0.85])
ax1.set_yticks(np.arange(0.61, 0.86, 0.04))

ax1.set_xticklabels(xticks_label, fontweight='bold', fontsize=18)
ax1.plot(x, HR, color='#1F77B4', marker='o', markersize=7, linewidth=2, label='HR', zorder=3)
ax1.set_xlabel(r'Single Choice',
               fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 20})
# ax1.set_ylabel('HR', color='#00c2d0',
#                fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 15})
ax1.tick_params(axis='y', labelcolor='#1F77B4')
ax1.spines['top'].set_visible(True)  # Top border
ax1.spines['right'].set_visible(True)  # Right border
ax1.spines['bottom'].set_visible(True)  # Bottom border
ax1.spines['left'].set_visible(True)  # Left border

ax2 = ax1.twinx()
ax2.set_ylim([0.72, 0.84])
ax2.set_yticks(np.arange(0.72, 0.85, 0.03))
ax2.plot(x, Recall, color='#D62728', marker='s', markersize=7, linewidth=2, label='Recall', zorder=3)
# ax2.set_ylabel('Recall', color='#00a4de',
#                fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 15})
ax2.tick_params(axis='y', labelcolor='#D62728')

ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.12), frameon=False, fontsize=12)
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1.12), frameon=False, fontsize=12)

for i in x:
    ax1.axvline(x=i, ymin=0, ymax=1, color='gray', linestyle='--', linewidth=1, zorder=2)

plt.savefig('txtfile/Single_Qwen_f2.png', dpi=600, bbox_inches='tight')
plt.show()
