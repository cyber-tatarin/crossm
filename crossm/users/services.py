import os
import openai
from abc import ABC, abstractmethod
import requests
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")
url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"
headers = {
    "X-RapidAPI-Key": os.getenv('X-RAPID_API_KEY'),
    "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"
}


class GenerateCrossmAdviceBase:
    def __init__(self, *args, company, lang):
        self.company = company
        self.lang = lang
    
    @abstractmethod
    def generate_prompt(self):
        pass
    
    def translate(self, response):
        querystring = {"langpair": f"en|{self.lang}", "q": response, "mt": "1"}
        try:
            translated_response = requests.request("GET", url, headers=headers, params=querystring)
            if translated_response.json()['responseData']['translatedText'] == 'QUERY LENGTH LIMIT EXCEEDED. ' \
                                                                               'MAX ALLOWED QUERY : 500 CHARS':
                return 'error'
            return translated_response.json()['responseData']['translatedText']
        except:
            return 'error'
    
    def get_ai_response(self):
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + os.getenv('OPENAI_API_KEY', ''),
            }
            
            json_data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'user',
                        'content': self.generate_prompt(),
                    },
                ],
                'temperature': 0.7,
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
        # response = openai.Completion.create(
        # 	model="text-davinci-003",
        # 	prompt=self.generate_prompt(),
        # 	temperature=1,
        # 	max_tokens=300,
        # 	top_p=0,
        # 	frequency_penalty=1.2,
        # 	presence_penalty=1.2,
        # )
            text_from_response = response.json()['choices'][0]['message']['content']
            
        except:
            return {'error': True}
        result = {'translated': self.translate(response=text_from_response), 'original': text_from_response}
        return result


class GenerateCouponIdeas(GenerateCrossmAdviceBase):
    def generate_prompt(self):
        return f'I own a {self.company} in Belarus. What the most high-margin do I have services, so that ' \
               f'I can issue  cheap coupons for cross-marketing partners? Briefly write 6 options with the word free or ' \
               f'with a discount greater than 90% written in numbers. Generate not more than 499 characters'

# return f'Я владею {self.company}. Какие у меня могут быть самые ' \
# 	   f'высокомаржинальные услуги, чтобы я выдал на них ' \
# 	   f'дешевые купоны партнерам по кросс-макетингу? Я живу в Беларуси, тут ' \
# 	   f'людей интересуют только бесплатные или очень дешевые вещи. Напиши 6 вариантов ' \
# 	   f'со словом бесплатно или с очень большой скидкой, написанной числами'


class GeneratePossiblePartners(GenerateCrossmAdviceBase):
    def generate_prompt(self):
        return f'I own a {self.company} in Belarus. What small business partners should I look for cross-marketing, not advertisement? ' \
               f'Write 6 best options without any description. I want to exchange coupons to increase my average check. Generate not more than 499 characters'


class AiGeneratorChooser:
    g_dict = {'generate_coupon_ideas': GenerateCouponIdeas,
              'generate_possible_partners': GeneratePossiblePartners,
              }
    
    def __init__(self, *args, g_type, company, lang):
        self.g_class = self.g_dict[g_type]
        self.g_instance = self.g_class(company=company, lang=lang)
    
    def execute(self):
        return self.g_instance.get_ai_response()
    

def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code
