import csv
import pymysql
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def read_csv_to_list(file_path):
    """
    CSV 파일을 읽어서 데이터를 리스트로 반환합니다.
    """
    res_list = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # 헤더 행 건너뛰기
            
            for row in reader:
                try:
                    float_value = float(row[1])
                    int_value = int(float_value)
                    new_row = [row[0], int_value]
                    res_list.append(new_row)
                except (ValueError, IndexError) as e:
                    print(f"❗ 데이터 변환 오류 발생: {e} - 행 건너뜀: {row}")
                    continue
        print(f"✅ CSV 파일에서 {len(res_list)}개의 행을 성공적으로 읽었습니다.")
        return res_list
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None
    except Exception as e:
        print(f"파일 처리 중 오류 발생: {e}")
        return None

def insert_data_into_db(data_list):
    """
    주어진 데이터 리스트를 MySQL 데이터베이스에 삽입합니다.
    """
    if not data_list:
        print("데이터가 없어 삽입 작업을 건너뜁니다.")
        return

    conn = None
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        
        # `executemany()`를 사용하여 데이터 삽입
        sql_query = "INSERT INTO population (region, popul) VALUES (%s, %s)"
        cursor.executemany(sql_query, data_list)
        
        conn.commit()
        print(f"🎉 {len(data_list)}개의 행이 성공적으로 삽입되었습니다.")
    except pymysql.MySQLError as e:
        print(f"데이터베이스 오류 발생: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
    finally:
        if conn and conn.open:
            conn.close()

if __name__ == "__main__":
    csv_file_path = 'population_total_filtered.csv'
    data_to_insert = read_csv_to_list(csv_file_path)
    insert_data_into_db(data_to_insert)