import os
import random
import datetime
import subprocess
import base64
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter

# ==================== 配置 ====================
base_dir = r"D:\code\python\dj"
briefing_date = "2026-06-02"
stock_ticker = "0992.HK"
stock_name = "联想集团"
story_theme = "random"
party_rule_section = "general-program"

# 按日期创建输出目录
output_dir = os.path.join(base_dir, "file", briefing_date)
os.makedirs(output_dir, exist_ok=True)

html_path = os.path.join(output_dir, "card.html")
png_path = os.path.join(output_dir, "card.png")
chart_temp_path = os.path.join(output_dir, "_chart_temp.png")

# Chrome 路径（用于无头截图）
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ==================== 内容库 ====================
party_rules = {
    "general-program": {
        "title": "党章总纲摘录",
        "content": "中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，是中国特色社会主义事业的领导核心，代表中国先进生产力的发展要求，代表中国先进文化的前进方向，代表中国最广大人民的根本利益。党的最高理想和最终目标是实现共产主义。",
        "quote": "党的性质：两个先锋队、一个领导核心、三个代表"
    },
    "article-1": {
        "title": "党员的条件",
        "content": "年满十八岁的中国工人、农民、军人、知识分子和其他社会阶层的先进分子，承认党的纲领和章程，愿意参加党的一个组织并在其中积极工作、执行党的决议和按期交纳党费的，可以申请加入中国共产党。",
        "quote": "入党条件：年龄、承认、参加、执行、交纳"
    },
    "article-6": {
        "title": "入党誓词",
        "content": "预备党员必须面向党旗进行入党宣誓。誓词如下：我志愿加入中国共产党，拥护党的纲领，遵守党的章程，履行党员义务，执行党的决定，严守党的纪律，保守党的秘密，对党忠诚，积极工作，为共产主义奋斗终身，随时准备为党和人民牺牲一切，永不叛党。",
        "quote": "誓词核心：拥护、遵守、履行、执行、严守、保守、忠诚"
    }
}

stories = {
    "jiao-yulu": {
        "name": "焦裕禄",
        "title": "县委书记的榜样",
        "content": "1962年，焦裕禄调任河南兰考县委书记。面对内涝、风沙、盐碱三大灾害，他带领群众栽泡桐、固风沙，身患肝癌仍坚持工作，用棍子顶破肝部缓解疼痛。他常说：\"吃别人嚼过的馍没味道。\"1964年病逝，年仅42岁。临终前嘱咐：\"把我运回兰考，埋在沙堆上。活着我没有治好沙丘，死了也要看着你们把沙丘治好。\"",
        "quote": "精神内核：亲民爱民、艰苦奋斗、科学求实、迎难而上、无私奉献"
    },
    "lei-feng": {
        "name": "雷锋",
        "title": "全心全意为人民服务",
        "content": "雷锋，湖南望城人，1960年参军。他干一行爱一行，在平凡的岗位上做出不平凡的事迹。他省吃俭用，把积蓄捐给灾区；利用休息时间到工地帮忙、到车站服务。1962年因公殉职，年仅22岁。毛泽东题词：\"向雷锋同志学习。\"他的精神成为全心全意为人民服务的象征。",
        "quote": "精神内核：助人为乐、爱岗敬业、无私奉献、钉子精神"
    }
}

# ==================== 内容生成 ====================
# 党员必会
if party_rule_section == "random":
    rule_key = random.choice(list(party_rules.keys()))
else:
    rule_key = party_rule_section
rule_data = party_rules[rule_key]

# 党员故事
if story_theme == "random":
    story_key = random.choice(list(stories.keys()))
else:
    story_key = story_theme
story_data = stories[story_key]

# ==================== 股票数据（模拟近7个交易日）====================
stock_data = [
    {"date": "05-26", "open": 19.11, "high": 19.73, "low": 18.56, "close": 19.00, "volume": "3.59亿"},
    {"date": "05-27", "open": 19.00, "high": 19.78, "low": 18.75, "close": 19.68, "volume": "2.15亿"},
    {"date": "05-28", "open": 22.62, "high": 25.70, "low": 22.62, "close": 24.00, "volume": "7.22亿"},
    {"date": "05-29", "open": 24.50, "high": 26.10, "low": 24.20, "close": 25.50, "volume": "4.10亿"},
    {"date": "05-30", "open": 25.50, "high": 27.00, "low": 25.10, "close": 26.80, "volume": "3.50亿"},
    {"date": "06-01", "open": 25.96, "high": 27.42, "low": 25.68, "close": 26.38, "volume": "2.60亿"},
    {"date": "06-02", "open": 26.50, "high": 28.10, "low": 26.20, "close": 27.50, "volume": "3.20亿"},
]

# 计算关键指标
first_close = stock_data[0]["close"]
latest_close = stock_data[-1]["close"]
highest = max(d["high"] for d in stock_data)
change_pct = (latest_close - first_close) / first_close * 100
avg_volume = sum([float(d["volume"].replace("亿", "")) for d in stock_data]) / len(stock_data)

