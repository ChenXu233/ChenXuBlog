from fastapi import Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import SecretStr

from backend.config import CONFIG
from backend.logger import logger

# 邮件服务器配置（仅在启用时创建）
mail_config = None
if CONFIG.MAIL_ENABLED and CONFIG.MAIL_USERNAME:
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
    verify_url = request.url_for("verify_email", token=verify_token)

    logger.info(f"Verify URL for {email}: {verify_url}")

    if not mail_config:
        # 邮件未配置，只打印日志
        logger.info(f"[Mail disabled] Would send verification to {email}: {verify_url}")
        return verify_url

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
        logger.warning(f"Failed to send verify email to {email}: {e}")
    logger.info(f"Verify email sent to {email}.")

    return verify_url

async def send_comment_notify_email(
    email: str,
    blog_title: str,
    blog_id: int,
    commenter: str,
    content: str,
):
    """评论/回复通知。邮件未配置时只打日志。"""
    url = f"{CONFIG.SITE_URL.rstrip('/')}/article/{blog_id}"
    subject = "ChenXuBlog: 新的评论通知"
    body = (
        f"<p>{commenter} 评论了你的文章《{blog_title}》：</p>"
        f"<blockquote>{content}</blockquote>"
        f'<p><a href="{url}">查看评论</a></p>'
    )

    if not mail_config:
        logger.info(f"[Mail disabled] Comment notify to {email}: {commenter}: {content}")
        return

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )
    try:
        await FastMail(mail_config).send_message(message)
        logger.info(f"Comment notify email sent to {email}.")
    except Exception as e:
        logger.warning(f"Failed to send comment notify email to {email}: {e}")
