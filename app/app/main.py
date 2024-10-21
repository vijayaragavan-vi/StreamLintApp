import streamlit as st
from auth_utils import get_auth_url, get_token_from_code, handle_token_response

st.set_page_config(page_title="MSAL Streamlit App", layout="wide")

if "token" not in st.session_state:
    st.title("Login with Microsoft Account")
    
    # Generate Login URL
    login_url = get_auth_url()
    st.markdown(f"[Click here to login]({login_url})")

    # Check if redirected back with an auth code
    if "code" in st.experimental_get_query_params():
        auth_code = st.experimental_get_query_params()["code"][0]
        response = get_token_from_code(auth_code)
        handle_token_response(response)
else:
    st.sidebar.success("You are logged in!")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())
    st.write(f"Hello, {st.session_state['user']['name']}! Welcome to the dashboard.")

    # Optionally show a link to another page
    st.markdown("[Go to Dashboard](pages/dashboard.py)")
