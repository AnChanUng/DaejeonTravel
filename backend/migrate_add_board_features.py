# migrate_add_board_features.py — 딱 한 번 실행하는 스크립트
#
# posts 테이블이 이미 만들어져 있는 상태에서 새 컬럼(조회수/좋아요/북마크/이미지/태그)을
# 추가하기 위한 마이그레이션. SQLAlchemy의 create_all()은 "테이블이 없을 때만" 만들어주고
# 기존 테이블에 컬럼을 자동으로 추가해주지는 않기 때문에 필요하다.
#
# 실행: python migrate_add_board_features.py
# 이미 컬럼이 있으면 자동으로 건너뛰므로 여러 번 실행해도 안전하다.
import sqlite3

DB_PATH = "localhub.db"

NEW_COLUMNS = [
    ("image", "VARCHAR"),
    ("tags", "VARCHAR"),
    ("view_count", "INTEGER DEFAULT 0"),
    ("like_count", "INTEGER DEFAULT 0"),
    ("bookmark_count", "INTEGER DEFAULT 0"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA table_info(posts)")
existing_columns = {row[1] for row in cur.fetchall()}

for name, coltype in NEW_COLUMNS:
    if name in existing_columns:
        print(f"이미 존재함, 건너뜀: {name}")
        continue
    cur.execute(f"ALTER TABLE posts ADD COLUMN {name} {coltype}")
    print(f"컬럼 추가 완료: {name}")

conn.commit()
conn.close()
print("마이그레이션 완료")