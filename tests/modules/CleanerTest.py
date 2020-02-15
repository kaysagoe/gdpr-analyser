import unittest

from api.modules.Cleaner import Cleaner


class CleanerTest(unittest.TestCase):
    def test_should_sanitise_text_tags(self):
        source = """
            <h1>Heading <span>Tag</span></h1>
            <p>Paragraph <a href="#">Tag</a></p>
            <p>Paragraph tag with<img src="#" alt="description"/> image</p>
        """
        tags = Cleaner.clean(source)

        self.assertEqual(tags[0].string, "Heading Tag")
        self.assertEqual(tags[1].string, "Paragraph Tag")
        self.assertEqual(tags[2].string, "Paragraph tag with image")

    def test_should_sanitise_li_tags_ul_tag(self):
        source = """
            <ul><li>List item tag 1</li><li>List <code>item tag 2</code></li></ul>
        """
        tags = Cleaner.clean(source)

        self.assertEqual(tags[0].contents[0].string, "List item tag 1")
        self.assertEqual(tags[0].contents[1].string, "List item tag 2")


if __name__ == '__main__':
    unittest.main()
