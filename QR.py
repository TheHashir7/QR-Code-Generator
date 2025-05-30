import qrcode
import streamlit as st
from PIL import Image
import io


st.set_page_config(page_title="QR Code Generator", layout="centered")
st.title("🔗 Generate Qr Code in Your Style")
user=st.text_input("Enter url to generate your QR code")
is_whatsapp = st.checkbox("Is this a WhatsApp number?")

# Customized Colors 
st.sidebar.header("🎨 Customize QR Code")
fill_color = st.sidebar.color_picker("QR Color", "#000000")
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")

logo = st.sidebar.checkbox("Add logo to the center")
logo_file = None
if logo:
    logo_file = st.sidebar.file_uploader("Upload logo (PNG or JPG)", type=["png", "jpg", "jpeg"])


if st.button("Generate QR Code"):
    if user:
        if is_whatsapp:
            if user.isdigit():
                user = (f"https://wa.me/{user}")
            else:
                st.warning("⛔ WhatsApp number must be numeric without '+' or dashes.")

        qr = qrcode.QRCode(
             version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(user)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color,back_color = bg_color ).convert("RGB")

        if logo and logo_file:
            try:
                logo = Image.open(logo_file)
                logo_size = 60
                logo = logo.resize((logo_size, logo_size))
                pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
                img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
            except Exception as e:
                st.error(f"⚠️ Error processing logo: {e}")
        

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
