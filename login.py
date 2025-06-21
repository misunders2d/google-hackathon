import streamlit as st

def login_screen():
    st.header("This app requires authorization.")
    st.subheader("Please log in.")
    st.button("Log in with Google", on_click=st.login, use_container_width=True, type="primary")


def login_st():
    if not st.user.is_logged_in:
        login_screen()
    else:
        with st.sidebar:
            if 'picture' in st.user and isinstance(st.user.picture, str):
                user_picture = st.user.picture
            else:
                user_picture = 'media/user_avatar.jpg'
            st.image(user_picture, width=50)
            if 'name' in st.user and isinstance(st.user.name, str):
                user_name = st.user.name
            else:
                user_name = "Unknown User"
            st.subheader(user_name)
            st.button("Log out", on_click=st.logout)
        return True
    return False