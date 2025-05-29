# aking Qr code Generator using streamlit
import qrcode
import streamlit as st
# from PIL import Image
import io

st.title("🔗 Qr Code Generator")
user=st.text_input("Enter url to generate your QR code")


if st.button("Generate QR Code"):
    if user:
        qr = qrcode.QRCode(
            version=15,
            box_size=10,
            border=5
        )
        qr.add_data(user)
        qr.make(fit=True)
        img = qr.make_image(fill="black",back_color = "white" ).convert("RGB")
        

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        st.image(img, caption="Here is your QR Code", use_container_width=False)

        img.save("qr_code.png")
        with open("qr_code.png", "rb") as file:
            st.download_button(
                label="📥 Download QR Code",
                data=buf,
                file_name="qr_code.png",
                mime="image/png"
            )
    else:
        st.warning("⛔ Please Enter a Valid URL")
