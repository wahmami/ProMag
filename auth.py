import streamlit as st

def login():
    """
    Displays a login form and handles user authentication.
    Returns True if the user is successfully logged in, False otherwise.
    """
    st.title("PerfMan Lite - Login")

    # Ensure credentials are configured in Streamlit's secrets
    if "credentials" not in st.secrets or "usernames" not in st.secrets["credentials"]:
        st.error("Authentication credentials are not configured correctly.")
        st.info("Please add a [credentials.usernames] section to your .streamlit/secrets.toml file.")
        st.stop()

    users = st.secrets["credentials"]["usernames"]

    # Create the login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in users and users[username] == password:
                # If credentials are correct, set session state and rerun
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    return False
