import streamlit as st

st.title("📝 Formulaire d'évaluation")
st.markdown("Votre avis nous aide à améliorer cette application. Merci de prendre 2 minutes.")

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeJyibMxp2Sk9ouCRZaipp9wXiTXEKbGZPwyJ7FWyX83fIlCw/viewform?usp=publish-editor"
KOBO_FORM_URL   = "https://ee.kobotoolbox.org/x/VOTRE_KOBO_ID"

col1, col2 = st.columns(2)

with col1:
    st.subheader("Google Forms")
    st.markdown("Répondez via **Google Forms**.")
    st.link_button(
        "📋 Ouvrir Google Forms",
        GOOGLE_FORM_URL,
        use_container_width=True,
    )

with col2:
    st.subheader("Kobo Toolbox")
    st.markdown("Répondez via **Kobo Toolbox**.")
    st.link_button(
        "📋 Ouvrir Kobo Toolbox",
        KOBO_FORM_URL,
        use_container_width=True,
    )


