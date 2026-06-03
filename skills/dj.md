# Skill: 每日党建简报生成器

## 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | `daily-party-briefing` |
| **名称** | 每日党建简报生成器 |
| **版本** | v1.0.0 |
| **适用平台** | AG2 / Coze / Kimi / OpenSpec / 任意 LLM Agent |
| **输出格式** | Markdown + PNG 图表 |

---

## 功能描述

自动生成包含三个固定模块的每日党建简报：
1. **党员必会**：从党章截取核心段落（约100字）
2. **党员故事**：精选党员先进事迹（约100字）
3. **市场动态**：指定股票近7日走势折线图 + 数据表格

---

## 输入参数 (Inputs)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `stock_ticker` | string | 是 | `0992.HK` | 股票代码，支持港股/美股/A股格式 |
| `briefing_date` | string | 否 | 当天日期 | 简报日期，格式 `YYYY-MM-DD`。脚本运行时自动获取系统当前日期，无需手动指定。 |
| `story_theme` | string | 否 | `random` | 党员故事主题：`jiao-yulu`\|`lei-feng`\|`random` |
| `party_rule_section` | string | 否 | `general-program` | 党章章节：`general-program`\|`article-1`\|`random` |
| `output_style` | string | 否 | `standard` | 输出风格：`standard`\|`concise`\|`colorful` |

---

## 输出结构 (Outputs)

### Part 1: 党员必会
- **内容来源**：党章原文截取
- **字数限制**：80-120字
- **格式要求**：引用块标注出处，核心句加粗
- **可选章节**：
  - `general-program`：党的性质、先锋队、三个代表、最高理想
  - `article-1`：党员定义与入党条件
  - `article-6`：入党誓词

### Part 2: 党员故事
- **字数限制**：80-120字
- **叙事要求**：时间+地点+人物+事迹+精神提炼
- **可选人物**：
  - `jiao-yulu`：兰考治沙，"活着没治好沙丘，死了也要看着你们治好"
  - `lei-feng`：助人为乐，"把有限的生命投入到无限的为人民服务"
  - `random`：随机轮换，保证多样性

### Part 3: 市场动态
- **数据来源**：Yahoo Finance / 同花顺 / 东方财富
- **时间范围**：最近7个交易日
- **图表要求**：
  - 折线图，标注每日收盘价
  - 填充区域显示趋势
  - 每个数据点标注具体价格
  - 左上角显示区间涨跌幅
- **数据表格**：日期、开盘、最高、最低、收盘、成交量
- **关键指标**：区间涨幅、最新价、最高价、日均成交量

---

## 执行工作流 (Workflow)

```
┌─────────────────┐
│  接收输入参数   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌─────────┐
│Part 1 │ │ Part 2  │  ← 并行生成（纯文本）
│党章截取│ │党员故事 │
└───┬───┘ └────┬────┘
    │          │
    └────┬─────┘
         ▼
┌─────────────────┐
│  Part 3 数据获取 │
│  调用金融API获取 │
│  近7日股价数据   │
└────────┬────────┘
         ▼
┌─────────────────┐
│  生成折线图      │
│  matplotlib/echarts│
└────────┬────────┘
         ▼
┌─────────────────┐
│  组装Markdown   │
│  输出最终简报    │
└─────────────────┘
```

---

## Prompt 模板（可直接复制使用）

### System Prompt

```
你是一个党建简报生成助手。你的任务是根据用户提供的参数，生成一份包含三个部分的每日简报。

## 输出规范
1. 使用 Markdown 格式输出
2. 每个部分必须有明确的标题和分隔线
3. 第一部分和第二部分字数严格控制在80-120字之间
4. 第三部分必须包含数据表格和图表占位符

## 内容要求
- 党员必会：从党章原文截取，保持原文准确性，不得篡改
- 党员故事：选取真实历史人物，突出精神内核，语言简洁有力
- 市场动态：数据必须准确，图表使用 matplotlib 生成并保存为 PNG

## 格式模板

# 📋 每日简报
> 日期：{briefing_date} | 来源：自动生成

---

## 一、党员必会 💡
> **{章节标题}（约100字）**

{党章内容，80-120字}

---

## 二、党员故事 📖
> **{人物名称}：{事迹标题}**

{党员故事，80-120字}

---

## 三、市场动态 📈
### {股票名称}（{stock_ticker}）近7日股价走势

![股价走势图]({chart_filename})

| 日期 | 开盘价 | 最高价 | 最低价 | 收盘价 | 成交量 |
|------|--------|--------|--------|--------|--------|
{表格数据行}

**📊 关键数据**
- **区间涨幅**：{change}（{change_pct}）
- **最新收盘价**：{latest_close}
- **最高触及**：{highest}
- **成交活跃度**：{avg_volume}

---
*本简报由 AI 自动生成，数据截至 {latest_date} 收盘。*
```

### User Prompt 示例

```
生成今日党建简报：
- 股票代码：0992.HK（联想集团）
- 党员故事主题：焦裕禄
- 党章章节：总纲
- 日期：2026-06-02
```

