from fastapi import Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import SecretStr

from backend.config import CONFIG

# 邮件服务器配置
mail_config = ConnectionConfig(
    MAIL_USERNAME=CONFIG.MAIL_USERNAME,
    MAIL_PASSWORD=SecretStr(CONFIG.MAIL_PASSWORD),
    MAIL_FROM=CONFIG.MAIL_FROM,
    MAIL_PORT=CONFIG.MAIL_PORT,
    MAIL_SERVER=CONFIG.MAIL_SERVER,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)


async def send_verify_email(request: Request, email: str, verify_token: str):
    """发送电子邮件验证码"""
    # 使用 FastAPI 的 url_for 生成验证链接
    verify_url = request.url_for("verify_email", token=verify_token)

    print(f"Verify URL: {verify_url}")

    body = f"Please verify your email by clicking the following link: {verify_url}"
    message = MessageSchema(
        subject="Email Verify",
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(mail_config)
    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Failed to send verify email to {email}: {e}")
    print(f"Verify email sent to {email}.")

    return verify_url
