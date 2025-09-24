# data_viewer.py

import streamlit as st
import pandas as pd
import plotly.express as px
from db_manager import get_db_engine
from data_collector import collect_and_save_data

# ---- 데이터 로딩 및 캐싱 함수 ----
@st.cache_data(ttl=3600)
def load_and_cache_data():
    """데이터를 로드하고, 데이터가 없으면 수집하여 DB에 저장합니다."""
    engine = get_db_engine()

    try:
        car_df = pd.read_sql("SELECT * FROM car_regist", engine)
    except Exception:
        car_df = pd.DataFrame()

    try:
        faq_df = pd.read_sql("SELECT question, answer, source FROM faq", engine)
    except Exception:
        faq_df = pd.DataFrame()

    if car_df.empty or faq_df.empty:
        st.info("데이터가 없습니다. 자동으로 데이터 수집을 시작합니다.")
        collect_and_save_data()
        
        car_df = pd.read_sql("SELECT * FROM car_regist", engine)
        faq_df = pd.read_sql("SELECT question, answer, source FROM faq", engine)

    engine.dispose()

    if not car_df.empty:
        car_df["year"] = car_df["reg_date"].str[:4]
        car_df["month"] = car_df["reg_date"].str[4:6]

    return car_df, faq_df

# ---- 페이지 표시 함수들 ----
def show_main_page():
    """앱의 메인 화면을 표시합니다."""
    st.title("🚗 자동차 통합 정보 플랫폼")
    st.markdown("---")
    st.markdown("### 메인 화면")
    st.write("환영합니다! 아래 버튼을 눌러 원하는 페이지로 이동하세요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 데이터 조회", use_container_width=True):
            st.session_state.page = '데이터 조회'
    with col2:
        if st.button("❓ FAQ", use_container_width=True):
            st.session_state.page = 'FAQ'

def show_data_dashboard(car_df):
    """'데이터 조회' 페이지를 표시합니다."""
    st.header("📈 차량 등록 통계")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        years = sorted(car_df["year"].unique())
        selected_year = st.selectbox("연도", years, key='year_select')
    with col2:
        months = sorted(car_df[car_df["year"] == selected_year]["month"].unique())
        selected_month = st.selectbox("월", months, key='month_select')
    with col3:
        sido_list = sorted(car_df["sido"].unique())
        selected_sido = st.selectbox("시도", sido_list, key='sido_select')
    with col4:
        filtered_sigungu = sorted(car_df[car_df["sido"] == selected_sido]["sigungu"].unique())
        selected_sigungu = st.selectbox("시군구", filtered_sigungu, key='sigungu_select')

    filtered_df = car_df[
        (car_df["year"] == selected_year) &
        (car_df["month"] == selected_month) &
        (car_df["sido"] == selected_sido) &
        (car_df["sigungu"] == selected_sigungu)
    ]
    
    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    else:
        tabs_car = st.tabs(["차량 종류별", "차량 용도별", "데이터 테이블"])
        with tabs_car[0]:
            st.subheader("차량 종류별 등록대수")
            chart_df = filtered_df.groupby("car_type")["count"].sum().reset_index()
            st.bar_chart(chart_df.set_index("car_type"), height=300)
        with tabs_car[1]:
            st.subheader("차량 용도별 비율")
            pie_df = filtered_df.groupby("usage_type")["count"].sum().reset_index()
            fig = px.pie(pie_df, names='usage_type', values='count', hole=0.45)
            st.plotly_chart(fig, use_container_width=True)
        with tabs_car[2]:
            st.subheader("필터링된 데이터")
            st.dataframe(filtered_df, height=400, use_container_width=True)

def show_faq_page(faq_df):
    """'FAQ' 페이지를 표시합니다."""
    st.header("❓ 통합 FAQ")
    st.markdown("---")
    
    search_query = st.text_input("궁금한 점을 입력하세요.", placeholder="차량 정비, 보증, 부품 등...", key='faq_search')
    
    if search_query:
        search_results = faq_df[
            faq_df['question'].str.contains(search_query, case=False, na=False) |
            faq_df['answer'].str.contains(search_query, case=False, na=False)
        ]
        if search_results.empty:
            st.info("검색 결과가 없습니다.")
        else:
            display_paginated_faq(search_results)
    else:
        display_paginated_faq(faq_df)
        
