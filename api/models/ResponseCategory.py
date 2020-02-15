from enum import Enum


class ResponseCategory(Enum):
    PURPOSES_OF_PROCESSING = "purposes_of_processing_user_data"
    CATEGORIES_COLLECTED = "data_categories_collected"
    RECIPIENTS_OF_DATA = "recipients_of_user_data"
    RIGHT_TO_WITHDRAW_CONSENT_FROM_PROCESSING = "right_to_withdraw_consent_from_processing"
    COMMUNICATION_OF_POLICY_CHANGES = "ways_policy_changes_are_communicated"