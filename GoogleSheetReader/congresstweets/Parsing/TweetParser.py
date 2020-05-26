import re


mentionRE = re.compile(r"@\w+\s")
urlRE = re.compile(r"https?://\S+\s")
hashTagRE = re.compile(r"#(\w+)\s")


class TweetParser:

    @staticmethod
    def extract_mentions(tweet):
        all_mentions = re.findall(mentionRE, tweet)
        replaced = tweet
        for mention in all_mentions:
            replaced = replaced.replace(mention, "")
        all_mentions = list(map(lambda x: x[1:], all_mentions))
        return all_mentions, replaced

    @staticmethod
    def extract_urls(tweet):
        all_urls = re.findall(urlRE, tweet)
        replaced = tweet
        for url in all_urls:
            replaced = replaced.replace(url, "")
        return all_urls, replaced

    @staticmethod
    def get_hash_tags(tweet):
        return re.findall(hashTagRE, tweet)



