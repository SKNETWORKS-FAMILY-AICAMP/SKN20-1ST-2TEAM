import pandas as pd
from db_manager import get_db_engine

def get_population_data_from_db():
    """
    데이터베이스에서 population 테이블의 데이터를 불러옵니다.
    """
    engine = get_db_engine()
    try:
        # DB에서 population 테이블 전체를 불러와 Pandas DataFrame으로 변환
        query = "SELECT region, popul FROM population"
        df = pd.read_sql(query, con=engine)
        print("✅ `population` 데이터 DB 로드 완료.")
        return df
    except Exception as e:
        print(f"❗ `population` 데이터 로드 오류: {e}")
        return pd.DataFrame()
    finally:
        engine.dispose()