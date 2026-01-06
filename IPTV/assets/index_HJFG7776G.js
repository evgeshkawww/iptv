function I(i){return document.getElementById(i);}

/* ======================= SERVERS ======================= */
var SPEEDTEST_SERVERS=[
{
name:"s1.turbod.iptv",
server:"https://ru.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"YES"
},
{
name:"s2.turbod.iptv",
server:"https://5.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"YES"
},
{
name:"s3.turbod.iptv",
server:"https://8.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"NO"
},
{
name:"s4.turbod.iptv",
server:"https://15.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"NO"
},
{
name:"s5.turbod.iptv",
server:"https://ua2.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"YES"
},
{
name:"s6.turbod.iptv",
server:"https://4.tvtm.one:8080/",
dlURL:"backend/garbage.php",
ulURL:"backend/empty.php",
pingURL:"backend/empty.php",
getIpURL:"backend/getIP.php",
serveropen:"YES"
},
{
name:"s7.turbod.iptv",
server:"https://14.tvtm.one:8080/",
serveropen:"NO"
},
{
name:"s8.turbod.iptv",
server:"https://ru3.tvtm.one:8080/",
serveropen:"YES"
},
{
name:"s9.turbod.iptv",
server:"https://nl.tvtm.one:8080/",
serveropen:"YES"
},
{
name:"s16.turbod.iptv",
server:"https://hk.tvtm.one:8080/",
serveropen:"YES"
}
];

/* ======================= SPEEDTEST INIT ======================= */
var s=new Speedtest();
s.setParameter("telemetry_level","basic");

/* ======================= SERVER INIT ======================= */
function initServers(){
    s.addTestPoints(SPEEDTEST_SERVERS);
    s.selectServer(function(server){
        I("loading").className="hidden";
        var sel=I("server");

        var opt=document.createElement("option");
        opt.value="all";
        opt.textContent="🌍 Все сервера";
        opt.selected=true;
        sel.appendChild(opt);

        SPEEDTEST_SERVERS.forEach(function(srv,i){
            var o=document.createElement("option");
            o.value=i;
            o.textContent=srv.name+(srv.serveropen==="NO"?" ❌":" 🌎");
            sel.appendChild(o);
        });
        I("testWrapper").className="visible";
        initUI();
    });
}

/* ======================= UI METERS ======================= */
var meterBk="#80808040";
var dlColor="#4CAF50",progColor=meterBk;

function drawMeter(c,amount){
    var ctx=c.getContext("2d");
    ctx.clearRect(0,0,c.width,c.height);
    ctx.beginPath();
    ctx.arc(100,100,80,-Math.PI*1.1,amount*Math.PI*1.2-Math.PI*1.1);
    ctx.strokeStyle=dlColor;
    ctx.lineWidth=10;
    ctx.stroke();
}
function format(d){
    d=Number(d);
    return d<10?d.toFixed(2):d.toFixed(1);
}

/* ======================= TEST CONTROL ======================= */
var uiData=null;
var groupResults=[];
var serverQueue=[];
var current=0;

function startStop(){
    if(s.getState()==3){
        s.abort();
        return;
    }
    prepareResultTable();
    if(I("server").value==="all"){
        prepareMultiTest();
    }else{
        runSingleServerTest();
    }
}

/* ======================= RESULT TABLE ======================= */
function prepareResultTable(){
    I("test").innerHTML=
    "<div>📅 Сгенерировано: "+new Date().toLocaleString()+"</div>"+
    "<table id='multi_results'><tbody>"+
    "<tr><th>🌐 Сервер</th><th>📶 Статус</th><th>⚡ Джиттер</th><th>🚀 Скорость</th><th>🏆 Оценка</th></tr>"+
    "</tbody></table>";
}

/* ======================= SINGLE TEST ======================= */
function runSingleServerTest(){
    var i=I("server").value;
    var srv=SPEEDTEST_SERVERS[i];
    s.setSelectedServer(srv);
    s.onupdate=d=>uiData=d;
    s.onend=function(){
        appendResult(srv.name,srv.serveropen,uiData.dlStatus,uiData.jitterStatus);
    };
    s.start();
}

/* ======================= MULTI TEST ======================= */
function prepareMultiTest(){
    groupResults=[];
    serverQueue=SPEEDTEST_SERVERS.map((_,i)=>i);
    current=0;
    startNext();
}
function startNext(){
    if(current>=serverQueue.length){
        var best=findBestServer(groupResults);
        I("currentTest").innerHTML="🏆 Лучший сервер: <b>"+best.name+"</b> ⚡ "+best.jitter+" ms";
        return;
    }
    var idx=serverQueue[current++];
    var srv=SPEEDTEST_SERVERS[idx];
    s.setSelectedServer(srv);
    s.onupdate=d=>uiData=d;
    s.onend=function(){
        appendResult(srv.name,srv.serveropen,uiData.dlStatus,uiData.jitterStatus);
        groupResults.push({name:srv.name,jitter:uiData.jitterStatus,dl:uiData.dlStatus});
        startNext();
    };
    s.start();
}

/* ======================= TABLE ROW ======================= */
function appendResult(name,open,dl,jitter){
    var icon=jitter<5?"🥇":jitter<10?"🥈":"💀";
    var status=open==="YES"?"🌎 Online":"❌ OFF";
    I("multi_results").getElementsByTagName("tbody")[0].innerHTML+=
    "<tr><td>"+name+"</td><td>"+status+"</td><td>"+jitter+"</td><td>"+dl+"</td><td>"+icon+"</td></tr>";
}

/* ======================= BEST SERVER BY JITTER ======================= */
function findBestServer(arr){
    arr.sort((a,b)=>a.jitter-b.jitter);
    return arr[0];
}

/* ======================= UI LOOP ======================= */
function initUI(){
    I("dlText").textContent="";
    I("pingText").textContent="";
}