---

## 工具调用配置

### 金融数据获取
```yaml
tool: yahoo_finance.get_historical_stock_prices
params:
  ticker: "{{stock_ticker}}"
  period: "1mo"
  interval: "1d"
  file_path: "/tmp/stock_{{stock_ticker}}.csv"
```

### 图片生成（完整 HTML 截图）

简报的图片不是单纯的折线图，而是**将完整的 HTML 页面渲染为 PNG 截图**，包含党员必会、党员故事、市场动态三个模块的全部内容。

#### 步骤 1：生成折线图（嵌入 HTML）
```python
import matplotlib.pyplot as plt
import pandas as pd
import base64

# 读取数据
df = pd.read_csv("/tmp/stock_{{stock_ticker}}.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
recent_7 = df.tail(7)

# 绘制折线图
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(recent_7['Date'], recent_7['Close'], marker='o', linewidth=2.5, color='#E63946')
ax.fill_between(recent_7['Date'], recent_7['Close'], alpha=0.15, color='#E63946')

# 标注价格
for _, row in recent_7.iterrows():
    ax.annotate(f'{row["Close"]:.2f}', xy=(row['Date'], row['Close']),
                xytext=(0, 12), textcoords='offset points', ha='center', fontweight='bold')

# 保存为临时文件
chart_temp = "/tmp/stock_chart_{{stock_ticker}}.png"
plt.savefig(chart_temp, dpi=150, bbox_inches='tight')
plt.close()

# 转为 base64 嵌入 HTML
with open(chart_temp, 'rb') as f:
    chart_base64 = base64.b64encode(f.read()).decode('utf-8')
```

#### 步骤 2：组装完整 HTML
将 Part 1、Part 2、Part 3 内容组装为带 CSS 样式的完整 HTML 文件，折线图以 `<img src="data:image/png;base64,...">` 形式内嵌。

#### 步骤 3：HTML 转 PNG（Chrome Headless 截图）
```python
import subprocess
import os

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = "/tmp/briefing.html"
png_path = "/tmp/briefing.png"

# 写入 HTML 文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

# Chrome 无头截图
cmd = [
    CHROME_PATH,
    "--headless", "--disable-gpu", "--no-sandbox",
    f"--screenshot={png_path}",
    "--window-size=900,2000",
    "file:///" + html_path.replace("\\", "/")
]
subprocess.run(cmd, timeout=60)

# 清理临时文件
os.remove(chart_temp)
```

#### 输出文件
| 文件 | 说明 |
|------|------|
| `card.html` | 完整简报网页（含 CSS + 内嵌图表） |
| `card.png` | **完整页面截图**，包含所有模块的渲染效果 |

---

## 内容库（内置素材）

### 党章素材库
```json
{
  "general-program": "中国共产党是中国工人阶级的先锋队，同时是中国人民和中华民族的先锋队，是中国特色社会主义事业的领导核心，代表中国先进生产力的发展要求，代表中国先进文化的前进方向，代表中国最广大人民的根本利益。党的最高理想和最终目标是实现共产主义。",
  "article-1": "年满十八岁的中国工人、农民、军人、知识分子和其他社会阶层的先进分子，承认党的纲领和章程，愿意参加党的一个组织并在其中积极工作、执行党的决议和按期交纳党费的，可以申请加入中国共产党。",
  "article-6": "预备党员必须面向党旗进行入党宣誓。誓词如下：我志愿加入中国共产党，拥护党的纲领，遵守党的章程，履行党员义务，执行党的决定，严守党的纪律，保守党的秘密，对党忠诚，积极工作，为共产主义奋斗终身，随时准备为党和人民牺牲一切，永不叛党。"
}
```

### 党员故事库
```json
{
  "jiao-yulu": "1962年，焦裕禄调任河南兰考县委书记。面对内涝、风沙、盐碱三大灾害，他带领群众栽泡桐、固风沙，身患肝癌仍坚持工作，用棍子顶破肝部缓解疼痛。他常说："吃别人嚼过的馍没味道。"1964年病逝，年仅42岁。临终前嘱咐："把我运回兰考，埋在沙堆上。活着我没有治好沙丘，死了也要看着你们把沙丘治好。"",
  "lei-feng": "雷锋，湖南望城人，1960年参军。他干一行爱一行，在平凡的岗位上做出不平凡的事迹。他省吃俭用，把积蓄捐给灾区；利用休息时间到工地帮忙、到车站服务。1962年因公殉职，年仅22岁。毛泽东题词："向雷锋同志学习。"他的精神成为全心全意为人民服务的象征。"
}
```


## 使用建议

1. **定时任务**：建议配置为每日早上8点自动执行
2. **多平台适配**：AG2 使用 `ConversableAgent` 封装，Coze 使用「工作流」节点编排
3. **数据源切换**：港股用 Yahoo Finance（后缀 .HK），A股用东方财富/同花顺接口
4. **内容轮换**：每周一自动轮换 `story_theme` 和 `party_rule_section`，保持新鲜感
