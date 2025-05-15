import numpy as np
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
categories = ["LLaMa", "Qwen", "GPT-4o"]

#
Single_Choice = [0.59, 0.81, 0.70, 0.60, 0.74, 0.75]
Multiple_Choice = [0.61, 0.82, 0.79, 0.52, 0.74, 0.82]
Judgment = [0.41, 0.62, 0.65, 0.62, 0.73, 0.72]

x = np.arange(6)
width = 0.7
colors = ['#86A3B8', '#E8D2A6', '#8ECFC9', '#86A3B8', '#E8D2A6', '#8ECFC9']

fig, axs = plt.subplots(1, 1, figsize=(4, 3))

for i in range(3):
    axs.bar(i*0.9, Single_Choice[i], width, color=colors[i], edgecolor='black')
for i in range(3, 6):
    axs.bar(i*0.9+0.4, Single_Choice[i ], width, color=colors[i ], edgecolor='black')
axs.set_ylabel('Single Choice')
axs.set_ylim(0.1, 1)
axs.set_xticks([1.35 * width, 6.67 * width], ['HR', 'Recall'])

# for i in range(3):
#     axs.bar(i*0.9, Multiple_Choice[i], width, color=colors[i], edgecolor='black')
# for i in range(3, 6):
#     axs.bar(i*0.9+0.4, Multiple_Choice[i ], width, color=colors[i ], edgecolor='black')
# axs.set_ylabel('Multiple Choice')
# axs.set_ylim(0.1, 1)
# axs.set_xticks([1.35 * width, 6.67 * width], ['HR', 'Recall'])

# for i in range(3):
#     axs.bar(i * 0.9, Judgment[i], width, color=colors[i], edgecolor='black')
# for i in range(3, 6):
#     axs.bar(i * 0.9 + 0.4, Judgment[i], width, color=colors[i], edgecolor='black')
# axs.set_ylabel('Judgment')
# axs.set_ylim(0.1, 1)
# axs.set_xticks([1.35 * width, 6.67 * width], ['HR', 'Recall'])

handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
fig.legend(handles, categories, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.95), frameon=False, fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.9])

plt.savefig('txtfile/fig1.png', dpi=600, bbox_inches='tight')

plt.show()

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.size'] = 18
plt.rcParams['legend.fontsize'] = 18
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']

categories = ["w/o. I-level", "w/o. R-level", "w/o. T-level", "w/o. I-condit", "w/o. R-condit", "Ours"]
Single_Choice = [0.0518, 0.0499, 0.0258, 0.0350, 0.0431, 0.0718]
Multiple_Choice = [0.0252, 0.0251, 0.0123, 0.0183, 0.0210, 0.0368]
Judgment = [0.0321, 0.0231, 0.0280, 0.0328, 0.0325, 0.0333]
ijcai_ndcg = [0.0196, 0.0126, 0.0151, 0.0188, 0.0186, 0.0201]

x = np.arange(len(categories))
width = 0.4  
colors = ['#86A3B8', '#E8D2A6', '#8ECFC9', '#F48484', '#AEE2FF', '#7286D3'] 

fig, axs = plt.subplots(1, 4, figsize=(20, 5))

for i in range(len(categories)):
    axs[0].bar(i, Single_Choice[i], width, color=colors[i])
axs[0].set_ylabel('HR@10')
axs[0].set_ylim(0.02, max(Single_Choice) + 0.005)
axs[0].set_xticks([])
axs[0].set_xlabel('BeiBei')
for i in range(len(categories)):
    axs[1].bar(i, Multiple_Choice[i], width, color=colors[i])
axs[1].set_ylabel('NDCG@10')
axs[1].set_ylim(0.01, max(Multiple_Choice) + 0.005)
axs[1].set_xticks([])
axs[1].set_xlabel('BeiBei')
for i in range(len(categories)):
    axs[2].bar(i, Judgment[i], width, color=colors[i])
axs[2].set_ylabel('HR@10')
axs[2].set_ylim(0.0225, max(Judgment) + 0.001)
axs[2].set_xticks([])
axs[2].set_xlabel('IJCAI')
for i in range(len(categories)):
    axs[3].bar(i, ijcai_ndcg[i], width, color=colors[i])
axs[3].set_ylabel('NDCG@10')
axs[3].set_ylim(0.012, max(ijcai_ndcg) + 0.001)
axs[3].set_xticks([])
axs[3].set_xlabel('IJCAI')
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
fig.legend(handles, categories, loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=len(categories))

handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
fig.legend(handles, categories, loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=len(categories))

plt.tight_layout(rect=[0, 0, 1, 0.9]) 

plt.savefig('F:\postgraduate work\ICDE2025\\fig\\ablation.png', dpi=600, bbox_inches='tight')

plt.show()


import seaborn as sns

sns.set()
import numpy as np
import matplotlib.pyplot as plt

font1 = {
    'family': 'Times New Roman', "weight": "normal", 'size': 18
}

