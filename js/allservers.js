var uiData=null;

document.getElementById("test").innerHTML +=
            '<table id="multi_results"><tbody></tbody></table>';

// Get the current date and time
let currentDateTime = new Date().toLocaleString();

// Insert the date and time before the table
document.getElementById("test").innerHTML += 
    '<p>Generated on: ' + currentDateTime + '</p>' +
        '<table id="multi_results"><tbody></tbody></table>';

// Your CSS as text
var styles = `
 table, tr, th, td {
  border: 1px solid #C0C0C0;
  margin: 0 auto;
  border-collapse: collapse;
  border-spacing: 0;
  padding: 7px 10px;
}

#multi_results {
  margin-top: 20px;
}`

// var sheet = window.document.styleSheets[0];
// sheet.insertRule(styles, sheet.cssRules.length);

var styleSheet = document.createElement("style")
styleSheet.innerHTML = styles
document.head.appendChild(styleSheet)

let currentServer = 0
for (;currentServer < SPEEDTEST_SERVERS.length && SPEEDTEST_SERVERS[currentServer].pingT === -1; currentServer++) {}

function appendResult(server,serveropen, dl, ping, jitter) {
    // Determine the status icon based on jitter and download speed
    let statusIcon;
    if (jitter < 3 && dl > 100) {
        statusIcon = 'рџ‘ЌрџЏ»рџ‘ЌрџЏ»рџ‘ЌрџЏ»';
    } else if (jitter < 5 && dl > 50) {
        statusIcon = 'рџ‘ЌрџЏ»рџ‘ЌрџЏ»';
    } else if (jitter < 10 && dl > 30) {
        statusIcon = 'рџ‘ЌрџЏ»';
    } else {
        statusIcon = 'вќЊ';
    }
    // Determine the output symbol based on serveropen value
        let isopen = serveropen === "YES" ? "Р”РѕСЃС‚СѓРїРµРЅ вњ…" : "Р—Р°РїРѕР»РЅРµРЅ рџ”“";
    // Append the result row to the table
    document.getElementById("multi_results").getElementsByTagName('tbody')[0].innerHTML +=
        '<tr><td>' +
        server + "</td><td>" +
        isopen + "</td><td>" +
        jitter + "</td><td>" +
        dl + "</td><td>" +
        statusIcon + "</td></tr>";
}

function startStop2(){
    if(s.getState()==3){
    //speedtest is running, abort
    s.abort();
    data=null;
    I("startStopBtn").className="";
    I("startStopBtn2").className="";
    I("server").disabled=false;
    initUI();
  }else{
    //test is not running, begin
    I("startStopBtn").className="running";
    I("startStopBtn2").className="running";
    I("shareArea").style.display="none";
    I("server").disabled=true;
    s.onupdate=function(data){
            uiData=data;
    };
    s.onend = function(aborted) {
        I("startStopBtn").className="";
        I("startStopBtn2").className="";
        I("server").disabled=false;
        updateUI(true);
        if(!aborted){
          appendResult(SPEEDTEST_SERVERS[currentServer].name, SPEEDTEST_SERVERS[currentServer].serveropen, uiData.dlStatus, uiData.pingStatus, uiData.jitterStatus)
            //if testId is present, show sharing panel, otherwise do nothing
            try{
                var testId=uiData.testId;
                if(testId!=null){
                    var shareURL=window.location.href.substring(0,window.location.href.lastIndexOf("/"))+"/results/?id="+testId;
                    I("resultsImg").src=shareURL;
                    I("resultsURL").value=shareURL;
                    I("testId").innerHTML=testId;
                    I("shareArea").style.display="";
                }
            }catch(e){}

            currentServer++
            for (;currentServer < SPEEDTEST_SERVERS.length && SPEEDTEST_SERVERS[currentServer].pingT === -1; currentServer++) {}
            document.getElementById("currentTest").innerHTML = "Currently testing: " + SPEEDTEST_SERVERS[currentServer].name
            if (currentServer < SPEEDTEST_SERVERS.length) {
                s.setSelectedServer(SPEEDTEST_SERVERS[currentServer])
                startStop2()
            }
            else {
                document.getElementById("currentTest").innerHTML = ''
            }
        }
    };
    s.start();
  }
}

function startStop3() {
    if(s.getState() !== 3) {
    document.getElementById("multi_results").getElementsByTagName('tbody')[0].innerHTML = '<tr>' +
              '<th>Server</th>' +
              '<th>Close / Open</th>' +
              '<th>Jitter, ms</th>' +
              '<th>Download, Mbps</th>' +
              '<th>Status</th>' +
              '</tr>'

    currentServer = 0
    for (;currentServer < SPEEDTEST_SERVERS.length && SPEEDTEST_SERVERS[currentServer].pingT === -1; currentServer++) {}
    document.getElementById("currentTest").innerHTML = "Currently testing: " + SPEEDTEST_SERVERS[currentServer].name

    s.setSelectedServer(SPEEDTEST_SERVERS[currentServer])
    }
    else {
        document.getElementById("currentTest").innerHTML = ''
    }
    

  startStop2()
}

