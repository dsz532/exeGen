import matplotlib.pyplot as plt
import numpy as np

# 数据
categories = ['KR', 'Clarity', 'AA', 'DA', 'EF', 'SE']

# Single Choice
LLaMa = [4.19, 4.19, 4.31, 4.11, 4.00, 3.90]
Qwen = [4.70, 4.69, 4.81, 4.69, 4.60, 4.47]
GPT4o = [4.81, 4.78, 4.89, 4.81, 4.72, 4.62]

# Multiple Choice
# LLaMa = [4.21, 4.62, 4.18, 4.18, 4.08, 4.18]
# Qwen = [4.70, 4.82, 4.73, 4.73, 4.63, 4.52]
# GPT4o = [4.81, 4.73, 4.79, 4.80, 4.58, 4.69]

# Judgment
# LLaMa = [4.47, 4.72, 4.27, 4.28, 4.01, 4.23]
# Qwen = [4.83, 4.79, 4.88, 4.54, 4.63, 4.53]
# GPT4o = [4.71, 4.61, 4.62, 4.80, 4.66, 4.63]

# 计算角度
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]  # 闭合图形

# 绘制雷达图
fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

# 绘制每组数据
ax.fill(angles, LLaMa + LLaMa[:1], alpha=0.25)
ax.plot(angles, LLaMa + LLaMa[:1], linewidth=2, label='LLaMa')

ax.fill(angles, Qwen + Qwen[:1], alpha=0.25)
ax.plot(angles, Qwen + Qwen[:1], linewidth=2, label='Qwen')

ax.fill(angles, GPT4o + GPT4o[:1], alpha=0.25)
ax.plot(angles, GPT4o + GPT4o[:1], linewidth=2, label='GPT4o')

# 添加分类标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=15)

# 设置 y 轴范围
ax.set_ylim(3.9, 5)
ax.set_yticks(np.arange(3.9, 5.1, 0.3))

# 添加图例
ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
ax.set_xlabel(r'Single Choice',
                   fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})

# 显示图形
plt.savefig('txtfile/single_rader.png', dpi=800, bbox_inches='tight')
plt.show()
