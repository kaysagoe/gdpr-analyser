from enum import Enum, auto


class ClassifierType(Enum):
    CATEGORY = "category"
    CHANGE_TYPE = "change-type"
    CHOICE_TYPE = "choice-type"
    NOTIFICATION_TYPE = "notification-type"
    PERSONAL_INFORMATION_TYPE = "personal-information-type"
    PURPOSE = "purpose"
    THIRD_PARTY_ENTITY = "third-party-entity"
