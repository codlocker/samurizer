import http.client
import urllib.parse
import nltk.data
import xml.etree.ElementTree as ET


class Translator:
    host = 'api.microsofttranslator.com'
    path = '/V2/Http.svc/Translate'

    # supported indian languages list:
    # https://docs.microsoft.com/en-us/azure/cognitive-services/translator/languages
    language_dictionary = {
        'bengali': 'bn',
        'hindi': 'hi',
        'tamil': 'ta',
        'urdu': 'ur',
        'english': 'en'
    }

    def __init__(self) -> None:
        self.subscription_key = "dd4276f8cbba496c979b14d118862f8d"

    def _get_header(self) -> dict:
        return {'Ocp-Apim-Subscription-Key': self.subscription_key}

    def get_translated_text(self, text: str, language: str) -> str:
        header = self._get_header()
        conn = http.client.HTTPSConnection(self.host)
        try:
            language_code = self.language_dictionary[language.lower()]
            params = '?to=' + language_code + '&text=' + urllib.parse.quote(text)
            conn.request("GET", self.path + params, None, header)
            response = conn.getresponse()
            data = str(response.read().decode('utf-8'))
            print(data)
            text_data = ET.fromstring(data).text
            # print(text_data)
            return text_data
        except Exception as e:
            print(str(e))
            return ''

    def generate_summary(self, content, keywords):
        """
        content: original news article, full lengthed
        keywords: Key-phrases returned from Azure Text Analytics API
                  in the order of decreasing importance
        """
        summary = []
        content_length = str(content).count(' ')
        estimated_sent_min = max(1, int((content_length * 0.17) / 10))
        estimated_sent_max = int((content_length * 0.23) / 10)
        # print("estimated_sent_min, estimated_sent_max\n", estimated_sent_min, estimated_sent_max)
        keywords = keywords.split(',')
        keywords = keywords[:-1]
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(content)
        # print("sentences\n", sentences)
        keyword_idx = 0
        while (len(summary) < estimated_sent_min) and keyword_idx < len(keywords):
            # print("keywords[keyword_idx]\n", keywords[keyword_idx])
            candidates = [_ for _ in sentences if keywords[keyword_idx] in _]
            # print("candidates\n", candidates)
            if len(summary) > estimated_sent_max:
                break
            for candidate in candidates:
                if candidate not in summary:
                    summary.append(candidate)
            keyword_idx = keyword_idx + 1
        summary_text = ' '.join(summary)
        return summary_text
