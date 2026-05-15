# Changelog

## [Unreleased]

### Added
- Part 3 单独练习支持：练习页筛选器新增 Part 3 选项，从 Part 2 的 P3 讨论题中单独抽题
- 题库数量显示：随机抽题按钮右侧实时显示当前条件下有多少题
- 题库导入功能：导出页面新增"导入题库 JSON"，支持用户自定义题库合并
- GitHub 仓库同步：`git@github.com:Prophecypr/IELTS-Speaking-Scoring-System.git`
- 双文件夹同步：`E:\Vibe Coding\IELTS Speaking Scoring System` ↔ `E:\prophecypr_project\github\IELTS Speaking Scoring System`

### Changed
- P1 题目显示：移除了话题标签（如"Music"），直接显示第一道题目文本
- P2 题目显示：卡片标题改为中文话题（如"建筑"），取代英文"Describe..."
- AI 评分 Prompt：新增 Part 3 类型描述（Discussion questions）

### Fixed
- （无）

---

## [2026-05-15] - 初始版本

### Added
- 完整雅思口语练习单页应用
- 题库：89 道题（Part 1 × 42 + Part 2 × 47），含来源标签（大陆新题/老题/非大陆新题/万年老题）
- AI 评分：DeepSeek API 评分，返回 4 维分数 + 改进建议 + 示范答案
- 练习历史：localStorage 持久化，支持筛选/删除/导出
- 数据可视化：Chart.js 雷达图 + 折线趋势图
- 导出功能：JSON / CSV / PDF 三种格式
- 答题模板：Part 1/2/3 模板 + 万能短语库
