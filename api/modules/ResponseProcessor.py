from typing import List

from api.models.CategoryAnalysis import CategoryAnalysis
from api.models.Annotation import Annotation
from api.models.ResponseCategory import ResponseCategory
from api.models.ClassifierType import ClassifierType
from typing import Dict


class ResponseProcessor:
    @staticmethod
    def run(annotations: List[Annotation], analysis: CategoryAnalysis):
        response = {
            ResponseCategory.PURPOSES_OF_PROCESSING.value: {},
            ResponseCategory.CATEGORIES_COLLECTED.value: {},
            ResponseCategory.RECIPIENTS_OF_DATA.value: {},
            ResponseCategory.RIGHT_TO_WITHDRAW_CONSENT_FROM_PROCESSING.value: {},
            ResponseCategory.COMMUNICATION_OF_POLICY_CHANGES.value: {}
        }

        firstPartyAnnotations = ResponseProcessor.get(annotations, analysis, "First Party Collection/Use")
        ResponseProcessor.insertResponse(response,
                                         ResponseProcessor.filterForUnemptyAndNotUnspecified(firstPartyAnnotations,
                                                                                             ClassifierType.PURPOSE),
                                         ResponseCategory.PURPOSES_OF_PROCESSING,
                                         ClassifierType.PURPOSE)

        ResponseProcessor.insertResponse(response,
                                         ResponseProcessor.filterForUnemptyAndNotUnspecified(firstPartyAnnotations,
                                                                                             ClassifierType.PERSONAL_INFORMATION_TYPE),
                                         ResponseCategory.CATEGORIES_COLLECTED,
                                         ClassifierType.PERSONAL_INFORMATION_TYPE)

        thirdPartyAnnotations = ResponseProcessor.get(annotations, analysis, "Third Party Sharing/Collection")
        ResponseProcessor.insertResponse(response,
                                         ResponseProcessor.filterForUnemptyAndNotUnspecified(thirdPartyAnnotations,
                                                                                             ClassifierType.THIRD_PARTY_ENTITY),
                                         ResponseCategory.RECIPIENTS_OF_DATA,
                                         ClassifierType.THIRD_PARTY_ENTITY)

        ResponseProcessor.insertResponse(response,
                                         list(filter(lambda x: "Opt-out via contacting company" in x.attributes[ClassifierType.CHOICE_TYPE.value]
                                                               or "Opt-out link" in x.attributes[ClassifierType.CHOICE_TYPE.value],
                                                     ResponseProcessor.filterForUnemptyAndNotUnspecified(
                                                         firstPartyAnnotations,
                                                         ClassifierType.CHOICE_TYPE))),
                                         ResponseCategory.RIGHT_TO_WITHDRAW_CONSENT_FROM_PROCESSING,
                                         ClassifierType.PERSONAL_INFORMATION_TYPE)

        policyChangeAnnotations = ResponseProcessor.get(annotations, analysis, "Policy Change")
        ResponseProcessor.insertResponse(response,
                                         list(filter(lambda x: "Privacy relevant change" in x.attributes[ClassifierType.CHANGE_TYPE.value], ResponseProcessor.filterForUnemptyAndNotUnspecified(policyChangeAnnotations,
                                                                                             ClassifierType.CHANGE_TYPE))),
                                         ResponseCategory.COMMUNICATION_OF_POLICY_CHANGES,
                                         ClassifierType.NOTIFICATION_TYPE)
        return response

    @staticmethod
    def get(annotations: List[Annotation], analysis: CategoryAnalysis, category: str):
        selectedAnnotations = None

        if category == "First Party Collection/Use":
            selectedAnnotations = [annotations[index] for index in analysis.firstPartyCollection]
        elif category == "Policy Change":
            selectedAnnotations = [annotations[index] for index in analysis.policyChange]
        elif category == "Third Party Sharing/Collection":
            selectedAnnotations = [annotations[index] for index in analysis.thirdPartySharing]
        return selectedAnnotations

    @staticmethod
    def insertResponse(response: Dict, annotations: List[Annotation], key: ResponseCategory,
                       attribute: ClassifierType):
        for annotation in annotations:
            for attr_value in annotation.attributes[attribute.value]:
                if attr_value != "Unspecified":
                    if attr_value in response[key.value]:
                        response[key.value][attr_value]["sources"].append(annotation.text)
                    else:
                        response[key.value][attr_value] = {
                            "description": f"/api/help?key={attr_value.replace(' ', '-').replace('/', '-').lower()}",
                            "sources": [annotation.text]
                        }

    @staticmethod
    def filterForUnemptyAndNotUnspecified(annotations: List[Annotation], attribute: ClassifierType):
        return list(filter(lambda x: (len(x.attributes[attribute.value]) > 1) or
                                     (len(x.attributes[attribute.value]) == 1 and x.attributes[attribute.value][
                                         0] != "Unspecified"),
                           annotations))
