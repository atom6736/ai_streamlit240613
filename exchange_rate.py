import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO


def ex_rate():
    def get_exchange(currency_code):
        last_page_num=10
        df = pd.DataFrame()

        for page_no in range(1,last_page_num+1):
            url=f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
            dfs = pd.read_html(url, header=1, encoding='cp949')

            if dfs[0].empty:
                if (page_no == 1):
                    print(f"통화코드({currency_code})가 잘못 지정되었습니다.")
                else:
                    print(f"{page_no}마지막 페이지 입니다.")
                break

            #print(dfs[0])
            df = pd.concat([df,dfs[0]],ignore_index=True)

        return df


    currency_name_dict={'미국 달러':'USD', '유럽연합 유로':'EUR', '일본 엔':'JPY'}
    # currency_name = st.sidebar.selectbox('통화선택',currency_name_dict.keys())
    # clicked = st.sidebar.button("환율 데이터 가져오기")
    currency_name = st.selectbox('통화선택',currency_name_dict.keys())
    clicked = st.button("환율 데이터 가져오기")


    if clicked:
        currency_code = currency_name_dict[currency_name]
        df_exchange = get_exchange(currency_code)
        # print(df_exchange)

        # 원하는 열만 선택
        df_exchange_rate = df_exchange[['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']]
        df_exchange_rate2 = df_exchange_rate.set_index('날짜')

        # 날짜열의 데이터 변경
        df_exchange_rate2.index= pd.to_datetime(df_exchange_rate2.index, format="%Y-%m-%d", errors='ignore')


        # 환율 데이터 표시
        st.subheader(f"{currency_name} 환율데이터")
        st.dataframe(df_exchange_rate2.head(20))

        # 차트(선 그래프) 그리기
        matplotlib.rcParams['font.family']='Malgun Gothic'

        ax = df_exchange_rate2['매매기준율'].plot(figsize=(15,5), grid=True)    
        ax.set_title("환율(매개기준율) 그래프", fontsize=20)
        ax.set_xlabel("기간",fontsize=10 )
        ax.set_ylabel(f"원화/{currency_name}",fontsize=10 )
        plt.xticks(fontsize=10) # x축 눈금값의 폰트 크기
        plt.yticks(fontsize=10)
        fig = ax.get_figure()# fig객체를 먼저 만들어준다.
        st.pyplot(fig)

        # 파일 다운로드
        st.text("** 환율 데이터 파일 다운로드 **")
        # dataframe데이터를 csv 파일로 변환
        csv_data = df_exchange_rate.to_csv() #가상의 공간안에 csv_data라고 데이터가 저장됨.

        # 데이터프레임을 엑셀로 변환. csv는 텍스트는 바로 메로리안에 컨버트가 되는데, 엑셀은 바이너리로 변환이 되어 저장되기때문에 주의해야 함.
        excel_data = BytesIO()    #메모리 버퍼(임시장소)에 바이너리 객체가 생상되는 것
        df_exchange_rate.to_excel(excel_data) # 엑셀 형식으로 버퍼에 쓰겠다는 것.

        #버튼을 두개 만들어 쓸 것
        col = st.columns(2) # 2개의 세로단 생성
        with col[0]:
            st.download_button("csv 파일 다운로드", csv_data, file_name='exchange_rate_data.csv')
        with col[1]:
            st.download_button("csv 파일 다운로드", excel_data, file_name='exchange_rate_data.xlsx') #가서 누르면 경로도 설정할 수 있게 나온다고.


    # df_exchange_rate2.info()
# else:
#     pass