def display_paginated_faq(df):
    """페이지네이션이 적용된 FAQ 결과를 표시합니다."""
    st.markdown(f"총 {len(df)}개의 FAQ가 있습니다.")
    st.markdown("---")

    page_size = 10
    total_pages = (len(df) + page_size - 1) // page_size
    
    if 'current_faq_page' not in st.session_state:
        st.session_state.current_faq_page = 1
        
    cols = st.columns([1, 5, 1])
    with cols[0]:
        if st.button("이전 페이지"):
            if st.session_state.current_faq_page > 1:
                st.session_state.current_faq_page -= 1
    with cols[2]:
        if st.button("다음 페이지"):
            if st.session_state.current_faq_page < total_pages:
                st.session_state.current_faq_page += 1
    with cols[1]:
        st.markdown(f"<div style='text-align:center;'>페이지: {st.session_state.current_faq_page} / {total_pages}</div>", unsafe_allow_html=True)
    
    start_index = (st.session_state.current_faq_page - 1) * page_size
    end_index = start_index + page_size
    
    paginated_df = df.iloc[start_index:end_index]
    
    for _, row in paginated_df.iterrows():
        source_name = "현대차" if row['source'] == 0 else "기아차"
        with st.expander(f"**Q. {row['question']}**"):
            st.markdown(f"**출처:** _{source_name}_")
            st.write(f"**A.** {row['answer']}")

def show_dashboard():
    """메인 대시보드 함수. 초기 로딩과 페이지 분기를 관리합니다."""
    if 'page' not in st.session_state:
        st.session_state.page = 'loading'
    
    # CSS 스타일은 여기에 통합
    st.set_page_config(page_title="자동차 통합 정보 플랫폼", layout="wide")
    st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    div[data-testid="stSidebarContent"] {
        padding-top: 1rem;
    }
    .main-page {
        text-align: center;
        padding-top: 10rem;
    }
    .main-page .stButton>button {
        padding: 1rem 2rem;
        font-size: 1.25rem;
    }
    .st-emotion-cache-1aplgmp {
        min-width: 2.5rem !important;
        min-height: 2.5rem !important;
    }
    .st-emotion-cache-pd6qx2 {
        width: 2.5rem !important;
        height: 2.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 로딩 페이지
    if st.session_state.page == 'loading':
        with st.spinner("데이터를 로드하는 중입니다. 처음 실행 시 시간이 오래 걸릴 수 있습니다."):
            car_df, faq_df = load_and_cache_data()
        
        st.session_state.car_data = car_df
        st.session_state.faq_data = faq_df
        
        st.session_state.page = 'main'
        st.rerun()
        
    # 메인 페이지
    elif st.session_state.page == 'main':
        st.set_page_config(layout="centered")  # 메인 페이지에만 중앙 정렬 레이아웃 적용
        show_main_page()
    
    # 데이터 조회/FAQ 페이지
    else:
        st.set_page_config(layout="wide")  # 다른 페이지에는 와이드 레이아웃 적용
        
        st.sidebar.title("메뉴")
        st.sidebar.header("자동차 통합 정보 플랫폼")
        
        # 홈 아이콘 버튼 추가
        if st.sidebar.button("🏠 메인으로", use_container_width=True):
            st.session_state.page = 'main'
            st.rerun()
        
        st.sidebar.markdown("---")
        
        if st.session_state.page == "데이터 조회":
            if st.session_state.car_data.empty:
                st.warning("차량 등록 데이터가 없습니다.")
            else:
                show_data_dashboard(st.session_state.car_data)
        elif st.session_state.page == "FAQ":
            if st.session_state.faq_data.empty:
                st.warning("FAQ 데이터가 없습니다.")
            else:
                show_faq_page(st.session_state.faq_data)