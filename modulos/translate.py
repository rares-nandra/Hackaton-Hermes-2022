import translators as ts

class Translate():
    def traducere(self, element, language):
        result = ts.google(element, from_language='en', to_language=language)
        return result
        