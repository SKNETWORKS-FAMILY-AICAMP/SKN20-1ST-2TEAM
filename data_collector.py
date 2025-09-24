# data_collector.py

from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service as sv
from webdriver_manager.chrome import ChromeDriverManager as cdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import requests
import time
import pandas as pd
import os
from sqlalchemy import text
from dotenv import load_dotenv
from db_manager import get_db_engine, create_tables

load_dotenv()

# MOLIT API 데이터 수집 및 정제 함수
def fetch_and_process_molit_data():
    """MOLIT API에서 차량 등록 데이터를 수집하고 정규화합니다."""
    print("\n--- MOLIT API 데이터 수집 및 정제 시작 ---")
    api_key = os.getenv("MOLIT_API_KEY", "4c49d1028d634c258ca4c7b99eb4a134")
    url = "http://stat.molit.go.kr/portal/openapi/service/rest/getList.do"
    params = {
        "key": api_key,
        "form_id": 5498,
        "style_num": 2,
        "start_dt": 201101,
        "end_dt": 202508
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data["result_data"]["formList"])
        
        df["reg_date"] = df["date"].astype(str).str[:6]
        value_cols = [c for c in df.columns if any(x in c for x in ["승용", "승합", "화물", "특수"])]
        long_df = df.melt(
            id_vars=["reg_date", "시도명", "시군구"],
            value_vars=value_cols,
            var_name="category",
            value_name="count"
        )
        long_df[["car_type", "usage_type"]] = long_df["category"].str.split(">", expand=True)
        final_df = long_df.rename(columns={"시도명": "sido", "시군구": "sigungu"})
        final_df = final_df[["reg_date", "sido", "sigungu", "car_type", "usage_type", "count"]]
        final_df["count"] = pd.to_numeric(final_df["count"], errors="coerce").fillna(0).astype(int)
        final_df = final_df[(final_df["usage_type"] != "계") & (final_df["sigungu"] != "계")].copy()
        
        print("MOLIT API 데이터 정제 완료. 최종 데이터 수:", len(final_df))
        return final_df
    except requests.exceptions.RequestException as e:
        print(f"MOLIT API 호출 오류: {e}")
        return pd.DataFrame()

# FAQ 크롤링 함수 (현대차)
def crawl_hyundai_faq():
    """현대차 웹사이트에서 FAQ 데이터를 크롤링합니다."""
    # (이전 답변과 동일한 코드)
    # ...
    # return faq_data
    
# FAQ 크롤링 함수 (기아차)
def crawl_kia_faq():
    """기아차 웹사이트에서 FAQ 데이터를 크롤링합니다."""
    # (이전 답변과 동일한 코드)
    # ...
    # return faq_data

def collect_and_save_data():
    """모든 데이터를 수집하고 데이터베이스에 저장합니다."""
    engine = get_db_engine()
    create_tables(engine)

    # 1. MOLIT API 데이터 수집 및 저장
    df_molit = fetch_and_process_molit_data()
    if not df_molit.empty:
        df_molit.to_sql("car_regist", con=engine, if_exists="replace", index=False)
        print("✅ MOLIT API 데이터 DB 저장 완료.")

    # 2. 현대차 FAQ 데이터 수집 및 저장
    hyundai_faqs = crawl_hyundai_faq()
    if hyundai_faqs:
        df_hyundai = pd.DataFrame(hyundai_faqs, columns=['category', 'question', 'answer', 'source'])
        df_hyundai.to_sql('faq', con=engine, if_exists='append', index=False)
        print("✅ 현대차 FAQ 데이터 DB 저장 완료.")

    # 3. 기아차 FAQ 데이터 수집 및 저장
    kia_faqs = crawl_kia_faq()
    if kia_faqs:
        df_kia = pd.DataFrame(kia_faqs, columns=['category', 'question', 'answer', 'source'])
        df_kia.to_sql('faq', con=engine, if_exists='append', index=False)
        print("✅ 기아차 FAQ 데이터 DB 저장 완료.")

    engine.dispose()
    print("✅ 모든 데이터 수집 및 DB 저장 작업 완료.")