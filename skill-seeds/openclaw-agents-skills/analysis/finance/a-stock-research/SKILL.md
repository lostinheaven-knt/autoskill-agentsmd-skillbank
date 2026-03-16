# A股股票基本面与消息面研究

查询A股股票基本面和消息面的工作流指南。

## 优先级

1. **数据指标**：a-stock-analysis > tushare > agent-browser东财
2. **基本面和消息面**：agent-browser东财 > agent-browser Google > web_fetch

## 数据指标查询

使用 a-stock-analysis（新浪接口，最快）：
```bash
python ~/.openclaw/workspace/.agents/skills/a-stock-analysis-1.0.0/scripts/analyze.py 600021 000989
```

## 基本面/消息面查询（东财）

### 页面URL格式
- 操盘必读：`https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZxxxxxx`（深市）
- 操盘必读：`https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SHxxxxxx`（沪市）

### 查询命令
```bash
# 打开页面，等待7秒加载
agent-browser open "https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SH600021"
agent-browser wait 7000

# 获取关键信息
agent-browser get text body | grep -E "总市值|净资产|净利润|市盈率|毛利率|ROE|股东人数|所属板块|股权质押|大宗交易"
```

### 提取关键指标
从页面提取以下信息：
- 总市值、净资产、净利润
- 市盈率、毛利率、ROE
- 股东人数、筹码集中度
- 所属板块、核心题材
- 大宗交易、股权质押
- 近期重大事项（并购、减持、解质押等）

## 输出格式

整理为表格：
| 指标 | 数值 |
|------|------|
| 总市值 | xx亿 |
| 净资产 | xx亿 |
| 净利润 | x.x亿 |
| 市盈率 | xx.xx |
| 毛利率 | xx% |
| ROE | xx% |
| 股东人数 | x.xx万 |

消息面要点：
- 近期重大事项列表
- 所属板块和概念
- 大宗交易/股权质押情况

## 示例输出

**600021 上海电力：**

| 指标 | 数值 |
|------|------|
| 总市值 | 约570亿 |
| 净资产 | 211亿 |
| 净利润 | 30.50亿（盈利！） |
| 市盈率 | 14.22 |
| 毛利率 | 27.65% |
| ROE | 13.91% |
| 股东人数 | 18.95万 |

**消息面：**
- ✅ 2025年业绩预增：25.11-29.88亿
- 🆕 新增概念：油气资源
- 📈 融资余额：16.14亿
- 🔧 总经理变更

---

## 注意事项
- 每页面查询后等待7秒，避免被封
- 深市代码前缀SZ，沪市代码前缀SH
- ST股票注意风险提示