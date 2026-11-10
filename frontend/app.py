
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="BhashaMitra AI",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 BhashaMitra AI")
st.subheader("Your multilingual voice ordering assistant")

st.write(
    "Speak naturally in Hindi, Telugu or Hinglish "
    "and place your grocery order."
)

language = st.selectbox(
    "Choose your language",
    ["Hindi", "Telugu", "Hinglish"]
)

st.divider()

st.subheader("🎤 Voice ordering")

audio = st.audio_input("Record your grocery order")

if audio is not None:

    if st.button("Process voice order", type="primary"):

        with st.spinner("Understanding your voice..."):

            try:
                response = requests.post(
                    f"{API_URL}/process-audio",
                    files={
                        "audio": (
                            audio.name,
                            audio.getvalue(),
                            audio.type or "audio/wav"
                        )
                    },
                    data={"language": language},
                    timeout=90
                )

                response.raise_for_status()
                result = response.json()

                st.session_state["result"] = result
                st.success("Voice successfully processed!")

            except requests.RequestException as error:
                st.error(f"Processing failed: {error}")

st.divider()

st.subheader("⌨️ Or type your order")

text = st.text_area(
    "Enter your order",
    placeholder="Example: 2 kg rice, 1 litre milk and 2 bread packets"
)

if st.button("Generate text order"):

    if text.strip():

        try:
            response = requests.post(
                f"{API_URL}/process-text",
                json={
                    "text": text,
                    "language": language
                },
                timeout=30
            )

            response.raise_for_status()

            st.session_state["result"] = response.json()

        except requests.RequestException as error:
            st.error(f"Order processing failed: {error}")

if "result" in st.session_state:

    result = st.session_state["result"]

    st.divider()
    st.header("📋 Your order summary")

    st.write("**Recognized speech / text:**")
    st.info(result["transcript"])

    st.write("**Detected model:**", result.get("model", "Text input"))

    items = result["order"]["items"]

    if items:

        st.write("### Products")

        for item in items:
            st.write(
                f"- {item['product'].title()} × "
                f"{item['quantity']} = "
                f"₹{item['total']}"
            )

        st.metric(
            "Estimated total",
            f"₹{result['order']['total_amount']}"
        )

        st.success(result["response"])

        if st.button("🔊 Hear AI response"):

            try:
                with st.spinner("Generating voice response..."):

                    audio_response = requests.post(
                        f"{API_URL}/speak",
                        json={
                            "text": result["response"],
                            "language": language
                        },
                        timeout=90
                    )

                    audio_response.raise_for_status()

                st.audio(
                    audio_response.content,
                    format="audio/wav"
                )

            except requests.RequestException as error:
                st.error(f"Voice generation failed: {error}")

        if st.button("Confirm order"):
            st.success(
                "Demo order confirmed! "
                "No actual purchase or payment was made."
            )

    else:
        st.warning(
            "No products were identified. "
            "Please try another order."
        )

st.divider()

st.caption(
    "Powered by Gnani AI Prisma v2.5 and Timbre v2.5"
)
