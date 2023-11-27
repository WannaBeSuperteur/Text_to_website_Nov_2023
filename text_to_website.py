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

num = 5 # 이미지 개수 (1분당 5장 초과의 경우 오류 발생)


# 입력 텍스트를 5장의 이미지로 변환하는 함수
def convert_text_to_image(input_text):

    # DALL-E API를 통해 이미지를 요청하는 부분
    response = openai.Image.create(
        prompt = f'Draw a detailed wireframe of website that shows {input_text}. Draw in detail so that web developers can create website.',
        n = num,
        size = '1024x1024'
    )

    # 생성된 이미지의 링크 목록
    image_urls = [response['data'][x]['url'] for x in range(num)]

    # 생성된 이미지의 링크 반환
    return image_urls


# 5장의 각 이미지를 읽어서 웹사이트의 HTML 코드로 변환하는 함수
# gpt-4-vision-preview API로 이미지에 대한 HTML 코드를 요청해서 결과 읽기
def convert_image_to_website(image_urls, input_text):

    prompt = f'Write an HTML code for the website with the wireframe image. The website shoud show {input_text}.'
    openai_api_url = 'https://api.openai.com/v1/chat/completions'

    # OpenAI API로 요청하는 함수
    def request_to_openai_api(url):
        try_count = 0

        while try_count < 10:
            try:
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
                response = response.json()
                answer_content = response['choices'][0]['message']['content']

                if '```' in answer_content:
                    return answer_content.split('```')[1]

                else:
                    return ''

            except Exception as e:
                print(f'error: {e}')
                try_count += 1
                

    # 각 URL마다 OpenAI API (gpt-4-vision-preview) 로 요청한 HTML 코드 받기
    html_codes = []
    
    for idx, url in enumerate(image_urls):
        print(f'{idx} / {num}')
        
        html_code = request_to_openai_api(url)
        html_codes.append(html_code)

    return html_codes


# 입력 텍스트를 이미지로 바꾸고, 그 이미지를 웹사이트의 HTML 코드로 변환
def convert_text_to_website(input_text):

    # 텍스트 -> 이미지 변환
    print('converting text to image ...')
    image_urls = convert_text_to_image(input_text)

    # 이미지 (5장) -> 웹사이트 (총 5개) HTML 코드 변환
    print('converting images to website codes ...')
    website_html_codes = convert_image_to_website(image_urls, input_text)

    return website_html_codes
