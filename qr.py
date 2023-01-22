import qrcode
from io import BytesIO

def generateQRCode(recipient=None,iban=None,amount=None,currency=None,purpose=None) -> BytesIO:
    if None in (recipient, iban, amount, currency, purpose):
        raise Exception("Missing arguement")

    # Create the QR code data string in the EPC format
    qr_data = f"BCD\n002\n1\nSCT\n\n{recipient}\n{iban}\n{currency}{amount}\n\n\n{purpose}"

    # Create a QR code object
    qr = qrcode.QRCode(version=1, box_size=10, border=5)

    # Add the wire transfer information to the QR code object
    qr.add_data(qr_data)

    # Make the QR code image
    qr.make(fit=True)

    # Create an image from the QR code object
    img = qr.make_image(fill_color="black", back_color="white")

    # Create a binary buffer to receive PNG data.
    buf = BytesIO()

    # Save the QR code image to the buffer
    img.save(buf, format='PNG')

    # Get the value of the binary buffer
    return buf.getvalue()
    