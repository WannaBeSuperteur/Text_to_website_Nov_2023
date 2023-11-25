# convert input text to website

import openai

f = open('api_key.txt', 'r')
apikey = f.readlines()[0] # OpenAI API KEY
openai.api_key = apikey
f.close()

import os
import base64
import requests

header = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {apikey}'
}


# 입력 텍스트를 5장의 이미지로 변환하는 함수
def convert_text_to_image(input_text):

    num = 5 # 이미지 개수 (1분당 5장 초과의 경우 오류 발생)

    # DALL-E API를 통해 이미지를 요청하는 부분
    response = openai.Image.create(
        prompt = f'a wireframe of website with {input_text}',
        n = num,
        size = '1024x1024'
    )

    # 생성된 이미지의 링크 목록
    image_urls = [response['data'][x]['url'] for x in range(num)]

    # 생성된 이미지의 링크 출력 및 반환
    for i in range(num):
        print(f'\nresult image url:\n{image_urls[i]}')

    return image_urls


# 이미지를 읽어서 웹사이트로 변환하는 함수
# gpt-4-vision-preview API로 이미지에 대한 HTML 코드를 요청해서 결과 읽기
def convert_image_to_website(image_urls):

    prompt = 'Write an HTML code for the website with the wireframe image.'
    openai_api_url = 'https://api.openai.com/v1/chat/completions'

    # OpenAI API로 요청하는 함수
    def request_to_openai_api(url):
        payload = {
            'model': 'gpt-4-vision-preview',
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {'url': url}
                        }
                    ]
                }
            ],
            'max_tokens': 3585
        }

        response = requests.post(url=openai_api_url, headers=header, json=payload)
        print(f'\nresponse:\n{response.json()}')

        return response.json()

    # 각 URL마다 OpenAI API (gpt-4-vision-preview) 로 요청한 HTML 코드 받기
    resps = []
    
    for url in image_urls:
        resp = request_to_openai_api(url)
        resps.append(resp)

    return resps


# 입력 텍스트를 이미지로 바꾸고, 그 이미지를 웹사이트로 변환
def convert_text_to_website(input_text):

    # 텍스트 -> 이미지 변환
    image_urls = convert_text_to_image(input_text)

    # 이미지 -> 웹사이트 변환
    website_html_codes = convert_image_to_website(image_urls)
