import streamlit as st
from graph.graph import graph_func
from langchain_core.messages import HumanMessage, AIMessage
from tools.memory import memory
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "images/background/2.jpg"
avatar='images/GigaChat.png'
img_base64 = get_img_as_base64(img_path)


st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
      background-image: url("data:image/jpg;base64,{img_base64}");
      background-position: center;
      background-size: cover;
    }}
    [data-testid="stHeader"] {{
    background-color: rgba(0, 0, 0, 0);
    }}
    [data-testid="stBottomBlockContainer"]{{
    background-color: rgba(0, 0, 0, 0)!important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(page_title="ИИ-Хакасия", layout="wide")
st.title("🤖 Туристический ИИ-агент ТИЦ Хакасия")

if st.button("Новый диалог"):
    memory.clear()
    st.session_state.clear()
    st.rerun()

# --- Управление состоянием ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Здравствуйте! Я ваш туристический помощник с портала туристического информационного центра"
                          " на базе GigaChat! "
                          "Чем могу помочь?")
    ]
if "params_flow" not in st.session_state:
    st.session_state.params_flow = {
        "accomodation": None,
        "holiday_recommendation": None,
        "nature_recommendation": None
    }

if "usage_logged" not in st.session_state:
    with open('usage.txt', 'a') as f:
        f.write('\n\n---CHAT---\n')
    st.session_state.usage_logged = True

@st.cache_resource
def get_graph():
    return graph_func()

app = get_graph()


for message in st.session_state.messages:
    # Используем правильный аватар в зависимости от роли
    current_avatar = avatar if message.type == 'ai' else None
    with st.chat_message(message.type, avatar=current_avatar):
        st.markdown(message.content)



if prompt := st.chat_input("Спросите что-нибудь о турах..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.rerun()



if st.session_state.messages and st.session_state.messages[-1].type == "human":
    last_user_input = st.session_state.messages[-1].content

    # Отображаем спиннер в контейнере ассистента, пока ждем ответ
    with st.chat_message("ai", avatar=avatar):
        with st.spinner("Думаю..."):
            # Собираем state для графа
            initial_state = {
                "input": last_user_input,
                # Вся история, кроме последнего сообщения пользователя
                "chat_history": st.session_state.messages[:-1],
            }

            # Вызываем граф. Это блокирующая операция.
            response_state = app.invoke(initial_state)
            response_content = response_state.get("result", "Извините, я не смог обработать ваш запрос.")

            # Добавляем полученный ответ в историю
            st.session_state.messages.append(AIMessage(content=response_content))

    st.rerun()
