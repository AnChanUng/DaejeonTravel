import { ref, computed } from "vue";

// 앱 전체에서 연결과 알림 목록을 하나만 사용하기 위해
// 상태를 모듈 바깥(전역)에 둔다.
export const onlineCount = ref(0);
export const connected = ref(false);
export const notifications = ref([]);

export const unreadCount = computed(
  () => notifications.value.filter((n) => !n.read).length,
);

const STORAGE_KEY = "board:notifications";
const MAX_KEEP = 20;

let socket = null;
let retryTimer = null;
let pingTimer = null;
let retryDelay = 1000; // 재연결 대기 시간 (실패할수록 늘어남)
let baseTitle = "";
let titleWatching = false;

/* ---------------- 저장 / 불러오기 ---------------- */
// 새로고침해도 알림이 사라지지 않도록 브라우저에 보관한다.

function loadStored() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    notifications.value = raw ? JSON.parse(raw) : [];
  } catch {
    notifications.value = [];
  }
}

function save() {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(notifications.value.slice(0, MAX_KEEP)),
    );
  } catch {
    // 저장 공간이 없어도 알림 기능 자체는 계속 동작해야 하므로 무시
  }
}

/* ---------------- 탭 제목 배지 ---------------- */
// 사용자가 다른 탭을 보고 있을 때 제목을 "(2) 원래제목" 으로 바꿔
// 새 알림이 왔다는 걸 알려준다.

function applyTitle() {
  if (!baseTitle) return;

  const count = unreadCount.value;

  document.title =
    document.hidden && count > 0 ? `(${count}) ${baseTitle}` : baseTitle;
}

function watchTitle() {
  if (titleWatching) return;

  titleWatching = true;
  baseTitle = document.title;

  document.addEventListener("visibilitychange", applyTitle);
}

/* ---------------- 알림 조작 ---------------- */

export function markAllRead() {
  notifications.value = notifications.value.map((n) => ({ ...n, read: true }));
  save();
  applyTitle();
}

export function removeNotification(id) {
  notifications.value = notifications.value.filter((n) => n.id !== id);
  save();
  applyTitle();
}

export function clearNotifications() {
  notifications.value = [];
  save();
  applyTitle();
}

function addNotification(payload) {
  notifications.value = [
    {
      id: `${payload.postId}-${Date.now()}`,
      ...payload,
      at: new Date().toISOString(),
      read: false,
    },
    ...notifications.value,
  ].slice(0, MAX_KEEP);

  save();
  applyTitle();
}

/* ---------------- WebSocket ---------------- */

function buildWebSocketUrl() {
  // 💡 환경 변수에서 가져온 값을 공백 제거하고 정제합니다.
  const base = (import.meta.env.VITE_API_BASE_URL || "").trim();

  // 1. 만약 환경 변수가 제대로 설정되어 있고, 문자열 'VITE_API_BASE_URL'이 아니라 실제 주소인 경우
  if (base && !base.includes("VITE_API_BASE_URL")) {
    return base.replace(/^http/, "ws") + "/ws";
  }

  // 2. 환경 변수가 비어있거나 꼬였을 때를 대비한 완전 안전 장치 (하드코딩 배포 주소)
  // 이 주소로 확실하게 싱크를 맞춥니다.
  return "wss://localhub-7ql5.onrender.com/ws";
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
    addNotification({
      postId: data.post.id,
      title: data.post.title,
      category: data.post.category,
    });
  }
}

export function connectRealtime() {
  loadStored();
  watchTitle();

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

    // 서버 재시작 등에 대비해 자동으로 다시 연결한다.
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

/* ---------------- 표시용 유틸 ---------------- */

export function timeAgo(isoString) {
  const diff = Date.now() - new Date(isoString).getTime();
  const minutes = Math.floor(diff / 60000);

  if (minutes < 1) return "방금 전";
  if (minutes < 60) return `${minutes}분 전`;

  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}시간 전`;

  return `${Math.floor(hours / 24)}일 전`;
}
