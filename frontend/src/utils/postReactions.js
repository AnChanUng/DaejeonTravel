// localStorage 기반 좋아요/북마크 상태 관리
// 로그인 기능이 없는 게시판이라, "내가 이 글에 좋아요/북마크를 눌렀는지"는
// 서버가 아니라 이 브라우저(기기)에 저장한다. 카운트 자체는 서버가 관리한다.

const LIKED_KEY = "board:liked_posts";
const BOOKMARKED_KEY = "board:bookmarked_posts";

function readIds(key) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function writeIds(key, ids) {
  localStorage.setItem(key, JSON.stringify(ids));
}

export function isLiked(postId) {
  return readIds(LIKED_KEY).includes(postId);
}

export function isBookmarked(postId) {
  return readIds(BOOKMARKED_KEY).includes(postId);
}

export function setLiked(postId, liked) {
  const ids = readIds(LIKED_KEY);
  const next = liked
    ? [...new Set([...ids, postId])]
    : ids.filter((id) => id !== postId);
  writeIds(LIKED_KEY, next);
}

export function setBookmarked(postId, bookmarked) {
  const ids = readIds(BOOKMARKED_KEY);
  const next = bookmarked
    ? [...new Set([...ids, postId])]
    : ids.filter((id) => id !== postId);
  writeIds(BOOKMARKED_KEY, next);
}

export function getBookmarkedIds() {
  return readIds(BOOKMARKED_KEY);
}
