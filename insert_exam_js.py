#!/usr/bin/env python3
import re

with open(r'E:\Vibe Coding\IELTS Speaking Scoring System\ielts-speaking.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Exam mode state
exam_js = '''
// ============================================================
// EXAM MODE
// ============================================================
const examState = {
  phase: '',      // 'P1', 'P2', 'P3'
  p1Questions: [],  // array of P1 question objects
  p1Index: 0,
  p2Question: null,
  p3Questions: [],
  p3Index: 0,
  timerSeconds: 0,
  timerRunning: false,
  timerInterval: null,
};

function startExam() {
  // Randomly pick: 5 P1 questions, 1 P2 question (with its P3)
  const p1Pool = QUESTIONS.filter(q => q.part === 1);
  const p2Pool = QUESTIONS.filter(q => q.part === 2);
  shuffleArray(p1Pool);
  shuffleArray(p2Pool);

  examState.p1Questions = p1Pool.slice(0, 5);
  examState.p1Index = 0;
  examState.p2Question = p2Pool[0] || null;
  examState.p3Questions = examState.p2Question && examState.p2Question.p3
    ? examState.p2Question.p3.map((t, i) => ({
        id: 'exam_p3_' + i, part: 3, text: t, topic: examState.p2Question.topic
      }))
    : [];
  examState.p3Index = 0;

  examState.phase = 'P1';
  examState.timerSeconds = 0;
  examState.timerRunning = false;

  document.getElementById('examStartCard').style.display = 'none';
  document.getElementById('examProgressCard').style.display = 'block';
  document.getElementById('examResultCard').style.display = 'none';
  document.getElementById('examAnswerInput').value = '';
  document.getElementById('examP2Card').style.display = 'none';

  showExamQuestion();
}

function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
}

function showExamQuestion() {
  stopExamTimer();
  document.getElementById('examTimerBtn').textContent = '开始计时';
  document.getElementById('examActionBtn').textContent = '完成此题，下一题 →';

  if (examState.phase === 'P1') {
    const q = examState.p1Questions[examState.p1Index];
    document.getElementById('examPhase').textContent = 'Part 1 — 第 ' + (examState.p1Index + 1) + '/5 题';
    document.getElementById('examProgress').textContent = '雅思口语模拟考试';
    let html = `<div style="font-size:18px;font-weight:600;margin-bottom:8px">${q.topic}</div>`;
    if (q.questions && q.questions.length) {
      html += `<div style="font-size:14px;color:var(--text-muted);line-height:2">${q.questions.map((s,i) => '<div style="' + (i === 0 ? 'font-weight:600;color:var(--text)' : '') + '">• ' + s + '</div>').join('')}</div>`;
    }
    document.getElementById('examQuestionArea').innerHTML = html;
    document.getElementById('examP2Card').style.display = 'none';
    // Timer hint
    examState.timerSeconds = 0;
    updateExamTimerDisplay();
  } else if (examState.phase === 'P2') {
    const q = examState.p2Question;
    examState.timerSeconds = 0;
    updateExamTimerDisplay();
    document.getElementById('examPhase').textContent = 'Part 2 — Cue Card';
    document.getElementById('examProgress').textContent = '建议 2 分钟，请独自连续作答';
    let html = `<div style="font-size:20px;font-weight:600;margin-bottom:10px">${q.text.split('\\n')[0]}</div>`;
    document.getElementById('examQuestionArea').innerHTML = html;
    document.getElementById('examP2Card').style.display = 'block';
    document.getElementById('examP2Card').innerHTML = q.text.split('\\n').slice(1).map(l => l.trim() ? l : '').filter(Boolean).join('<br>');
  } else if (examState.phase === 'P3') {
    const q = examState.p3Questions[examState.p3Index];
    document.getElementById('examPhase').textContent = 'Part 3 — 第 ' + (examState.p3Index + 1) + '/' + examState.p3Questions.length + ' 题';
    document.getElementById('examProgress').textContent = '讨论题 · 来源话题：' + q.topic;
    document.getElementById('examQuestionArea').innerHTML = `<div style="font-size:18px;font-weight:600">${q.text}</div>`;
    document.getElementById('examP2Card').style.display = 'none';
    examState.timerSeconds = 0;
    updateExamTimerDisplay();
  }
  document.getElementById('examAnswerInput').value = '';
  document.getElementById('examAnswerInput').focus();
}

function examAction() {
  if (examState.phase === 'P1') {
    examState.p1Index++;
    if (examState.p1Index >= examState.p1Questions.length) {
      // Move to P2
      examState.phase = 'P2';
      showExamQuestion();
    } else {
      showExamQuestion();
    }
  } else if (examState.phase === 'P2') {
    // Move to P3
    examState.phase = 'P3';
    showExamQuestion();
  } else if (examState.phase === 'P3') {
    examState.p3Index++;
    if (examState.p3Index >= examState.p3Questions.length) {
      // Exam finished
      finishExam();
    } else {
      showExamQuestion();
    }
  }
}

function finishExam() {
  stopExamTimer();
  document.getElementById('examProgressCard').style.display = 'none';
  document.getElementById('examResultCard').style.display = 'block';
}

function toggleExamTimer() {
  if (examState.timerRunning) {
    stopExamTimer();
    document.getElementById('examTimerBtn').textContent = '继续计时';
  } else {
    examState.timerRunning = true;
    examState.timerInterval = setInterval(() => {
      examState.timerSeconds++;
      updateExamTimerDisplay();
    }, 1000);
    document.getElementById('examTimerBtn').textContent = '暂停';
  }
}
function stopExamTimer() {
  examState.timerRunning = false;
  if (examState.timerInterval) { clearInterval(examState.timerInterval); examState.timerInterval = null; }
}
function updateExamTimerDisplay() {
  const m = Math.floor(examState.timerSeconds / 60);
  const s = examState.timerSeconds % 60;
  document.getElementById('examTimer').textContent =
    String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
}

function speakExamQuestion() {
  let text = '';
  if (examState.phase === 'P1') {
    const q = examState.p1Questions[examState.p1Index];
    text = q.questions ? q.questions.join(' ') : q.text;
  } else if (examState.phase === 'P2') {
    text = examState.p2Question ? examState.p2Question.text.replace(/\\n/g, '. ') : '';
  } else if (examState.phase === 'P3') {
    const q = examState.p3Questions[examState.p3Index];
    text = q ? q.text : '';
  }
  if (!text) return;
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = 'en-GB';
  utter.rate = 0.88;
  const voices = window.speechSynthesis.getVoices();
  const gbVoice = voices.find(v => v.lang && v.lang.startsWith('en-GB'));
  if (gbVoice) utter.voice = gbVoice;
  window.speechSynthesis.speak(utter);
}
'''

# Insert before the last </script> tag (the main script block closing tag)
# Find the position of the last </script> that is at the end of the file
# We need to insert before: the closing </script> of the main script block
# The pattern is: ... </script>  (line 1839)

# Insert the exam JS before the closing </script> of the main block
# The main JS block starts with <script> after </head> and ends with </script> before </body>
# Actually the file has 2 script tags: one for chart.js, one for jspdf, then the main inline script
# The main inline script ends at line 1839 with </script>
# We need to insert before that </script>

insert_marker = '</script>\n</body>\n</html>'
if insert_marker in content:
    content = content.replace(insert_marker, exam_js + '\n  </script>\n</body>\n</html>')
    print("Inserted exam mode JS before closing </script>")
else:
    print("WARNING: insert_marker not found, trying alternative...")
    # Try to find just </script> before </body>
    if '</script>\n</body>' in content:
        content = content.replace('</script>\n</body>', exam_js + '\n  </script>\n</body>')
        print("Inserted exam JS (alt method)")
    else:
        print("ERROR: Could not find insertion point")

with open(r'E:\Vibe Coding\IELTS Speaking Scoring System\ielts-speaking.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Exam mode JS added successfully!")
