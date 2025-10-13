from notifications_python_client.notifications import NotificationsAPIClient


def send_email_notification_for_questionnaire_without_daybatch(config, questionnaire_name):
    try:
        print(f"Sending email notification for questionnaire {questionnaire_name} to {config.to_notify_email}")
        notifications_client = NotificationsAPIClient(config.notify_api_key)
        notifications_client.send_email_notification(
            email_address=f"{config.to_notify_email}",
            template_id=f"26ee1592-2de8-4ca7-a833-219595e110cf",
            personalisation={"questionnaire_name": questionnaire_name}
        )
    except Exception as error:
        print(f"Error when sending email notification for questionnaire {questionnaire_name} via GOV.UK Notify API - ", error)

def test_send_email_notification(config, questionnaire_name):
    try:
        print(f"Sending test email notification for questionnaire {questionnaire_name} to {config.to_notify_email}")
        notifications_client = NotificationsAPIClient(config.notify_api_key)
        notifications_client.send_email_notification(
            email_address=f"{config.to_notify_email}",
            template_id=f"26ee1592-2de8-4ca7-a833-219595e110cf",
            personalisation={"questionnaire_name": questionnaire_name}
        )
    except Exception as error:
        print(f"Error when sending email notification for questionnaire {questionnaire_name} via GOV.UK Notify API - ", error)
