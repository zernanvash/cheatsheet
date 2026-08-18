(function () {
  "use strict";
  const channel = "BroadcastChannel" in window ? new BroadcastChannel("ch-vault-session") : null;
  const tabId = crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random()}`;
  const leaderKey = "ch-vault-heartbeat-leader";
  const heartbeatKey = "ch-vault-heartbeat-success";
  let timer;

  function read(key) { try { return JSON.parse(localStorage.getItem(key) || "null"); } catch { return null; } }
  function write(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} }
  function isLeader() {
    const now = Date.now();
    const leader = read(leaderKey);
    if (!leader || now - leader.at > 75000 || leader.id === tabId) {
      write(leaderKey, { id: tabId, at: now });
      return true;
    }
    return false;
  }
  async function heartbeat(force) {
    const last = Number(read(heartbeatKey) || 0);
    if (!isLeader() || (!force && Date.now() - last < 110000)) return;
    try {
      const response = await fetch("/auth/heartbeat", { method: "POST", credentials: "same-origin", headers: { "X-Vault-Heartbeat": "1" } });
      if (response.status === 401) {
        clearInterval(timer);
        location.assign(`/login?next=${encodeURIComponent(location.pathname + location.search + location.hash)}`);
        return;
      }
      if (response.ok) {
        write(heartbeatKey, Date.now());
        channel?.postMessage({ type: "heartbeat" });
      }
    } catch {}
  }
  function tick() {
    if (isLeader()) {
      write(leaderKey, { id: tabId, at: Date.now() });
      heartbeat(false);
    }
  }
  channel?.addEventListener("message", (event) => {
    if (event.data?.type === "heartbeat") write(heartbeatKey, Date.now());
  });
  addEventListener("storage", tick);
  addEventListener("focus", () => heartbeat(false));
  document.addEventListener("visibilitychange", () => { if (!document.hidden) heartbeat(false); });
  heartbeat(true);
  timer = setInterval(tick, 30000);
}());

