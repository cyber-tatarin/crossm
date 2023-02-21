import os
import openai
from abc import ABC, abstractmethod
import requests

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
		translated_response = requests.request("GET", url, headers=headers, params=querystring)
		return translated_response.json()['responseData']['translatedText']

	def get_ai_response(self):
		response = openai.Completion.create(
			model="text-davinci-003",
			prompt=self.generate_prompt(),
			temperature=1,
			max_tokens=300,
			top_p=0,
			frequency_penalty=1.2,
			presence_penalty=1.2,
		)
		text_from_response = response['choices'][0]['text']
		result = self.translate(response=text_from_response)
		return result


class GenerateCouponIdeas(GenerateCrossmAdviceBase):
	def generate_prompt(self):
		return f'I own a {self.company} in Belarus. What the most high-margin do I have services, so that ' \
			   f'I can issue  cheap coupons for cross-marketing partners? Write 6 options with the word free or ' \
			   f'with a discount greater than 90% written in numbers'

		# return f'Я владею {self.company}. Какие у меня могут быть самые ' \
		# 	   f'высокомаржинальные услуги, чтобы я выдал на них ' \
		# 	   f'дешевые купоны партнерам по кросс-макетингу? Я живу в Беларуси, тут ' \
		# 	   f'людей интересуют только бесплатные или очень дешевые вещи. Напиши 6 вариантов ' \
		# 	   f'со словом бесплатно или с очень большой скидкой, написанной числами'


class GeneratePossiblePartners(GenerateCrossmAdviceBase):
	def generate_prompt(self):
		return ''


class AiGeneratorChooser:
	g_dict = {'generate_coupon_ideas': GenerateCouponIdeas,
			  'generate_possible_partners': GeneratePossiblePartners,
			  }

	def __init__(self, *args, g_type, company, lang):
		print(g_type)
		self.g_class = self.g_dict[g_type]
		self.g_instance = self.g_class(company=company, lang=lang)

	def execute(self):
		return self.g_instance.get_ai_response()



