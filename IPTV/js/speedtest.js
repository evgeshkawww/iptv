import { startMassTest } from './allservers.js';

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

function detectSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function toggleTheme() {
  const current = localStorage.getItem('theme') || detectSystemTheme();
  const next = current === 'light' ? 'dark' : 'light';
  applyTheme(next);
  document.getElementById('themeToggle').textContent = next === 'dark' ? '?? День' : '?? Ночь';
}

window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme') || detectSystemTheme();
  applyTheme(savedTheme);

  const themeBtn = document.createElement('button');
  themeBtn.id = 'themeToggle';
  themeBtn.textContent = savedTheme === 'dark' ? '?? День' : '?? Ночь';
  themeBtn.onclick = toggleTheme;
  document.body.appendChild(themeBtn);

  const s = new Speedtest();
  window.speedtestInstance = s;

  s.addTestPoints(window.SPEEDTEST_SERVERS);
  s.selectServer(() => console.log("Сервер выбран:", s.getSelectedServer().name));

  s.onupdate = data => {
    document.getElementById("results").innerHTML = `
      <p>Ping: ${data.pingStatus} ms</p>
      <p>Jitter: ${data.jitterStatus} ms</p>
      <p>Download: ${data.dlStatus} Mbps</p>
      <p>Upload: ${data.ulStatus} Mbps</p>
    `;
  };

  s.onend = aborted => {
    console.log("Одиночный тест завершён", aborted ? "прерван" : "успешно");
  };

  document.getElementById("startStopBtn").onclick = () => {
    if (s.getState() === 3) {
      s.abort();
    } else {
      s.start();
    }
  };

  document.getElementById("multiTestBtn").onclick = () => {
    startMassTest();
  };
});
