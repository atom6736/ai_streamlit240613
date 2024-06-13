import streamlit as st
from PIL import Image

#사이드바 화면을 먼저 만들고
st.sidebar.title("사이드바")
st.sidebar.header("텍스트 입력")
user_id = st.sidebar.text_input("ID입력:", value='streamlit', max_chars=15)
user_pw = st.sidebar.text_input("PW입력", value='abcd', type='password')

#사이드바 두번째에 적는게 오른쪽이 된다. 
st.sidebar.header("셀렉트박스")
sel_opt = ['진주 귀걸이를 한 소녀','별이 빛나는 밤','절규','월하정인']
user_opt = st.sidebar.selectbox("좋아하는 작품은?", sel_opt)
st.sidebar.write("선택한 작품은:", user_opt)

#메인 화면
st.title("스트림릿의 사이드바")
# folder = r'D:\AI_ThrusdayCLass\data\data\'
image_files=['Vermeer.png','Gogh.png','Munch.png','ShinYoonbok.png']

sel_img_index = sel_opt.index(user_opt)
#선택한 항목에 맞는 이미지파일이 무엇인지를 먼저 지정
img_file = image_files[sel_img_index]
img_local = Image.open(r"D:/AI_ThrusdayCLass/data/data/"+img_file) #PIL에서 이미지를 열어주는 것.
st.image(img_local,caption=user_opt) # 이미지를 표시하는 것

