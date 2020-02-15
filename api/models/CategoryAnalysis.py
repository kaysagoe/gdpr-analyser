class CategoryAnalysis:
    def __init__(self):
        self.firstPartyCollection = set()
        self.thirdPartySharing = set()
        self.userChoice = set()
        self.accessEditDelete = set()
        self.policyChange = set()

    def insert(self, category, index):
        if category == "Edit and Deletion":
            self.accessEditDelete.add(index)
        elif category == "First Party Collection/Use":
            self.firstPartyCollection.add(index)
        elif category == "Policy Change":
            self.policyChange.add(index)
        elif category == "Third Party Sharing/Collection":
            self.thirdPartySharing.add(index)
        elif category == "User Access":
            self.accessEditDelete.add(index)

    def count(self):
        return len(self.firstPartyCollection) + len(self.thirdPartySharing) + len(self.userChoice) \
               + len(self.policyChange)
