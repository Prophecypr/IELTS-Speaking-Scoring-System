#!/usr/bin/env python3
import re

with open(r'E:\Vibe Coding\IELTS Speaking Scoring System\ielts-speaking.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. src 标签替换：大陆新题 → 5-8月新题，大陆老题 → 1-4月题目
content = content.replace('src:"大陆新题"', 'src:"5-8月新题"')
content = content.replace('value="大陆新题">大陆新题<', 'value="5-8月新题">5-8月新题<')
content = content.replace('"大陆新题"', '"5-8月新题"')  # srcBadgeClass 比较
content = content.replace('大陆新题 + 老题沿用', '5-8月新题 + 1-4月题目沿用')

content = content.replace('src:"大陆老题"', 'src:"1-4月题目"')
content = content.replace('value="大陆老题">大陆老题<', 'value="1-4月题目">1-4月题目<')
content = content.replace('"大陆老题"', '"1-4月题目"')

content = content.replace('src:"非大陆新题"', 'src:"非大陆新题"')  # 保持不变
content = content.replace('src:"万年老题"', 'src:"万年老题"')    # 保持不变

# 2. 删除"全部话题"选项（topic 下拉菜单里的第一个 <option>）
# pracTopic
content = content.replace(
    '<option value="">全部话题</option>\n        <select id="pracSrc"',
    '<select id="pracSrc"'
)
# qTopic - 需要在 renderQuestions 区域找
# 实际上"全部话题"是由 JS 动态生成的，需要在 updateTopicDropdown 里改
# 把 '<option value="">全部话题</option>' 改成空（即不添加默认全部选项）
# 这个在 updateTopicDropdown 函数里，我们稍后在 JS 里处理

# 3. P1 朗读时跳过 topic（speakQuestion 函数）
old_speak = '''function speakQuestion() {
  const q = state.selectedQuestion;
  if (!q) return;
  window.speechSynthesis.cancel();
  let text = '';
  if (q.part === 1 && q.questions) {
    text = q.topic + '. ' + q.questions.join(' ');
  } else if (q.part === 2) {
    text = q.text.replace(/\\n/g, '. ');
  } else {
    text = q.text;
  }
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-GB';
  utter.rate = 0.88;
  utter.pitch = 1.0;
  const voices = window.speechSynthesis.getVoices();
  const gbVoice = voices.find(v => v.lang && v.lang.startsWith('en-GB'));
  if (gbVoice) utter.voice = gbVoice;
  window.speechSynthesis.speak(utter);
}'''

new_speak = '''function speakQuestion() {
  const q = state.selectedQuestion;
  if (!q) return;
  window.speechSynthesis.cancel();
  let text = '';
  if (q.part === 1 && q.questions) {
    text = q.questions.join(' ');
  } else if (q.part === 2) {
    text = q.text.replace(/\\n/g, '. ');
  } else {
    text = q.text;
  }
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-GB';
  utter.rate = 0.88;
  utter.pitch = 1.0;
  const voices = window.speechSynthesis.getVoices();
  const gbVoice = voices.find(v => v.lang && v.lang.startsWith('en-GB'));
  if (gbVoice) utter.voice = gbVoice;
  window.speechSynthesis.speak(utter);
}

// P1 逐题回答模式相关状态
state.p1GuideIndex = -1;
state.p1GuideQuestions = [];

function startP1Guide() {
  const q = state.selectedQuestion;
  if (!q || q.part !== 1 || !q.questions) return;
  state.p1GuideQuestions = q.questions;
  state.p1GuideIndex = 0;
  showP1GuideQuestion();
}
function showP1GuideQuestion() {
  const qi = state.p1GuideIndex;
  const qs = state.p1GuideQuestions;
  if (qi >= qs.length) {
    document.getElementById('p1GuideArea').style.display = 'none';
    document.getElementById('answerInput').value = '';
    alert('所有小问已回答完毕！');
    return;
  }
  const html = `<div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">第 ${qi+1}/${qs.length} 题</div>
    <div style="font-size:18px;font-weight:600;margin-bottom:12px">${qs[qi]}</div>
    <button class="btn-primary btn-sm" onclick="submitP1GuideAnswer()">提交此题答案，下一题 →</button>`;
  document.getElementById('p1GuideArea').innerHTML = html;
  document.getElementById('p1GuideArea').style.display = 'block';
  document.getElementById('answerInput').value = '';
  document.getElementById('answerInput').focus();
}
function submitP1GuideAnswer() {
  state.p1GuideIndex++;
  showP1GuideQuestion();
}

// 语音输入
let recognition = null;
function toggleSpeechInput() {
  const input = document.getElementById('answerInput');
  if (recognition && recognition.active) {
    recognition.stop();
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { alert('你的浏览器不支持语音识别，请使用 Chrome'); return; }
  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.onresult = (e) => {
    const transcript = e.results[0][0].transcript;
    input.value += (input.value ? ' ' : '') + transcript;
  };
  recognition.onend = () => {
    document.getElementById('speechInputBtn').textContent = '🎤 语音输入';
  };
  recognition.onerror = (e) => {
    document.getElementById('speechInputBtn').textContent = '🎤 语音输入';
  };
  recognition.start();
  document.getElementById('speechInputBtn').textContent = '⏹ 停止录音';
}'''

if old_speak in content:
    content = content.replace(old_speak, new_speak)
    print("Replaced speakQuestion + added guide/speech")
else:
    print("WARNING: speakQuestion pattern not found, trying alternative...")
    # Try to find it with regex
    if 'function speakQuestion()' in content:
        print("  speakQuestion function exists but pattern mismatch")

# 4. updateTopicDropdown：不添加"全部话题"选项
old_utd = '''function updateTopicDropdown(part, selId) {
  const sel = document.getElementById(selId);
  const currentValue = sel.value;
  let topics = [];
  if (!part) {
    topics = [...new Set(QUESTIONS.map(q => q.topic))].sort();
  } else if (part === '3') {
    topics = [...new Set(QUESTIONS.filter(q => q.part === 2 && q.p3).map(q => q.topic))].sort();
  } else {
    topics = [...new Set(QUESTIONS.filter(q => String(q.part) === part).map(q => q.topic))].sort();
  }
  sel.innerHTML = '<option value="">全部话题</option>';
  topics.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t; opt.textContent = t;
    sel.appendChild(opt);
  });
  if (topics.includes(currentValue)) sel.value = currentValue;
  else sel.value = '';
}'''

new_utd = '''function updateTopicDropdown(part, selId) {
  const sel = document.getElementById(selId);
  const currentValue = sel.value;
  let topics = [];
  if (!part) {
    topics = [...new Set(QUESTIONS.map(q => q.topic))].sort();
  } else if (part === '3') {
    topics = [...new Set(QUESTIONS.filter(q => q.part === 2 && q.p3).map(q => q.topic))].sort();
  } else {
    topics = [...new Set(QUESTIONS.filter(q => String(q.part) === part).map(q => q.topic))].sort();
  }
  sel.innerHTML = '';
  topics.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t; opt.textContent = t;
    sel.appendChild(opt);
  });
  if (topics.includes(currentValue)) sel.value = currentValue;
  else sel.value = '';
}'''

if old_utd in content:
    content = content.replace(old_utd, new_utd)
    print("Removed '全部话题' from topic dropdowns")
else:
    print("WARNING: updateTopicDropdown pattern not found")

# 5. P2 回答区：左对齐 + 题目同大小粗细
# 找到 selectQuestion 中 P2 的 HTML 生成部分
old_p2_html = '''  if (q.part === 2) {
    // Cue card format
    const lines = q.text.split('\\n');
    questionHTML = `<div style="font-size:13px;color:var(--text-muted);margin-bottom:4px">${q.topic}</div>`;
    questionHTML += `<div style="font-size:20px;font-weight:600;margin-bottom:10px">${lines[0]}</div>`;
    if (lines.length > 1) {
      questionHTML += `<div style="font-size:13px;color:var(--text-muted);line-height:2;background:var(--bg);padding:10px 14px;border-radius:var(--radius-sm);border-left:3px solid var(--amber)">`;
      questionHTML += lines.slice(1).map(l => l.trim() ? l : '').filter(Boolean).join('<br>');
      questionHTML += '</div>';
    }
    // P3 questions
    if (q.p3 && q.p3.length) {
      questionHTML += `<details style="margin-top:12px"><summary style="cursor:pointer;font-size:12px;color:var(--blue);font-weight:500">Part 3 讨论题 (${q.p3.length})</summary><ul style="margin-top:8px;padding-left:16px;font-size:12px;color:var(--text-muted);line-height:2">${q.p3.map(s=>`<li>${s}</li>`).join('')}</ul></details>`;
    }
  }'''

new_p2_html = '''  if (q.part === 2) {
    // Cue card format - left aligned, title same size as questions
    const lines = q.text.split('\\n');
    questionHTML = `<div style="text-align:left;font-size:13px;color:var(--text-muted);margin-bottom:4px">${q.topic}</div>`;
    questionHTML += `<div style="text-align:left;font-size:20px;font-weight:600;margin-bottom:10px">${lines[0]}</div>`;
    if (lines.length > 1) {
      questionHTML += `<div style="text-align:left;font-size:20px;font-weight:600;line-height:2;background:var(--bg);padding:10px 14px;border-radius:var(--radius-sm);border-left:3px solid var(--amber)">`;
      questionHTML += lines.slice(1).map(l => l.trim() ? l : '').filter(Boolean).join('<br>');
      questionHTML += '</div>';
    }
    // P3 questions
    if (q.p3 && q.p3.length) {
      questionHTML += `<details style="margin-top:12px;text-align:left"><summary style="cursor:pointer;font-size:12px;color:var(--blue);font-weight:500">Part 3 讨论题 (${q.p3.length})</summary><ul style="margin-top:8px;padding-left:16px;font-size:12px;color:var(--text-muted);line-height:2">${q.p3.map(s=>`<li>${s}</li>`).join('')}</ul></details>`;
    }
  }'''

if old_p2_html in content:
    content = content.replace(old_p2_html, new_p2_html)
    print("Updated P2 display: left align, uniform title size")
else:
    print("WARNING: P2 HTML pattern not found")

# 6. .practice-q 移除居中（P2 左对齐需要）
content = content.replace(
    '  .practice-q { font-size: 16px; font-weight: 500; margin-bottom: 12px; line-height: 1.5; text-align: center; }',
    '  .practice-q { font-size: 16px; font-weight: 500; margin-bottom: 12px; line-height: 1.5; }'
)
print("Removed text-align:center from .practice-q")

# 7. 添加 P1 逐题回答区 HTML（在 answerArea 里）
old_answer_area = '''      <textarea id="answerInput" placeholder="在这里输入你的答案..." rows="6"></textarea>
      <div style="margin-top:12px" class="btn-row">
        <button class="btn-primary" onclick="submitAnswer()">✓ 提交并评分</button>
        <button onclick="clearAnswer()">清空</button>
      </div>'''

new_answer_area = '''      <div id="p1GuideArea" style="display:none;margin-bottom:12px;padding:12px;background:var(--blue-bg);border-radius:var(--radius-sm)"></div>
      <textarea id="answerInput" placeholder="在这里输入你的答案..." rows="6"></textarea>
      <div style="margin-top:12px" class="btn-row">
        <button class="btn-primary" onclick="submitAnswer()">✓ 提交并评分</button>
        <button onclick="clearAnswer()">清空</button>
        <button class="btn-sm" id="speechInputBtn" onclick="toggleSpeechInput()">🎤 语音输入</button>
        <button class="btn-sm" onclick="startP1Guide()" id="p1GuideBtn" style="display:none">📝 逐题回答模式</button>
      </div>'''

if old_answer_area in content:
    content = content.replace(old_answer_area, new_answer_area)
    print("Added P1 guide area + speech input button to answer area")
else:
    print("WARNING: answer area pattern not found")

# 8. 显示/隐藏逐题回答按钮（在 selectQuestion 里）
# 在 selectQuestion 末尾添加逻辑：P1 且有 questions 时显示逐题按钮
old_end_select = '''  document.getElementById('answerInput').focus();
  document.getElementById('answerArea').scrollIntoView({behavior:'smooth'});
}'''

new_end_select = '''  // Show/hide P1 guide button
  if (q.part === 1 && q.questions && q.questions.length > 1) {
    document.getElementById('p1GuideBtn').style.display = '';
  } else {
    document.getElementById('p1GuideBtn').style.display = 'none';
    document.getElementById('p1GuideArea').style.display = 'none';
  }
  document.getElementById('answerInput').focus();
  document.getElementById('answerArea').scrollIntoView({behavior:'smooth'});
}'''

if old_end_select in content:
    content = content.replace(old_end_select, new_end_select)
    print("Added P1 guide button show/hide logic")
else:
    print("WARNING: selectQuestion end pattern not found")

# 9. 导入按钮移到导出页面左边 + 更详细的格式说明
old_export = '''    <div class="card">
      <h3>导入题库</h3>
      <p style="font-size:12px;color:var(--text-muted);margin-bottom:12px">导入自定义题库（格式：[{"id":..., "part":1, "topic":"...", "text":"...", "questions":[...], "src":"..."}]）。导入后题库将合并到现有题目中。</p>
      <input type="file" accept=".json" onchange="importQuestionBank(event)" style="font-size:13px" />
    </div>'''

new_export = '''    <div class="card">
      <h3>导入题库</h3>
      <p style="font-size:12px;color:var(--text-muted);margin-bottom:12px">
        支持导入自定义题库 JSON 文件，导入后题目将合并到现有题库中（相同 id 的题目不会被重复导入）。<br><br>
        <strong>JSON 格式说明：</strong><br>
        • 数组格式：直接是一个数组 <code>[...]</code><br>
        • 对象格式：<code>{"questions": [...]}</code><br><br>
        <strong>单题格式：</strong><br>
        • <code>id</code>：唯一编号（数字，不可重复）<br>
        • <code>part</code>：1、2 或 3<br>
        • <code>topic</code>：话题名称（如 "Music"）<br>
        • <code>src</code>：来源标签（如 "5-8月新题"、"1-4月题目"）<br>
        • <code>text</code>：题目文本（Part 2 用 \\n 分隔各部分）<br>
        • <code>questions</code>：数组，Part 1 的各小问（可选）<br>
        • <code>p3</code>：数组，Part 2 对应的 Part 3 讨论题（可选）
      </p>
      <input type="file" accept=".json" onchange="importQuestionBank(event)" style="font-size:13px" />
    </div>'''

if old_export in content:
    content = content.replace(old_export, new_export)
    print("Updated import section with detailed format description")
else:
    print("WARNING: export/import pattern not found, searching...")
    if '导入题库' in content:
        print("  '导入题库' found but HTML structure differs")

with open(r'E:\Vibe Coding\IELTS Speaking Scoring System\ielts-speaking.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! All replacements complete.")
