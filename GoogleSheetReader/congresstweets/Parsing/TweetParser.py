import re

mentionRE = re.compile(r"@\w+(?:\s+|$)")
urlRE = re.compile(r"https?://\S+(?:\s+|$)")
hashTagRE = re.compile(r"#(\w+)(?:\s+|$)")
sentenceRE = re.compile(r"\w+[.!?\n$]")


class TweetParser:

    @staticmethod
    def extract_mentions(tweet_text):
        all_mentions = re.findall(mentionRE, tweet_text)
        replaced = tweet_text
        for mention in all_mentions:
            replaced = replaced.replace(mention, "")
        all_mentions = list(map(lambda x: x[1:].strip(), all_mentions))
        return all_mentions, replaced

    @staticmethod
    def extract_urls(tweet_text):
        all_urls = list(map(lambda x: x.strip(), re.findall(urlRE, tweet_text)))
        replaced = tweet_text
        for url in all_urls:
            replaced = replaced.replace(url, "")
        return all_urls, replaced

    @staticmethod
    def get_hash_tags(tweet_text):
        return re.findall(hashTagRE, tweet_text)

    @staticmethod
    def break_into_sentences(text):
        def yield_func(input_string):
            current = ""
            for c in input_string:
                if c == '.' or c == '?' or c == '\n' or c == '!' or c == '\"' or c == '\n':
                    result = current.strip()
                    current = ""
                    if len(result) > 0:
                        yield result.strip()
                else:
                    # Don't pass the hash-tag symbol, or other
                    if c != '#':
                        current = current + c
            remainder = current.strip()
            if len(remainder) > 0:
                yield remainder

        sentences = list(yield_func(text))
        return sentences

    @staticmethod
    def remove_punctuation(text):
        punct = {'.', ',', ':', ';', '-', '"', '`', '(', ')', '+', '<', '>'}
        r = ""
        for t in text:
            if t not in punct:
                r = r + t
        return r

    @staticmethod
    def tokenize_tweet(tweet):
        text = tweet['text']
        mentions, mentions_removed = TweetParser.extract_mentions(text)
        tweet['mentions'] = mentions
        urls, urls_removed = TweetParser.extract_urls(mentions_removed)
        tweet['URLs'] = urls
        tweet['hash_tags'] = TweetParser.get_hash_tags(text)
        sentences = TweetParser.break_into_sentences(urls_removed)
        tokens = list(map(lambda x: TweetParser.remove_punctuation(x), sentences))
        tweet['tokens'] = tokens
