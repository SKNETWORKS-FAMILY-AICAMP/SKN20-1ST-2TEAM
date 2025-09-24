# db_manager.py

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# MySQL 데이터베이스 엔진 생성
def get_db_engine():
    """MySQL 데이터베이스 엔진을 반환합니다."""
    return create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )

# 테이블 생성 함수
def create_tables(engine):
    """필요한 데이터베이스 테이블을 생성합니다."""
    with engine.connect() as conn:
        print("MySQL 데이터베이스 연결 성공!")
        # 차량 등록 데이터 테이블
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS car_regist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                reg_date VARCHAR(255),
                sido VARCHAR(255),
                sigungu VARCHAR(255),
                car_type VARCHAR(255),
                usage_type VARCHAR(255),
                fuel_type VARCHAR(255),
                count INT
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        '''))
        # FAQ 데이터 테이블
        conn.execute(text('''
            CREATE TABLE IF NOT EXISTS faq (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category TEXT,
                question TEXT,
                answer TEXT,
                source INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        '''))
        conn.commit()
    print("데이터베이스 테이블 생성이 완료되었습니다.")