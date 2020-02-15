from bs4 import BeautifulSoup


class Cleaner:
    relevant_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "ul", "p"]

    @staticmethod
    def clean(text):
        soup = BeautifulSoup(text, "lxml")
        selected_tags = soup.find_all(Cleaner.relevant_tags)
        for i in range(len(selected_tags)):
            if selected_tags[i].name == "ul":
                for j in range(len(selected_tags[i].contents)):
                    if selected_tags[i].contents[j].name == "li":
                        selected_tags[i].contents[j].string = selected_tags[i].contents[j].get_text()
            else:
                if selected_tags[i].get_text().strip() != "":
                    selected_tags[i].string = selected_tags[i].get_text()
        return selected_tags
