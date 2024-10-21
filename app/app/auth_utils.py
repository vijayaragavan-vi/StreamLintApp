import msal
import streamlit as st
import requests

# Azure AD App details
CLIENT_ID = '308fad87-b3d9-4c08-afa2-6583f2a92450'
TENANT_ID = "2fc13e34-f03f-498b-982a-7cb446e25bc6"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_PATH = "http://localhost:8501/" 
SCOPES = ["User.Read"]

msal_instance = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=None,
)

# def get_auth_url():
#     """Generates the login URL."""
#     return msal_instance.get_authorization_request_url(
#         SCOPES,
#         redirect_uri=f"http://localhost:8501{REDIRECT_PATH}",
#     )
def get_auth_url():
    # Construct the authorization URL
    url = f"{AUTHORITY}/oauth2/v2.0/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8501/redirect&scope=User.Read"
    response = requests.get(url, verify=False)  # Disable SSL verification
    return response.ur

def handle_token_response(response):
    """Stores token in session state."""
    if "error" in response:
        st.error(f"Login failed: {response['error_description']}")
    else:
        st.session_state["token"] = response["access_token"]
        st.session_state["user"] = response["id_token_claims"]
        st.success(f"Welcome {st.session_state['user']['name']}")

def get_token_from_code(auth_code):
    """Fetches token using authorization code."""
    return msal_instance.acquire_token_by_authorization_code(
        auth_code, SCOPES, redirect_uri=f"http://localhost:8501{REDIRECT_PATH}"
    )
