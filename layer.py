import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['savefig.dpi'] = 800  # 图片像素
plt.rcParams['figure.dpi'] = 800  # 分辨率
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['mathtext.fontset'] = 'stix'

# 数据
xticks_label = ['turbo', 'plus', 'max']
# HR = [0.81, 0.84, 0.82]
# Recall = [0.74, 0.78, 0.81]

# HR = [0.82,0.84,0.82]
# Recall = [0.74, 0.77, 0.81]

HR = [0.62, 0.70, 0.75]
Recall = [0.73, 0.77, 0.79]

# 创建图形和轴
fig, ax1 = plt.subplots(dpi=800, figsize=(10, 7))
fig.subplots_adjust(left=0.1, right=0.9, bottom=0.16, top=0.9)

# 绘制 HR 折线图
ax1.set_ylim([0.61, 0.85])
ax1.set_yticks(np.arange(0.61, 0.86, 0.04))
ax1.plot(xticks_label, HR, color='b', marker='o', markersize=7, linewidth=2, label='HR', zorder=3)
ax1.set_xlabel(r'Judgment',
               fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 30})  # 设置 x 轴标签
ax1.set_ylabel('HR', color='b',
               fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 15})  # 设置 HR 的 y 轴标签和颜色
ax1.tick_params(axis='y', labelcolor='b')  # 设置 HR 的 y 轴刻度颜色
ax1.spines['top'].set_visible(True)  # Top border
ax1.spines['right'].set_visible(True)  # Right border
ax1.spines['bottom'].set_visible(True)  # Bottom border
ax1.spines['left'].set_visible(True)  # Left border

# 创建共享 x 轴的第二个 y 轴
ax2 = ax1.twinx()
# 绘制 Recall 折线图
ax2.set_ylim([0.72, 0.81])
ax2.set_yticks(np.arange(0.72, 0.81, 0.03))
ax2.plot(xticks_label, Recall, color='r', marker='s', markersize=7, linewidth=2, label='Recall', zorder=3)
ax2.set_ylabel('Recall', color='r',
               fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 15})  # 设置 Recall 的 y 轴标签和颜色
ax2.tick_params(axis='y', labelcolor='r')  # 设置 Recall 的 y 轴刻度颜色

# 添加图例
ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.1))
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1.1))

for i in range(3):
    ax1.axvline(x=i, ymin=0, ymax=1, color='gray', linestyle='--', linewidth=1, zorder=2)

# 显示图形
plt.savefig('txtfile/Judgment_Qwen_f2.png', dpi=800)
plt.show()
