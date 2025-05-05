import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['savefig.dpi'] = 600  # 图片像素
plt.rcParams['figure.dpi'] = 600  # 分辨率
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['mathtext.fontset'] = 'stix'

# 示例数据
categories = ['KR', 'Clarity', 'AA', 'DA', 'EF']
data1 = [4.45, 4.85, 4.65, 4.25, 4.1]  # 第一组数据
data2 = [4.6, 4.6, 4.5, 4.15, 4.85]  # 第二组数据

# 将数据归一化到0-5的范围
max_value = max(max(data1), max(data2))  # 获取最大值
normalized_data1 = [x / max_value * 5 for x in data1]
normalized_data2 = [x / max_value * 5 for x in data2]

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(6, 4))

# 设置条形图的位置
y_pos = np.arange(len(categories))

# 绘制第一组数据的条形图（向左生长）
bars1 = ax.barh(y_pos, -np.array(data1), align='center', color='#31859C', label='Manual scoring')

# 绘制第二组数据的条形图（向右生长）
bars2 = ax.barh(y_pos, data2, align='center', color='#D58882', label='GPT scoring')

# 设置纵坐标标签
ax.set_yticks(y_pos)
ax.set_yticklabels(categories, fontweight='bold', fontsize=18)
# 设置横坐标范围为-5到5
ax.set_xlim(-7, 7)

# 设置横坐标标签
ax.set_xlabel(r'compare',
                   fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})

# 添加图例
plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.15), frameon=False, fontsize=15)

# 添加中心线
ax.axvline(0, color='black', linestyle='--', linewidth=0.8)

# 调整横坐标刻度标签，使其看起来是从0到5
ax.set_xticks([-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7])
ax.set_xticklabels([7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 7],fontweight='bold', fontsize=18)

# 在每个柱状图的顶端标注数值
for bar in bars1:
    width = bar.get_width()
    label = f'{abs(width):.2f}'  # 取绝对值并保留两位小数
    ax.text(width, bar.get_y() + bar.get_height() / 2, label, va='center', ha='right', color='black',fontsize=13)

for bar in bars2:
    width = bar.get_width()
    label = f'{width:.2f}'  # 保留两位小数
    ax.text(width, bar.get_y() + bar.get_height() / 2, label, va='center', ha='left', color='black',fontsize=13)

# 调整图形布局
plt.tight_layout(rect=[0, 0, 1, 1])

plt.savefig('txtfile/figcompare.png', dpi=5000, bbox_inches='tight')

# 显示图形
plt.show()
