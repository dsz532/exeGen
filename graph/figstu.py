import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.size'] = 15
plt.rcParams['legend.fontsize'] = 15
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
data = [4.45, 4.85, 4.65, 4.25, 4.1]
labels = ['KR', 'Clarity', 'AA', 'DA', 'EF']

colors = ['#2c73d2', '#0081cf', '#0089ba', '#008e9b', '#008f7a']

fig, ax = plt.subplots(figsize=(6, 4))

ax.set_ylim(0, 6)
bars = ax.bar(labels, data, align='center', width=0.5, color=colors)

ax.set_xlabel('Students Judge', fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig('txtfile/figstu.png', dpi=800, bbox_inches='tight')
plt.show()