from msal import ConfidentialClientApplication
import requests
from config.azure_config import CLIENT_ID, CLIENT_SECRET, AUTHORITY, REDIRECT_URI, SCOPES

# Initialize MSAL client
msal_client = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY,
)

def get_auth_url():
    """Generate the Azure AD authorization URL."""
    return msal_client.get_authorization_request_url(
        scopes=SCOPES, redirect_uri=REDIRECT_URI
    )

def get_user_info(auth_code):
    """Exchange the authorization code for a token and get user info."""
    token_response = msal_client.acquire_token_by_authorization_code(
        code=auth_code, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    access_token = token_response.get("access_token")

    if access_token:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        if response.status_code == 200:
            return response.json()
    return None
