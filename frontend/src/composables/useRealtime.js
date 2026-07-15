import { ref } from "vue";

// 앱 전체에서 연결을 하나만 사용하기 위해
// 상태를 모듈 바깥(전역)에 둔다.
export const onlineCount = ref(0);
export const connected = ref(false);
export const notices = ref([]);

let socket = null;
let retryTimer = null;
let pingTimer = null;
let retryDelay = 1000; // 재연결 대기 시간 (실패할수록 늘어남)
let noticeSeq = 0;

function buildWebSocketUrl() {
  const base = import.meta.env.VITE_API_BASE_URL;

  // 배포 환경: http(s)://... → ws(s)://...
  if (base) {
    return base.replace(/^http/, "ws") + "/ws";
  }

  // 로컬 개발: vite 프록시를 통해 백엔드로 연결
  const protocol = location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${location.host}/ws`;
}

function pushNotice(notice) {
  const id = ++noticeSeq;

  notices.value.push({
    id,
    ...notice,
  });

  // 6초 뒤 자동으로 사라짐
  setTimeout(() => removeNotice(id), 6000);
}

export function removeNotice(id) {
  notices.value = notices.value.filter((n) => n.id !== id);
}

function handleMessage(event) {
  let data;

  try {
    data = JSON.parse(event.data);
  } catch {
    return;
  }

  if (data.type === "online") {
    onlineCount.value = data.count;
    return;
  }

  if (data.type === "new_post") {
    pushNotice({
      type: "new_post",
      postId: data.post.id,
      title: data.post.title,
      category: data.post.category,
    });
  }
}

export function connectRealtime() {
  // 이미 연결돼 있으면 다시 만들지 않는다.
  if (socket && socket.readyState <= WebSocket.OPEN) {
    return;
  }

  socket = new WebSocket(buildWebSocketUrl());

  socket.onopen = () => {
    connected.value = true;
    retryDelay = 1000;

    // 연결이 유휴 상태로 끊기지 않도록 25초마다 신호를 보낸다.
    pingTimer = setInterval(() => {
      if (socket?.readyState === WebSocket.OPEN) {
        socket.send("ping");
      }
    }, 25000);
  };

  socket.onmessage = handleMessage;

  socket.onclose = () => {
    connected.value = false;
    onlineCount.value = 0;
    clearInterval(pingTimer);

    // 서버가 재시작되는 경우 등을 대비해 자동으로 다시 연결한다.
    // 실패가 반복되면 대기 시간을 늘려 서버 부담을 줄인다. (최대 15초)
    clearTimeout(retryTimer);
    retryTimer = setTimeout(connectRealtime, retryDelay);
    retryDelay = Math.min(retryDelay * 2, 15000);
  };

  socket.onerror = () => {
    socket?.close();
  };
}

export function disconnectRealtime() {
  clearTimeout(retryTimer);
  clearInterval(pingTimer);

  if (socket) {
    socket.onclose = null; // 의도적인 종료이므로 재연결하지 않음
    socket.close();
    socket = null;
  }

  connected.value = false;
}
