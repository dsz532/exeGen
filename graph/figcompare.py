import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['savefig.dpi'] = 800
plt.rcParams['figure.dpi'] = 800
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['mathtext.fontset'] = 'stix'

categories = ['KR', 'Clarity', 'AA', 'DA', 'EF']
data0 = [4.47457627118644, 4.593220338983051, 4.610169491525424, 4.271186440677966, 4.2491525423728815]
data1 = [4.45, 4.85, 4.65, 4.25, 4.1]
data2 = [4.6, 4.6, 4.5, 4.15, 4.85]

# fig, ax = plt.subplots(figsize=(6, 4))
#
# y_pos = np.arange(len(categories))
#
# bars1 = ax.barh(y_pos, -np.array(data1), align='center', color='#31859C', label='Manual scoring')
#
# bars2 = ax.barh(y_pos, data2, align='center', color='#D58882', label='GPT scoring')
#
# ax.set_yticks(y_pos)
# ax.set_yticklabels(categories, fontweight='bold', fontsize=18)
# ax.set_xlim(-7, 7)
#
# ax.set_xlabel(r'compare',
#                    fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})
#
# plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.15), frameon=False, fontsize=15)
#
# ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
#
# ax.set_xticks([-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7])
# ax.set_xticklabels([7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7],fontweight='bold', fontsize=18)
#
# for bar in bars1:
#     width = bar.get_width()
#     label = f'{abs(width):.2f}'
#     ax.text(width, bar.get_y() + bar.get_height() / 2, label, va='center', ha='right', color='black',fontsize=13)
#
# for bar in bars2:
#     width = bar.get_width()
#     label = f'{width:.2f}'
#     ax.text(width, bar.get_y() + bar.get_height() / 2, label, va='center', ha='left', color='black',fontsize=13)
#
# plt.tight_layout(rect=[0, 0, 1, 1])
#
# plt.savefig('txtfile/figcompare.png', dpi=800, bbox_inches='tight')
#
# plt.show()
fig, ax = plt.subplots(figsize=(6, 4))

ax.set_ylim(0, 7)
bar_width = 0.36

index = range(len(categories))

ax.bar([i - 0.5 * bar_width for i in index], data1, width=bar_width, alpha=0.8, color='#75D497',
       label='Students scoring')
# ax.bar([i - 0.5*bar_width for i in index], data0, width=bar_width, color='#5da5d1', label='Expert scoring', alpha=0.8)
ax.bar([i + 0.5 * bar_width for i in index], data2, width=bar_width, alpha=0.8, color='#fd9c51', label='GPT scoring')

ax.set_xticks(index)
ax.set_xticklabels(categories)

ax.set_xlabel(r'compare',
              fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 20})

ax.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.2), frameon=False, fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig('txtfile/figcomparestu.png', dpi=800, bbox_inches='tight')
plt.show()