# ==================== 生成折线图 ====================
fig, ax = plt.subplots(figsize=(10, 5))

x = list(range(len(stock_data)))
dates = [d["date"] for d in stock_data]
closes = [d["close"] for d in stock_data]
highs = [d["high"] for d in stock_data]

# 绘制折线
ax.plot(x, closes, marker='o', linewidth=2.5, color='#E63946', markersize=8, markerfacecolor='white', markeredgewidth=2)
ax.fill_between(x, closes, alpha=0.15, color='#E63946')

# 标注价格
for i, d in enumerate(stock_data):
    ax.annotate(f'{d["close"]:.2f}', xy=(i, d["close"]), 
                xytext=(0, 14), textcoords='offset points', ha='center', fontweight='bold', fontsize=10, color='#333')

# 设置样式
ax.set_xticks(x)
ax.set_xticklabels(dates)
ax.set_ylabel('收盘价 (HKD)', fontsize=11)
ax.set_title(f'{stock_name} ({stock_ticker}) 近7日股价走势', fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 区间涨幅标注
ax.text(0.02, 0.95, f'区间涨幅: +{change_pct:.1f}%', transform=ax.transAxes, 
        fontsize=12, fontweight='bold', color='#E63946',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffeaa7', edgecolor='none', alpha=0.8),
        verticalalignment='top')

plt.tight_layout()
plt.savefig(chart_temp_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f"[OK] 股价走势图已生成: {chart_temp_path}")

# ==================== 生成 HTML ====================
# 将折线图 PNG 转为 base64 嵌入 HTML
with open(chart_temp_path, 'rb') as f:
    png_base64 = base64.b64encode(f.read()).decode('utf-8')

html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日党建简报</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 800px; margin: 0 auto; }}
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            padding: 20px;
        }}
        .header h1 {{ font-size: 2em; margin-bottom: 8px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }}
        .header .date {{ opacity: 0.9; font-size: 0.95em; }}
        .card {{
            background: white;
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            transition: transform 0.3s ease;
        }}
        .card:hover {{ transform: translateY(-4px); }}
        .card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 3px solid;
        }}
        .card-icon {{ font-size: 2em; margin-right: 12px; }}
        .card-title {{ font-size: 1.3em; font-weight: 700; }}
        .card-subtitle {{ font-size: 0.85em; color: #888; margin-left: auto; }}
        .card-body {{ line-height: 1.8; color: #333; font-size: 1.05em; }}
        .highlight {{
            background: linear-gradient(120deg, #ffeaa7 0%, #ffeaa7 100%);
            background-repeat: no-repeat;
            background-size: 100% 40%;
            background-position: 0 88%;
            padding: 0 4px;
            font-weight: 600;
        }}
        .quote {{
            border-left: 4px solid;
            padding-left: 16px;
            font-style: italic;
            color: #555;
            margin-top: 12px;
        }}
        .part1 .card-header {{ border-color: #e63946; }}
        .part1 .card-title {{ color: #e63946; }}
        .part1 .quote {{ border-color: #e63946; }}
        .part2 .card-header {{ border-color: #f4a261; }}
        .part2 .card-title {{ color: #f4a261; }}
        .part2 .quote {{ border-color: #f4a261; }}
        .part3 .card-header {{ border-color: #2a9d8f; }}
        .part3 .card-title {{ color: #2a9d8f; }}
        .part3 .quote {{ border-color: #2a9d8f; }}
        .chart-container {{ text-align: center; margin: 20px 0; }}
        .chart-container img {{
            max-width: 100%;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
            font-size: 0.9em;
        }}
        .data-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 8px;
            text-align: center;
        }}
        .data-table td {{
            padding: 10px 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }}
        .data-table tr:hover {{ background: #f8f9fa; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 12px;
            margin-top: 20px;
        }}
        .stat-item {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}
        .stat-value {{ font-size: 1.4em; font-weight: 700; color: #e63946; }}
        .stat-label {{ font-size: 0.8em; color: #888; margin-top: 4px; }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.7);
            font-size: 0.85em;
            margin-top: 30px;
            padding: 20px;
        }}
        .tag {{
            display: inline-block;
            background: #e63946;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            margin-right: 8px;
        }}
        .tag.green {{ background: #2a9d8f; }}
        .tag.blue {{ background: #457b9d; }}
        @media (max-width: 600px) {{
            body {{ padding: 12px; }}
            .card {{ padding: 20px; }}
            .header h1 {{ font-size: 1.5em; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 每日党建简报</h1>
            <div class="date">{briefing_date.replace('-', '年').replace('06', '6').replace('02', '2日')} | 星期二 | 来源：AI 自动生成</div>
        </div>

        <!-- Part 1: 党员必会 -->
        <div class="card part1">
            <div class="card-header">
                <span class="card-icon">💡</span>
                <span class="card-title">党员必会</span>
                <span class="card-subtitle">{rule_data['title']}</span>
            </div>
            <div class="card-body">
                <p>
                    <span class="tag">党章</span>
                    <span class="tag blue">{rule_data['title'].split('摘录')[0] if '摘录' in rule_data['title'] else rule_data['title']}</span>
                </p>
                <p style="margin-top: 12px;">
                    {rule_data['content'].replace('中国共产党', '<span class="highlight">中国共产党</span>', 1).replace('中国工人阶级的先锋队', '<span class="highlight">中国工人阶级的先锋队</span>').replace('中国先进生产力的发展要求', '<span class="highlight">中国先进生产力的发展要求</span>').replace('实现共产主义', '<span class="highlight">实现共产主义</span>')}
                </p>
                <div class="quote">
                    {rule_data['quote']}
                </div>
            </div>
        </div>

        <!-- Part 2: 党员故事 -->
        <div class="card part2">
            <div class="card-header">
                <span class="card-icon">📖</span>
                <span class="card-title">党员故事</span>
                <span class="card-subtitle">{story_data['name']}：{story_data['title']}</span>
            </div>
            <div class="card-body">
                <p>
                    <span class="tag">人物</span>
                    <span class="tag green">精神</span>
                </p>
                <p style="margin-top: 12px;">
                    {story_data['content'].replace('内涝、风沙、盐碱', '<span class="highlight">内涝、风沙、盐碱</span>').replace('吃别人嚼过的馍没味道', '<span class="highlight">吃别人嚼过的馍没味道</span>')}
                </p>
                <div class="quote">
                    {story_data['quote']}
                </div>
            </div>
        </div>

        <!-- Part 3: 市场动态 -->
        <div class="card part3">
            <div class="card-header">
                <span class="card-icon">📈</span>
                <span class="card-title">市场动态</span>
                <span class="card-subtitle">{stock_name} {stock_ticker}</span>
            </div>
            <div class="card-body">
                <p>
                    <span class="tag">港股</span>
                    <span class="tag green">近7日</span>
                </p>

                <div class="chart-container">
                    <img src="data:image/png;base64,{png_base64}" alt="股价走势图">
                </div>

                <table class="data-table">
                    <thead>
                        <tr>
                            <th>日期</th>
                            <th>开盘</th>
                            <th>最高</th>
                            <th>最低</th>
                            <th>收盘</th>
                            <th>成交量</th>
                        </tr>
                    </thead>
                    <tbody>
"""

# 生成表格行
for i, d in enumerate(stock_data):
    highlight = ' style="background: linear-gradient(120deg, #e8f5e9 0%, #e8f5e9 100%);"' if i == len(stock_data) - 1 else ''
    strong_close = f'<strong style="color:#e63946;">{d["close"]:.2f}</strong>' if i == len(stock_data) - 1 else f'<strong>{d["close"]:.2f}</strong>'
    html_template += f'                        <tr{highlight}><td><strong>{d["date"]}</strong></td><td>{d["open"]:.2f}</td><td>{d["high"]:.2f}</td><td>{d["low"]:.2f}</td><td>{strong_close}</td><td>{d["volume"]}</td></tr>\n'

html_template += f"""                    </tbody>
                </table>

                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">+{change_pct:.1f}%</div>
                        <div class="stat-label">区间涨幅</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{latest_close:.2f}</div>
                        <div class="stat-label">最新收盘价(HKD)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{highest:.2f}</div>
                        <div class="stat-label">最高触及(HKD)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{avg_volume:.2f}亿</div>
                        <div class="stat-label">日均成交量</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>📎 本简报由 AI 自动生成 | 数据截至 {briefing_date} 收盘</p>
            <p style="margin-top: 8px; font-size: 0.8em;">扫码分享本简报 ⬇️</p>
        </div>
    </div>
</body>
</html>"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"[OK] 简报 HTML 已生成: {html_path}")

# ==================== 用 Chrome 无头模式截图生成完整简报 PNG ====================
# 将 HTML 路径转为 file:// URL
html_file_url = "file:///" + html_path.replace("\\", "/")

cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    f"--screenshot={png_path}",
    "--window-size=900,2000",
    html_file_url
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if os.path.exists(png_path) and os.path.getsize(png_path) > 1000:
        print(f"[OK] 简报 PNG 已生成: {png_path}")
    else:
        print(f"[WARN] Chrome 截图可能失败，stdout: {result.stdout}, stderr: {result.stderr}")
except Exception as e:
    print(f"[ERROR] Chrome 截图失败: {e}")
    print(f"[INFO] 请确保 Chrome 已安装，路径: {CHROME_PATH}")

# 清理临时折线图文件
if os.path.exists(chart_temp_path):
    os.remove(chart_temp_path)
    print(f"[OK] 临时文件已清理: {chart_temp_path}")

print(f"[INFO] 输出目录: {output_dir}")
