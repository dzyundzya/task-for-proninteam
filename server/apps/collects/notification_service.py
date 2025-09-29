from django.conf import settings
from django.core.mail import EmailMessage

from server.apps.collects.models import Collect
from server.apps.payments.models import Payment


class EmailService:
    """Service for sending emails."""

    @classmethod
    def send_text_email(
        cls,
        subject: str,
        to_emails: list[str],
        message: str,
    ) -> None:
        """Send plain text email."""
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails,
        )
        email.send()


class CollectNotificationService:
    """Service for collect-related notifications."""

    @classmethod
    def send_collect_created_email(cls, collect: Collect) -> None:
        """Send email to author about collect creation."""
        author_name = collect.author.username

        message = f"""Hello, {author_name}!

        Your group collection "{collect.title}" has been successfully created.

        Collection details:
        • Title: {collect.title}
        • Occasion: {collect.get_occasion_display()}
        • Target amount: {collect.planned_amount or 'Unlimited collection'} rub
        • Description: {collect.description or 'Not specified'}

        Now other users can make donations to your collection.

        Best regards,
        Service Team

        ---
        This is an automated message, please do not reply to it."""

        EmailService.send_text_email(
            subject=f'Collection "{collect.title}" successfully created',
            to_emails=[collect.author.email],
            message=message,
        )


class PaymentNotificationService:
    """Service for payment-related notifications."""

    @classmethod
    def send_payment_created_email(cls, payment: Payment) -> None:
        """Send email to donor about payment creation."""
        user_name = payment.user.get_full_name() or payment.user.username
        status_text = 'Paid' if payment.paid else 'Pending payment'

        message = f"""Hello, {user_name}!

        Your payment "{payment.collect.title}" has been successfully created.

        Payment details:
        • Collection: {payment.collect.title}
        • Amount: {payment.amount} rub.
        • Status: {status_text}
        • Comment: {payment.comment or 'Not specified'}

        Thank you for your support!

        Best regards,
        Service Team

        ---
        This is an automated message, please do not reply to it."""

        EmailService.send_text_email(
            subject=f'Payment to collection "{payment.collect.title}" created',
            to_emails=[payment.user.email],
            message=message,
        )

    @classmethod
    def send_collect_author_notification(cls, payment: Payment) -> None:
        """Send email to collect author about new payment."""
        author = payment.collect.author
        author_name = author.get_full_name() or author.username
        donor_name = payment.user.get_full_name() or payment.user.username

        message = f"""Hello, {author_name}!

        Your collection "{payment.collect.title}" has received a new payment.

        Details:
        • From: {donor_name}
        • Amount: {payment.amount} rub.
        • Comment: {payment.comment or 'Not specified'}
        • Status: {'Paid' if payment.paid else 'Pending payment'}

        Current collection progress:
        • Collected: {payment.collect.current_amount} rub.
        • Number of donations: {payment.collect.donations_count}

        Best regards,
        Service Team

        ---
        This is an automated message, please do not reply to it."""

        EmailService.send_text_email(
            subject=f'New payment in your collection {payment.collect.title}',
            to_emails=[author.email],
            message=message,
        )
