import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'
from datetime import datetime

# ===== 当前时间 =====
CURRENT_DATE = datetime(2026, 3, 1)

# ===== 生命周期阶段 =====
def get_stage(years):
    if years < 1:
        return "Introduction"
    elif years < 3:
        return "Growth"
    elif years < 6:
        return "Maturity"
    else:
        return "Decline"

# ===== 年数计算 =====
def calc_years(start_date):
    delta = CURRENT_DATE - start_date
    return round(delta.days / 365, 1)

# ===== 通用绘图函数 =====
def plot_brand(ax, data, brand_name):
    category_order = ["Sedan", "SUV", "EV Sedan", "EV SUV"]
    plot_data = []
    for cat in category_order:
        if cat in data:
            for name, date_str in data[cat].items():
                start = datetime.strptime(date_str, "%Y-%m")
                years = calc_years(start)
                stage = get_stage(years)
                plot_data.append((cat, name, years, stage))

    # 颜色
    stage_colors = {
        "Introduction": "#4CAF50",
        "Growth": "#2196F3",
        "Maturity": "#FFC107",
        "Decline": "#F44336"
    }

    y_labels = []
    y_pos = []
    values = []
    colors = []
    category_positions = {}
    current_y = 0

    for cat in category_order:
        if cat in data:
            cat_data = [item for item in plot_data if item[0] == cat]
            cat_data.sort(key=lambda x: x[2], reverse=True)
            category_positions[cat] = current_y + len(cat_data) / 2
            for item in cat_data:
                y_labels.append(f"{item[1]}")
                y_pos.append(current_y)
                values.append(item[2])
                colors.append(stage_colors[item[3]])
                current_y += 1
            current_y += 1  # 间隙

    ax.barh(y_pos, values, color=colors)

    # 数值标注
    for i, v in enumerate(values):
        ax.text(v + 0.1, y_pos[i], str(v), va='center', fontsize=8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.set_title(f"{brand_name} Lifecycle (Mar 2026)")

    # 生命周期分界线
    ax.axvline(1, linestyle='--', linewidth=0.8, color="#4CAF50")
    ax.axvline(3, linestyle='--', linewidth=0.8, color="#2196F3")
    ax.axvline(6, linestyle='--', linewidth=0.8, color="#FFC107")

    # 类别标签
    for cat, pos in category_positions.items():
        ax.text(-0.5, pos, cat, ha='right', va='center', fontsize=10, fontweight='bold')

    ax.invert_yaxis()

    # 生命周期阶段标签
    ax.text(0.2, -0.5, "Intro", ha='center', fontsize=10, color="#4CAF50", fontweight='bold')
    ax.text(1.5, -0.5, "Growth", ha='center', fontsize=10, color="#2196F3", fontweight='bold')
    ax.text(3.5, -0.5, "Maturity", ha='center', fontsize=10, color="#FFC107", fontweight='bold')
    ax.text(6.5, -0.5, "Decline", ha='center', fontsize=10, color="#F44336", fontweight='bold')


# ===== ===== 数据输入（你可以自己改） ===== =====

mercedes = {
    "Sedan": {
        "C-Class": "2021-02",
        "E-Class": "2023-06",
        "S-Class": "2020-09",
        "A-Class": "2018-03",
        "CLA": "2019-01"
    },
    "SUV": {
        "GLA": "2020-01",
        "GLC": "2022-06",
        "GLE": "2019-03",
        "GLS": "2019-04"
    },
    "EV Sedan": {
        "EQE": "2021-09",
        "EQS": "2021-04"
    },
    "EV SUV": {
        "EQC": "2019-05",
        "EQA": "2021-10",
        "EQB": "2022-03"
    }
}

audi = {
    "Sedan": {
        "A3": "2020-03",
        "A4": "2015-06",
        "A5": "2016-05",
        "A6": "2018-03",
        "A7": "2018-02",
        "A8": "2017-07"
    },
    "SUV": {
        "Q3": "2025-01",
        "Q5": "2017-09",
        "Q7": "2015-06",
        "Q8": "2018-06"
    },
    "EV Sedan": {
        "e-tron GT": "2021-02",
        "A6 e-tron": "2024-01"
    },
    "EV SUV": {
        "Q4 e-tron": "2021-04",
        "Q8 e-tron": "2019-03",
        "Q6 e-tron": "2023-10",
        "Q5 e-tron": "2022-09"
    }
}

bmw = {
    "Sedan": {
        "1 Series": "2019-05",
        "2 Series": "2021-07",
        "3 Series": "2018-10",
        "5 Series": "2023-05",
        "7 Series": "2022-04"
    },
    "SUV": {
        "X1": "2022-06",
        "X3": "2017-06",
        "X5": "2018-06",
        "X7": "2019-03"
    },
    "EV Sedan": {
        "i4": "2021-06",
        "i7": "2022-04"
    },
    "EV SUV": {
        "iX3": "2020-07",
        "iX": "2021-11",
        "iX1": "2022-11",
        "iX2": "2023-11"
    }
}



# ===== 绘制三图 =====
brands = [
    ("Mercedes-Benz", mercedes),
    ("Audi", audi),
    ("BMW", bmw)
]

for brand_name, data in brands:
    fig, ax = plt.subplots(figsize=(10, 8))
    plot_brand(ax, data, brand_name)
    ax.set_xlabel("Years since launch")
    plt.tight_layout()
    filename = f"{brand_name.lower().replace('-', '_').replace(' ', '_')}_lifecycle.png"
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close(fig)