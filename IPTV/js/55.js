/**
 * Onlyskaz балансеры для Lampa
 * Подключение:
 *   <script src="https://ваш-домен/onlyskaz.js"></script>
 *
 * Использование:
 *   window.onlyskaz.init()   // инициализация с email из config.email
 *   window.onlyskaz.getBalancers({ kpId: "123456" })
 *     .then(list => console.log(list));
 */

(function () {
  // ===== НАСТРОЙКИ =====
  const config = {
    // <<< ВПИШИ СВОЙ EMAIL СЮДА >>>
    email: "Kova_sahsa@mail.ru"
  };

  const state = {
    email: null,
    encodedEmail: null,
    originPlain: "lampa.mx",
    origin: null,
    referer: "https://cub.rip/",
    unicId: null,
    scdn: null,
    dmail: null,
    rand: null,
    inited: false
  };

  // Вспомогательные функции
  function b64(s) {
    return btoa(unescape(encodeURIComponent(s)));
  }
  function urlencode(s) {
    return encodeURIComponent(s);
  }
  function log(msg, data) {
    console.log("[onlyskaz]", msg, data || "");
  }

  async function fetchText(url, headers = {}) {
    const res = await fetch(url, {
      method: "GET",
      headers: Object.assign({
        "Accept": "application/javascript, application/json"
      }, headers),
      cache: "no-store",
      redirect: "follow"
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} для ${url}`);
    const text = await res.text();
    if (text.trim().startsWith("<")) throw new Error(`HTML вместо JS/JSON для ${url}`);
    return text;
  }

  // Инициализация: авторизация по email
  async function init(email = config.email) {
    if (!email || !/^[^@]+@[^@]+\.[^@]+$/.test(email)) {
      throw new Error("Нужен корректный email");
    }
    state.email = email.trim();
    state.encodedEmail = urlencode(b64(state.email));
    state.origin = urlencode(b64(state.originPlain));
    state.rand = Math.random().toString().slice(2, 11);

    const tvjsUrl = `http://skaz.tv/tv.js?email=${state.encodedEmail}&logged=true&reset=${Math.random()}&origin=${state.origin}`;
    log("Загрузка tv.js", tvjsUrl);

    const tvjsRaw = await fetchText(tvjsUrl, {
      "Referer": state.referer,
      "Origin": `https://${state.originPlain}`
    });

    // Вытаскиваем параметры
    state.dmail = (tvjsRaw.match(/dmail\s*=\s*["']([^"']+)["']/) || [])[1] || null;
    state.unicId = (tvjsRaw.match(/lampac_unic_id",\s*"([^"]+)"/) || [])[1] || "cubrip123";
    state.scdn   = (tvjsRaw.match(/skazcdn"\],\s*"([^"]+)"/) || [])[1] || "edge1";

    log("Параметры", { dmail: state.dmail, unic_id: state.unicId, scdn: state.scdn });
    state.inited = true;
    return { email: state.email, unic_id: state.unicId, scdn: state.scdn };
  }

  // Формируем ссылку на externals для фильма
  function buildExternalsUrl({ kpId, movieId }) {
    const params = new URLSearchParams();
    if (kpId) params.set("kinopoisk_id", kpId);
    if (movieId) params.set("movie_id", movieId);
    params.set("unic_id", state.unicId);
    params.set("cdn", state.scdn);
    params.set("reset", state.rand);
    return `http://skaz.tv/externals/?${params.toString()}`;
  }

  // Получаем список балансеров для фильма
  async function getBalancers({ kpId, movieId }) {
    if (!state.inited) throw new Error("Сначала вызови window.onlyskaz.init()");
    if (!kpId && !movieId) throw new Error("Нужен kpId или movieId");

    const url = buildExternalsUrl({ kpId, movieId });
    log("Загрузка externals", url);

    const res = await fetch(url, { method: "GET", headers: { "Accept": "application/json" } });
    if (!res.ok) throw new Error(`HTTP ${res.status} при загрузке externals`);
    const text = await res.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      log("Ошибка JSON, возвращаю сырой текст", text.slice(0, 200));
      return [{ type: "raw", payload: text }];
    }

    const list = [];
    if (Array.isArray(data)) {
      data.forEach(item => list.push({
        provider: item.provider || "unknown",
        title: item.title || item.name || "Источник",
        quality: item.quality || null,
        url: item.url || item.stream || null
      }));
    } else if (typeof data === "object") {
      for (const [prov, v] of Object.entries(data)) {
        if (Array.isArray(v)) {
          v.forEach(it => list.push({
            provider: prov,
            title: it.title || it.name || "Источник",
            url: it.url || it.stream || null
          }));
        }
      }
    }
    log("Балансеры получены", list.length);
    return list;
  }

  // Экспортируем API
  window.onlyskaz = {
    init,
    getBalancers,
    setEmail: async (email) => { state.inited = false; return init(email); },
    getState: () => ({ ...state })
  };

  // Автоинициализация по email из config
  init(config.email).catch(err => log("Ошибка автоинициализации", err));
})();
