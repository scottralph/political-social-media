from unittest import TestCase

from congresstweets.Parsing.TweetParser import TweetParser


class TestTweetParser(TestCase):
    def test_extract_mentions(self):
        parser = TweetParser()
        test_input = "Did you see where @Bob tweeted about that thing that @Ted did?"
        result = parser.extract_mentions(test_input)
        self.assertEquals(result[0], ['Bob', 'Ted'])
        self.assertEquals(result[1], "Did you see where  tweeted about that thing that  did?")


    def test_extract_urls(self):
        parser = TweetParser()
        test_input = "this is one http://foo.bar and another https://bert.com okay?"
        result = parser.extract_urls(test_input)
        self.assertEquals(result[0], ['http://foo.bar', 'https://bert.com'])

    def test_find_hash_tags(self):
        parser = TweetParser()
        test_intput = "This is a #test of the #wonderful #hashtag parsing"
        result = parser.get_hash_tags(test_intput)
        self.assertEquals(result, ['test', 'wonderful', 'hashtag'])

