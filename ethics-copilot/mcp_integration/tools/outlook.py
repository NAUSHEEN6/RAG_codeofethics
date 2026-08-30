import webbrowser
from urllib.parse import quote


def send_outlook_email(
    recipient: str,
    subject: str,
    body: str
):

    try:

        compose_url = (
            "https://outlook.office.com/mail/deeplink/compose"
            f"?to={quote(recipient)}"
            f"&subject={quote(subject)}"
            f"&body={quote(body)}"
        )

        webbrowser.open(compose_url)

        return {
            "success": True,
            "message": (
                "Outlook Web compose window "
                "opened for review."
            ),
            "recipient": recipient,
            "subject": subject
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }