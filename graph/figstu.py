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
# 数据
data = [4.45, 4.85, 4.65, 4.25, 4.1]
labels = ['KR', 'Clarity', 'AA', 'DA', 'EF']  # X轴的标签

# 定义每个柱子的颜色
colors = ['#2c73d2', '#0081cf', '#0089ba', '#008e9b', '#008f7a']

# 创建一个图形和子图
fig, ax = plt.subplots(figsize=(6, 4))

ax.set_ylim(0, 6)
# 绘制柱状图，设置柱子宽度为0.5（变细），并指定颜色
bars = ax.bar(labels, data, align='center', width=0.5, color=colors)  # 添加label用于图例

# 添加标题和标签
ax.set_xlabel('Students Judge', fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})  # X轴标签

# 显示数值
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

# 显示图表
plt.tight_layout(rect=[0, 0, 1, 1])
plt.savefig('txtfile/figstu.png', dpi=800, bbox_inches='tight')
plt.show()