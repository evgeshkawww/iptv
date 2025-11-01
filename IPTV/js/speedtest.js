window.addEventListener('DOMContentLoaded', () => {
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
    import('./allservers.js').then(mod => mod.startMassTest());
  };
});
