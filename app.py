
import os
import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="텍스트 음성 변환", page_icon="🔊")
st.title("🔊 텍스트 음성 변환")
st.caption("생성되는 음성은 AI가 만든 음성입니다.")

# API 키 설정
api_key = os.getenv("OPENAI_API_KEY") or st.sidebar.text_input(
    "OpenAI API 키",
    type="password"
)

# 텍스트 입력
text = st.text_area(
    "읽을 텍스트를 입력하세요.",
    "안녕하세요. OpenAI 텍스트 음성 변환 실습입니다."
)

# 버튼
if st.button("음성으로 변환"):
    if text.strip() == "":
        st.warning("읽을 텍스트를 입력해주세요.")
    elif not api_key:
        st.warning("왼쪽 사이드바에 API 키를 입력해주세요.")
    else:
        try:
            client = OpenAI(api_key=api_key)

            with st.spinner("음성 생성 중..."):
                # TTS 생성
                speech = client.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=text,
                    response_format="mp3"
                )
                audio_bytes = speech.content

            # 음성 출력
            st.markdown("### 🔊 음성 재생")
            st.audio(audio_bytes, format="audio/mp3")

            # 파일 다운로드
            st.download_button(
                "MP3 다운로드",
                data=audio_bytes,
                file_name="speech.mp3",
                mime="audio/mpeg"
            )

        except Exception as e:
            st.error(f"음성 생성 중 오류가 발생했습니다: {e}")
