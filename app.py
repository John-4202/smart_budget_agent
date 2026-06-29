import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Smart Budget Agent",page_icon="💰",layout="wide")
DATA=Path("budget.csv")
if not DATA.exists():
    pd.DataFrame(columns=["date","type","category","amount","memo"]).to_csv(DATA,index=False)

def load():
    return pd.read_csv(DATA)
def save(df):
    df.to_csv(DATA,index=False)

st.title("💰 Smart Budget Agent")
menu=st.sidebar.radio("메뉴",["대시보드","입력","내역","AI 분석"])

df=load()

if menu=="입력":
    with st.form("f"):
        d=st.date_input("날짜",date.today())
        t=st.selectbox("구분",["수입","지출"])
        c=st.selectbox("카테고리",["급여","식비","교통","쇼핑","생활","문화","기타"])
        a=st.number_input("금액",min_value=0,step=1000)
        m=st.text_input("메모")
        if st.form_submit_button("저장"):
            df.loc[len(df)]=[d,t,c,a,m]
            save(df)
            st.success("저장 완료")

elif menu=="내역":
    st.dataframe(df,use_container_width=True)
    st.download_button("CSV 다운로드",df.to_csv(index=False),"budget.csv","text/csv")

elif menu=="대시보드":
    income=df[df.type=="수입"]["amount"].sum() if len(df) else 0
    expense=df[df.type=="지출"]["amount"].sum() if len(df) else 0
    bal=income-expense
    c1,c2,c3=st.columns(3)
    c1.metric("총 수입",f"{income:,.0f}원")
    c2.metric("총 지출",f"{expense:,.0f}원")
    c3.metric("잔액",f"{bal:,.0f}원")
    if len(df):
        spend=df[df.type=="지출"]
        if len(spend):
            st.subheader("카테고리별 지출")
            st.bar_chart(spend.groupby("category")["amount"].sum())

else:
    st.header("🤖 AI 소비 분석")
    if len(df)==0:
        st.info("데이터를 먼저 입력하세요.")
    else:
        income=df[df.type=="수입"]["amount"].sum()
        expense=df[df.type=="지출"]["amount"].sum()
        ratio=expense/income*100 if income else 0
        spend=df[df.type=="지출"]
        if len(spend):
            top=spend.groupby("category")["amount"].sum().sort_values(ascending=False)
            st.write(f"가장 많이 소비한 항목: **{top.index[0]} ({top.iloc[0]:,.0f}원)**")
        st.write(f"지출률: **{ratio:.1f}%**")
        if ratio<60:
            st.success("소비가 안정적입니다.")
        elif ratio<80:
            st.warning("지출이 다소 높습니다.")
        else:
            st.error("지출 비율이 매우 높습니다.")
