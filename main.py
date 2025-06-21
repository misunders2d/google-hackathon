import streamlit as st
from login import login_st
st.set_page_config(page_title = 'TikTok creator app',layout="wide")

from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types

from tiktok_creator.agent import create_root_agent

from dotenv import load_dotenv
load_dotenv()

APP_NAME='tiktok_creator_agent'

if login_st():
    if 'email' in st.user and isinstance(st.user.email, str):
        user_id = st.user.email
    else:
        user_id = 'unknown_user'
    user_name = st.user.name if 'name' in st.user else "Unknown User"
    if 'picture' in st.user and isinstance(st.user.picture, str):
        user_picture = st.user.picture
    else:
        user_picture = 'media/user_avatar.jpg'

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=user_picture if message["role"]=="user" else None):
            st.markdown(message["content"])


    new_msg = ''

    async def run_agent(user_input:str, session_id:str, user_id:str):
        global new_msg
        
        if 'session_service' not in st.session_state:
            st.session_state['session_service'] = InMemorySessionService()
            await st.session_state['session_service'].create_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id
            )
        else:
            await st.session_state['session_service'].get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id)
        session_service = st.session_state['session_service']
        artifact_service = InMemoryArtifactService()

        runner = Runner(
            agent=create_root_agent(),
            app_name=APP_NAME,
            session_service=session_service,
            artifact_service=artifact_service
        )

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(role='user', parts=[types.Part(text=user_input)])):

            if event.content and event.content.parts and event.content.parts[0].text:
                new_msg += event.content.parts[0].text
                yield event.content.parts[0].text
            elif event.content and event.content.parts and event.content.parts[0].function_call:
                st.toast(f'Running {event.content.parts[0].function_call.name} function\n')
            elif (
                event.content and event.content.parts
                and event.content.parts[0].function_response
                and event.content.parts[0].function_response.response
                and 'result' in event.content.parts[0].function_response.response
                and isinstance(event.content.parts[0].function_response.response['result'], str)
                ):
                new_msg += event.content.parts[0].function_response.response['result']
                yield event.content.parts[0].function_response.response['result']
            #handle errors
            elif event.error_code:
                st.error(f"Sorry, the following error happened:\n{event.error_code}")
                async for event in runner.run_async(
                    user_id=user_id,
                    session_id=session_id,
                    new_message=types.Content(role='user', parts=[types.Part(text=f'This error happened, please check: {event}')])):
                    if event.content and event.content.parts and event.content.parts[0].text:
                        new_msg += event.content.parts[0].text
                        yield event.content.parts[0].text

    if prompt_text := st.chat_input("Ask me what I can do ;)"):
        st.chat_message("user", avatar=user_picture).markdown(prompt_text)
        st.session_state.messages.append({"role": "user", "content": prompt_text})

        with st.chat_message("assistant"):
            try:
                st.write_stream(run_agent(user_input=prompt_text, session_id='session123', user_id=user_id))
            except Exception as e:
                st.error(f'Sorry, an error occurred, please try later:\n{e}')
        st.session_state.messages.append({"role": "assistant", "content": new_msg})

else:
    st.write("Please log in.")