import os

from dotenv import load_dotenv

from functions.questionnaire_functions import (
    get_installed_questionnaire_data,
    get_questionnaires_with_active_survey_day_today_and_cases,
    create_daybatch_for_questionnaire,
    check_questionnaire_has_daybatch
)
from functions.notify_functions import send_email_notification_for_questionnaire_without_daybatch, test_send_email_notification
from models.config_model import Config


def create_daybatches(_request):
    print(f"Running Cloud Function - create_daybatches")
    config = Config.from_env()
    config.log()
    installed_questionnaire_data = get_installed_questionnaire_data(config)
    if not installed_questionnaire_data:
        print(f"No questionnaires installed")
        return "No questionnaires installed"
    questionnaires_with_active_survey_day_today_and_cases = get_questionnaires_with_active_survey_day_today_and_cases(
        installed_questionnaire_data)
    if not questionnaires_with_active_survey_day_today_and_cases:
        print(f"No questionnaires installed with an active survey day of today and has cases")
        return "No questionnaires installed with an active survey day of today and has cases"
    for questionnaire in questionnaires_with_active_survey_day_today_and_cases:
        try:
            if not check_questionnaire_has_daybatch(config, questionnaire):
                create_daybatch_for_questionnaire(config, questionnaire)
            else:
                print(f"Questionnaire {questionnaire} already has a daybatch for today")
        except Exception as error:
            print(f"An error '{error}' occured whilst checking/creating a daybatch for questionnaire {questionnaire}")
    return "Finished"


def check_daybatches(_request):
    print("Running Cloud Function - check_daybatches")
    config = Config.from_env()
    config.log()
    test_send_email_notification(config, "TEST_QUESTIONNAIRE")
    installed_questionnaire_data = get_installed_questionnaire_data(config)
    if not installed_questionnaire_data:
        print("No questionnaires installed")
        return "No questionnaires installed"
    questionnaires_with_active_survey_day_today_and_cases = get_questionnaires_with_active_survey_day_today_and_cases(
        installed_questionnaire_data)
    if not questionnaires_with_active_survey_day_today_and_cases:
        print(f"No questionnaires installed with an active survey day of today and has cases")
        return "No questionnaires installed with an active survey day of today and has cases"
    for questionnaire in questionnaires_with_active_survey_day_today_and_cases:
        try:
            if not check_questionnaire_has_daybatch(config, questionnaire):
                send_email_notification_for_questionnaire_without_daybatch(config, questionnaire)
        except Exception as error:
            print(f"An error '{error}' occured whilst checking a daybatch or sending an email for questionnaire {questionnaire}")                
    return "Finished"


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()
