from api.models.Annotation import Annotation


class Segmenter:
    @staticmethod
    def segment(tags):
        segments = Segmenter.segment_by_structure(tags)
        annotations = list()
        for segment in segments:
            annotations.append(Annotation(segment))
        return annotations

    @staticmethod
    def segment_by_structure(tags):
        segments = []
        temp_string = ""
        i = 0
        while i < len(tags):
            if tags[i].get_text().strip() != "":
                if tags[i].name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                    temp_string = temp_string + tags[i].string.strip() + "\n"
                elif tags[i].name == "p":
                    if tags[i].string.strip()[-1] == ":" and tags[i + 1].name == "ul":
                        temp_string = temp_string + tags[i].string.strip()
                    else:
                        temp_string = temp_string + tags[i].string.strip()
                        segments.append(temp_string)
                        temp_string = ""
                elif tags[i].name == "ul":
                    if i > 0 and (tags[i - 1].name == "p" and (
                            tags[i - 1].string is not None and tags[i - 1].string.strip() != "") and
                                  tags[i - 1].string.strip()[-1] == ":"):
                        items_to_concatenate = []
                        for j, item_tag in enumerate(tags[i].contents):
                            if item_tag.string is not None:
                                if len(item_tag.string.split()) > 20:
                                    temp_string = tags[i - 1].string.strip() + "\n" + item_tag.string.strip()
                                    segments.append(temp_string)
                                    temp_string = ""
                                else:
                                    items_to_concatenate.append(j)
                        temp_string = tags[i - 1].string.strip() + "\n"
                        for j in items_to_concatenate:
                            temp_string = temp_string + tags[i].contents[j].string.strip() + "\n"

                        if len(items_to_concatenate) > 0:
                            segments.append(temp_string)
                        temp_string = ""
                    else:
                        temp_string = ""
            i += 1
        return segments
