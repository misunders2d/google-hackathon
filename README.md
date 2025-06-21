# google-hackathon
A sample of Google Agents team (Google ADK framework) collaborating on creating tiktok content
App is built on Streamlit.

Login capabilities require a ".streamlit" folder with a "secrets.toml" file properly configured:

[auth]
redirect_uri = "http://localhost:8501/oauth2callback" #or your web uri, make sure to include "/oauth2callback" at the end
cookie_secret = "very_secret_SeCreT_KeY"
client_id = "xxx"
client_secret = "xxx"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

Refer to [this help page](https://docs.streamlit.io/develop/api-reference/user/st.login) for documentation on login.

App uses Google ADK, make sure to create a Google Cloud project and obtain necessary credentials (simple google API key is enough) - see .env.example file for examples.