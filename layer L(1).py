import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()

if __name__ == '__main__':

    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['savefig.dpi'] = 600  # 图片像素
    plt.rcParams['figure.dpi'] = 600  # 分辨率
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['mathtext.fontset'] = 'stix'

    # Single Choice
    # hr = [4.70, 4.88, 4.91]
    # Clarity = [4.69, 4.88, 4.90]
    # AA = [4.81, 4.90, 4.92]
    # DA = [4.69, 4.78, 4.83]
    # EF = [4.60, 4.75, 4.75]
    # SE = [4.47, 4.65, 4.80]

    # Multiple Choice
    # hr = [4.70, 4.75, 4.91]
    # Clarity = [4.82, 4.85, 4.90]
    # AA = [4.73, 4.80, 4.92]
    # DA = [4.73, 4.78, 4.83]
    # EF = [4.63, 4.70, 4.75]
    # SE = [4.52, 4.60, 4.80]

    # Judgment
    hr = [4.83, 4.85, 4.90]
    Clarity = [4.79, 4.83, 4.85]
    AA = [4.88, 4.92, 4.93]
    DA = [4.54, 4.65, 4.70]
    EF = [4.63, 4.75, 4.80]
    SE = [4.53, 4.60, 4.75]

    '''
    # sampling_steps20
    hr = [0.0473, 0.0512, 0.0473]
    ndcg = [0.0225, 0.0253, 0.0236]

    # steps20
    hr = [0.0512, 0.0418, 0.0368, 0.0412, 0.0423]
    ndcg = [0.0253, 0.0179, 0.0163, 0.0175, 0.0187]

    # steps10
    hr = [0.0368, 0.0265, 0.0243, 0.0264, 0.0278]
    ndcg = [0.0217, 0.014, 0.0132, 0.0137, 0.015]
    '''
    hr = np.array(hr)
    Clarity = np.array(Clarity)
    AA = np.array(AA)
    DA = np.array(DA)
    EF = np.array(EF)
    SE = np.array(SE)
    x1 = [0.7, 1.5, 2.3]
    x2 = [0.7, 1.5, 2.3]
    x3 = [0.7, 1.5, 2.3]
    x4 = [0.7, 1.5, 2.3]
    x5 = [0.7, 1.5, 2.3]
    x6 = [0.7, 1.5, 2.3]

    fig, ax1 = plt.subplots(dpi=600, figsize=(5, 3))
    fig.subplots_adjust(left=0.07, right=0.7, bottom=0.1, top=0.9)

    # plt.rcParams['axes.facecolor'] = 'white'
    xticks_label = ['turbo', 'plus', 'max']
    x = [0.7, 1.5, 2.3]
    ax1.set_xlim(0, 3)
    ax1.set_xticks(list(x)[::], xticks_label)
    ax1.set_xticklabels(xticks_label, fontweight='bold', fontsize=18)

    ax1.set_ylim(4.4, 5.1)
    ax1.set_xlabel(r'Judgment',
                   fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})
    ax1.patch.set_facecolor('white')
    plt.plot(x1, hr, "#0089ba", marker='^', markersize=7, linewidth=2, label='KR', zorder=3)

    ax1.spines['top'].set_visible(True)  # Top border
    ax1.spines['right'].set_visible(True)  # Right border
    ax1.spines['bottom'].set_visible(True)  # Bottom border
    ax1.spines['left'].set_visible(True)  # Left border

    # plt.axhline(y=0.055, color='gray', linestyle='--', linewidth=1, zorder=2)
    # plt.axhline(y=0.06, color='gray', linestyle='--', linewidth=1, zorder=2)
    # plt.axhline(y=0.03, color='gray', linestyle='--', linewidth=1, zorder=2)
    plt.axhline(y=0.03, color='gray', linestyle='--', linewidth=1, zorder=2)
    plt.axhline(y=0.035, color='gray', linestyle='--', linewidth=1, zorder=2)

    plt.plot(x2, Clarity, "#374955", marker='.', markersize=7, linewidth=2, label='Clarity', zorder=3)
    plt.plot(x3, AA, "#d0595a", marker='o', markersize=7, linewidth=2, label='AA', zorder=3)
    plt.plot(x4, DA, "#783864", marker='*', markersize=7, linewidth=2, label='DA', zorder=3)
    plt.plot(x5, EF, "#008572", marker='x', markersize=7, linewidth=2, label='EF', zorder=3)
    plt.plot(x6, SE, "#eb9929", marker='1', markersize=7, linewidth=2, label='SE', zorder=3)
    plt.legend(loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.02), frameon=False, fontsize=12)
    ax1.set_yticks([4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0,5.1])

    ax1.spines['top'].set_color('black')  # Top border
    ax1.spines['right'].set_color('black')  # Right border
    ax1.spines['bottom'].set_color('black')  # Bottom border
    ax1.spines['left'].set_color('black')  # Left border

    ax1.tick_params(axis='y', colors='#084C95')
    # 以下为添加的绘制垂直线代码
    for i in x:
        ax1.axvline(x=i, ymin=0, ymax=1, color='gray', linestyle='--', linewidth=1, zorder=2)
    plt.savefig('txtfile/judgment_Qwen_pre6.png', dpi=600, bbox_inches='tight')
    plt.show()
