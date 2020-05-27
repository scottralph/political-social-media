from unittest import TestCase

from congresstweets.Parsing.TweetParser import TweetParser


class TestTweetParser(TestCase):
    def test_extract_mentions(self):
        parser = TweetParser()
        test_input = "Did you see where @Bob tweeted about that thing that @Ted did?"
        result = parser.extract_mentions(test_input)
        self.assertEquals(result[0], ['Bob', 'Ted'])
        self.assertEquals(result[1], "Did you see where tweeted about that thing that did?")

    def test_extract_urls(self):
        parser = TweetParser()
        test_input = "this is one http://foo.bar and another https://bert.com okay?"
        result = parser.extract_urls(test_input)
        self.assertEquals(result[0], ['http://foo.bar', 'https://bert.com'])

    def test_find_hash_tags(self):
        parser = TweetParser()
        test_input = "This is a #test of the #wonderful #hashtag parsing"
        result = parser.get_hash_tags(test_input)
        self.assertEquals(result, ['test', 'wonderful', 'hashtag'])

    def test_splitting_sentences(self):
        parser = TweetParser()
        test_input = "This is the first. Is this the #second? \nThis is also one. sudden"
        split = parser.break_into_sentences(test_input)
        self.assertEquals(split, ["This is the first", "Is this the second", "This is also one", "sudden"])
        pass

    def test_punctuation_removal(self):
        text = "This is a test, and this is another - When: hello (there) ; bogus"
        punct_removed = TweetParser.remove_punctuation(text)
        self.assertEquals(punct_removed, 'This is a test and this is another  When hello there  bogus')

    def test_tokenization(self):
        tweet = {
            "id": "1263325482554142721",
            "screen_name": "RashidaTlaib",
            "user_id": "435331179",
            "time": "2020-05-21T00:27:21-04:00",
            "link": "https://www.twitter.com/RashidaTlaib/statuses/1263325482554142721",
            "text": "I have been telling people for weeks. Outside of Congress, there is broad support for direct relief. #ABCAct \n\nThey only follow polls that fit the desires of their corporate donors, not the actual people who vote them into office. Sad. https://twitter.com/Ilhan/status/1263218052868509697 QT @Ilhan 82% of the country supports monthly relief checks.\n\nEighty. Two. Percent.\n\nWe need to stop making excuses and get money into people's pockets every month. \n\nI have a bill to do just that! https://omar.house.gov/media/press-releases/rep-omar-introduces-bold-package-address-coronavirus-crisis-1000-every-adult https://twitter.com/zackafriedman/status/1262835440853364736",
            "source": "Twitter for Android"
        }
        parser = TweetParser()
        parser.tokenize_tweet(tweet)
        expectedTokens = ['I have been telling people for weeks',
                    'Outside of Congress there is broad support for direct relief',
                    'ABCAct',
                    'They only follow polls that fit the desires of their corporate donors not the actual people who vote them into office',
                    'Sad', 'QT 82% of the country supports monthly relief checks',
                    'Eighty',
                    'Two',
                    'Percent',
                    "We need to stop making excuses and get money into people's pockets every month",
                    'I have a bill to do just that']
        self.assertEquals(tweet['tokens'], expectedTokens)
        self.assertEquals(tweet['mentions'], ["Ilhan"])
        self.assertEquals(tweet['URLs'], ['https://twitter.com/Ilhan/status/1263218052868509697',
                                          'https://omar.house.gov/media/press-releases/rep-omar-introduces-bold-package-address-coronavirus-crisis-1000-every-adult',
                                          'https://twitter.com/zackafriedman/status/1262835440853364736'])



