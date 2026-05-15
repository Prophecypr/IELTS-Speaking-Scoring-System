# IELTS Speaking Scoring System

雅思口语练习与 AI 评分系统（纯前端单页应用）

## 功能

- 题库浏览：覆盖 Part 1/2/3，支持按话题、来源、关键词筛选
- 练习模式：选题 / 随机抽题 + 计时器 + 文本作答
- AI 评分：调用 DeepSeek API，返回 4 维评分（词汇/流利/语法/发音）+ 改进建议 + 示范答案
- 历史记录：localStorage 存储，支持筛选/删除
- 数据可视化：雷达图（单次）+ 折线趋势图 + 平均雷达图
- 导出：JSON / CSV / PDF 三种格式，支持题库和历史导入
- Part 3 单独练习：从 Part 2 的 P3 讨论题中抽取单独练习

## 技术栈

纯 HTML + Vanilla JS + Chart.js + jsPDF，无需服务器，浏览器直接打开即用。

## 使用方法

1. 用浏览器打开 `ielts-speaking.html`
2. 在左侧填写 DeepSeek API Key
3. 开始练习，提交后获取 AI 评分和反馈

## 题库格式

支持导入自定义题库（JSON 格式）：
```json
[
  {"id": 1, "part": 1, "topic": "Music", "text": "...", "questions": ["..."], "src": "大陆新题"},
  {"id": 101, "part": 2, "topic": "建筑", "text": "Describe...", "p3": ["..."], "src": "大陆新题"}
]
```

## 更新日志

见 `CHANGELOG.md`

## 双文件夹同步方案

工作路径：`E:\Vibe Coding\IELTS Speaking Scoring System\`（主开发文件夹）  
备份路径：`E:\prophecypr_project\github\IELTS Speaking Scoring System\`（备份 / 发布文件夹）  

每次更新后执行：
```bat
# 1. 提交并推送到 GitHub
cd "E:\Vibe Coding\IELTS Speaking Scoring System"
git add -A && git commit -m "描述本次更新"
git push

# 2. 同步到本地备份文件夹
copy "E:\Vibe Coding\IELTS Speaking Scoring System\ielts-speaking.html" "E:\prophecypr_project\github\IELTS Speaking Scoring System\"
copy "E:\Vibe Coding\IELTS Speaking Scoring System\README.md" "E:\prophecypr_project\github\IELTS Speaking Scoring System\"
copy "E:\Vibe Coding\IELTS Speaking Scoring System\CHANGELOG.md" "E:\prophecypr_project\github\IELTS Speaking Scoring System\"
```

Chicago.md` 每次更新后手动更新，记录本次变更。
