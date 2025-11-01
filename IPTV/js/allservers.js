export function startMassTest() {
  const s = window.speedtestInstance;
  const servers = window.SPEEDTEST_SERVERS;
  let currentServer = 0;

  const container = document.getElementById("results");
  container.innerHTML = `
    <table id="multi_results">
      <thead>
        <tr>
          <th>Сервер</th>
          <th>Статус</th>
          <th>Jitter, ms</th>
          <th>Download, Mbps</th>
          <th>Оценка</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  `;

  function appendResult(server, serveropen, dl, ping, jitter) {
    let statusIcon;
    if (jitter < 3 && dl > 100) statusIcon = '⚡⚡⚡';
    else if (jitter < 5 && dl > 50) statusIcon = '⚡⚡';
    else if (jitter < 10 && dl > 30) statusIcon = '⚡';
    else statusIcon = '☠️';

    const isOpen = serveropen === "YES" ? "Доступен ✅" : "Заполнен 🔒";
    const row = `<tr><td>${server}</td><td>${isOpen}</td><td>${jitter}</td><td>${dl}</td><td>${statusIcon}</td></tr>`;
    document.querySelector("#multi_results tbody").innerHTML += row;
  }

  function testNext() {
    if (currentServer >= servers.length) return;

    while (servers[currentServer].pingT === -1 && currentServer < servers.length) {
      currentServer++;
    }

    if (currentServer >= servers.length) return;

    s.setSelectedServer(servers[currentServer]);
    s.onupdate = () => {};
    s.onend = aborted => {
      if (!aborted) {
        appendResult(
          servers[currentServer].name,
          servers[currentServer].serveropen,
          s.dlStatus,
          s.pingStatus,
          s.jitterStatus
        );
      }
      currentServer++;
      testNext();
    };
    s.start();
  }

  testNext();
}
