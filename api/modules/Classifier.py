from simpletransformers.classification import MultiLabelClassificationModel

from api.models.ClassifierType import ClassifierType
from api.models.CategoryAnalysis import CategoryAnalysis
from api.models.Annotation import Annotation
from typing import List

from api.models.Config import config


class Classifier:
    filePath = config.get("path")
    classes = {
        ClassifierType.CATEGORY: ["Edit and Deletion", "Data Retention", "Data Security", "Do Not Track",
                                  "First Party Collection/Use", "International and Specific Audiences",
                                  "Introductory/Generic", "Policy Change", "Practice not covered",
                                  "Privacy contact information", "Third Party Sharing/Collection", "User Access",
                                  "User Choice/Control"],
        ClassifierType.CHANGE_TYPE: ["Non-privacy relevant change", "Privacy relevant change",
                                     "In case of merger or acquisition", "Unspecified"],
        ClassifierType.CHOICE_TYPE: ["Dont use service/feature", "Opt-in", "Opt-out link",
                                     "Opt-out via contacting company",
                                     "First-party privacy controls", "Third-party privacy controls",
                                     "Browser/device privacy controls", "Unspecified"],
        ClassifierType.NOTIFICATION_TYPE: ["No notification", "General notice in privacy policy",
                                           "General notice on website", "Personal notice", "Unspecified"],
        ClassifierType.PERSONAL_INFORMATION_TYPE: ["Financial", "Health", "Contact", "Location", "Demographic",
                                                   "Personal identifier", "User online activities", "User Profile",
                                                   "IP address and device IDs", "Cookies and tracking elements",
                                                   "Computer information", "Survey data",
                                                   "Generic personal information",
                                                   "Unspecified", "Social media data"],
        ClassifierType.PURPOSE: ["Basic service/feature", "Additional service/feature", "Advertising",
                                 "Marketing", "Analytics/Research", "Personalization/Customization",
                                 "Service Operation and Security", "Legal requirement", "Merger/Acquisition",
                                 "Unspecified"],
        ClassifierType.THIRD_PARTY_ENTITY: ["Unnamed third party", "Named third party",
                                            "Other part of company/affiliate",
                                            "Other users", "Public", "Unspecified"]
    }

    @staticmethod
    def run(annotations: List[Annotation]):
        annotations, analysis = Classifier.predict(annotations, ClassifierType.CATEGORY)

        firstPartyCollectionAnnotations = [annotations[index] for index in analysis.firstPartyCollection]
        Classifier.predict(firstPartyCollectionAnnotations, ClassifierType.PURPOSE)
        Classifier.predict(firstPartyCollectionAnnotations, ClassifierType.PERSONAL_INFORMATION_TYPE)
        Classifier.predict(firstPartyCollectionAnnotations, ClassifierType.CHOICE_TYPE)

        thirdPartySharingAnnotations = [annotations[index] for index in analysis.thirdPartySharing]
        Classifier.predict(thirdPartySharingAnnotations, ClassifierType.THIRD_PARTY_ENTITY)

        policyChangeAnnotations = [annotations[index] for index in analysis.policyChange]
        Classifier.predict(policyChangeAnnotations, ClassifierType.CHANGE_TYPE)
        Classifier.predict(policyChangeAnnotations, ClassifierType.NOTIFICATION_TYPE)

        return annotations, analysis

    @staticmethod
    def predict(annotations: List[Annotation], classifier: ClassifierType):
        texts = [annotation.text for annotation in annotations]

        model = MultiLabelClassificationModel('bert', f"{Classifier.filePath}/{classifier.value}-classifier/",
                                              num_labels=len(Classifier.classes[classifier]), use_cuda=False, args={"no_cache": True})
        predictions, _ = model.predict(texts)

        analysis = None
        if classifier is ClassifierType.CATEGORY:
            analysis = CategoryAnalysis()

        for annotation_index in range(len(annotations)):
            for pred_index in range(len(predictions[annotation_index])):
                category = Classifier.classes[classifier][pred_index]
                if predictions[annotation_index][pred_index] is 1 and classifier is ClassifierType.CATEGORY:
                    annotations[annotation_index].categories.append(category)
                    analysis.insert(category, annotation_index)

                    if category == "First Party Collection/Use":
                        annotations[annotation_index].attributes[ClassifierType.PURPOSE.value] = []
                        annotations[annotation_index].attributes[ClassifierType.PERSONAL_INFORMATION_TYPE.value] = []
                        annotations[annotation_index].attributes[ClassifierType.CHOICE_TYPE.value] = []
                    elif category == "Third Party Sharing/Collection":
                        annotations[annotation_index].attributes[ClassifierType.THIRD_PARTY_ENTITY.value] = []
                    elif category == "Policy Change":
                        annotations[annotation_index].attributes[ClassifierType.CHANGE_TYPE.value] = []
                        annotations[annotation_index].attributes[ClassifierType.NOTIFICATION_TYPE.value] = []

                elif predictions[annotation_index][pred_index] is 1 and classifier is not ClassifierType.CATEGORY:
                    value = Classifier.classes[classifier][pred_index]
                    if classifier.value in annotations[annotation_index].attributes:
                        annotations[annotation_index].attributes[classifier.value].append(value)
                    else:
                        annotations[annotation_index].attributes[classifier.value] = [value]
        return annotations, analysis