if __name__ == '__main__':
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    matplotlib.rcParams['font.size'] = 20
    plt.rcParams['legend.fontsize'] = 18
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['mathtext.fontset'] = 'stix'
    Info1 = [0.8047, 0.4392, 0.3938 ]
    Info2 = [11.4680, 4.1398, 4.6082 ]
    Info1 = np.array(Info1)
    Info2 = np.array(Info2)
    x1 = range(len(Info1))
    x2 = range(len(Info2))
    fig, ax1 = plt.subplots(figsize=(9, 6))
    plt.rcParams['axes.facecolor'] = 'white'
    xticks_label = ['BeiBei', 'Tmall', 'IJCAI']

    xx1 = np.arange(len(Info1))
    xx2 = xx1 + 0.3

    ax1.set_xticks(xx1 + 0.2)
    ax1.set_xticklabels(xticks_label, fontdict={'family': 'Times New Roman', 'weight': 'bold', 'size': 18})

    ax1.set_ylim((0, 15))
    plt.yticks([0, 2, 4, 6, 8, 10, 12])
    total_width, n = 0.6, 2
    width = total_width / n

    bar1 = ax1.bar(xx1, Info1, width=width, align="center", label='CRGCN+D$^3$MBR', fc='#FCC898', edgecolor='black')
    bar2 = ax1.bar(xx2, Info2, width=width, align="center", label='DPT', fc='#82B0D2', edgecolor='black')

    ax1.bar_label(
        bar1,
        labels=None,
        fmt='%g',
        label_type='edge',
        padding=0,
        fontweight='bold',
        fontsize=16
    )

    ax1.bar_label(
        bar2,
        labels=None,
        fmt='%g',
        label_type='edge',
        padding=0,
        fontweight='bold',
        fontsize=16,
    )

    plt.legend(loc='best', prop={'weight': 'bold'})

    # ax1.spines['top'].set_visible(True)  # Top border
    # ax1.spines['right'].set_visible(True)  # Right border
    ax1.spines['bottom'].set_visible(True)  # Bottom border
    ax1.spines['left'].set_visible(True)  # Left border
    ax1.set_ylabel('Training Time Per Epoch (min)', fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 20})
    # ax1.spines['top'].set_color('black')  # Top border color
    # ax1.spines['right'].set_color('black')  # Right border color
    ax1.spines['bottom'].set_color('black')  # Bottom border color
    ax1.spines['left'].set_color('black')  # Left border color
    plt.tick_params(bottom=False, top=False, left=True, right=False)
    plt.gca().set_facecolor("white")
    plt.savefig('Training Time Per Epoch.png', dpi=600, bbox_inches='tight')
    plt.show()




import matplotlib.pyplot as plt
import numpy as np
from matplotlib.legend_handler import HandlerTuple

matplotlib.rcParams['font.size'] = 20
plt.rcParams['legend.fontsize'] = 20
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'

categories = ['IJCAI', 'Tmall', 'BeiBei']
fig, ax = plt.subplots(figsize=(8, 7))

skew_scores_top3 = [-0.8047, -0.4392, -0.3938]
skew_scores_top5 = [-11.4680, -4.1398, -4.6082]

red_scores_top3 = [15.35, 5.84, 5.65]
red_scores_top5 = [22.97, 18.96, 18.81]

bar_width = 0.05  

r = np.array([0, 0.25, 0.5])

ax.barh(r, skew_scores_top3, color='#31859B', height=bar_width, label='Skew')
ax.barh(r + bar_width, skew_scores_top5, color='#B7DDE8', height=bar_width, label='Skew')
ax.barh(r, red_scores_top3, color='#D58882', height=bar_width, label='RED')
ax.barh(r + bar_width, red_scores_top5, color='#EED0CE', height=bar_width, label='RED')

ax.set_ylabel('Datasets')
ax.set_yticks([r + bar_width * 0.5 for r in np.array([0, 0.25, 0.5])])
ax.set_yticklabels(categories)

custom_ticks = np.array([-12, -8, -4, 0, 4, 8, 12, 16, 20, 24])
ax.set_xticks(custom_ticks)
ax.set_xticklabels([str(abs(t)) for t in custom_ticks])  

ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True)  

ax.axvline(x=0, color='white', linestyle='-', linewidth=2)

ax.text(0.25, -0.1, 'Training Time Per Epoch (min)', transform=ax.transAxes)
ax.text(0.65, -0.1, 'GPU Memory Usage (GiB)', transform=ax.transAxes)

ax.set_xlim(-12, 24)


skew_handle_1 = plt.Line2D([0], [0], color='#31859B', lw=4)
skew_handle_2 = plt.Line2D([0], [0], color='#D58882', lw=4)
red_handle_1 = plt.Line2D([0], [0], color='#B7DDE8', lw=4)
red_handle_2 = plt.Line2D([0], [0], color='#EED0CE', lw=4)

skew_handles = (skew_handle_1, skew_handle_2)
red_handles = (red_handle_1, red_handle_2)

labels = ['D$^3$MBR + CRGCN', 'DPT']

ax.legend([skew_handles, red_handles], labels, handler_map={
    skew_handles: HandlerTuple(ndivide=None),
    red_handles: HandlerTuple(ndivide=None)
}, loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2, fontsize=16, frameon=True, framealpha=0.8, edgecolor='black')

plt.savefig('Test.png', dpi=600, bbox_inches='tight')

plt.show()
'''
