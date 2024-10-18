import streamlit as st
from utils.auth import get_auth_url, get_user_info

st.title("Azure AD Auth with Streamlit")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    auth_url = get_auth_url()
    st.write(f"Please [sign in with Azure AD]({auth_url})")

    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        auth_code = query_params["code"][0]
        user_info = get_user_info(auth_code)

        if user_info:
            st.session_state["authenticated"] = True
            st.session_state["user_info"] = user_info
        else:
            st.error("Authentication failed. Please try again.")
else:
    user_info = st.session_state["user_info"]
    st.write(f"Hello, {user_info['displayName']}!")
    st.json(user_info)

    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