'''
if __name__ == '__main__':
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.rcParams['savefig.dpi'] = 600  # 图片像素
    plt.rcParams['figure.dpi'] = 600  # 分辨率
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.figure(figsize=(6, 4))
    # 数据
    x = ['1e^{-5}', '1e^{-4}', '5e^{-3}', '1e^{-2}', '1e^{-1}']
    # hr10
    y1 = [0.0333, 0.0309, 0.0285, 0.0261, 0.0271]
    y2 = [0.0209, 0.0044, 0.0033, 0.0032, 0.0032]
    y3 = [0.0076, 0.0079, 0.0062, 0.0062, 0.0061]

    # hr20
    y1 = [0.0473, 0.0438, 0.0413, 0.0345, 0.0386]
    y2 = [0.0311, 0.0056, 0.004, 0.0043, 0.004]
    y3 = [0.013, 0.0129, 0.0113, 0.0108, 0.0105]

    # ndcg10
    y1 = [0.0201, 0.0183, 0.017, 0.0154, 0.0155]
    y2 = [0.0112, 0.0025, 0.0021, 0.0019, 0.002]
    y3 = [0.0034, 0.004, 0.0028, 0.0029, 0.0029]

    # ndcg20
    y1 = [0.0236, 0.0215, 0.0202, 0.0175, 0.0183]
    y2 = [0.0138, 0.0028, 0.0023, 0.0022, 0.0022]
    y3 = [0.0048, 0.0052, 0.0041, 0.004, 0.004]
    '''    '''
    # 绘制三条折线，设置颜色和样式
    plt.plot(x, y1, label='CRGCN+D$^3$MBR', marker='o', color='#CC4242', linestyle='-')
    plt.plot(x, y2, label='CRGCN', marker='s', color='#1C84C3', linestyle='-')
    plt.plot(x, y3, label='DPT', marker='^', color='#4853A2', linestyle='-')

    # 设置标题和轴标签
    #plt.title('Three Lines in One Graph')
    plt.xlabel('Noise Ratio', fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})
    plt.ylabel('NDCG@20', fontdict={'family': 'Times New Roman', "weight": "bold", 'size': 18})
    plt.axhline(y=0.005, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.01, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.015, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.02, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.025, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.03, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.04, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.axhline(y=0.05, color='gray', linestyle='--', linewidth=1, zorder=1)
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_color('black')
        spine.set_linewidth(1)
    #for i in x:
        #ax.axvline(x=i, ymin=0, ymax=1, color='gray', linestyle='--', linewidth=1, zorder=1)
    plt.ylim(0, 0.03)
    plt.legend(loc='upper center', ncol=3, fontsize=12)
    plt.savefig('Noise Ratio_N20.png', dpi=600, bbox_inches='tight')
    # 显示图形
    plt.show()
'''
