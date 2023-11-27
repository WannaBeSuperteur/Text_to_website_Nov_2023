import text_to_website as t2w

if __name__ == '__main__':

    # 텍스트 입력
    print('input text for creating website :')
    input_text = input()

    # 텍스트를 이미지 (총 5장) 로, 각 이미지를 웹사이트의 HTML 코드로 변환
    html_codes = t2w.convert_text_to_website(input_text)
    input_text_with_underbar = input_text.replace(' ', '_')

    # HTML 코드 (최대 5개 생성) 쓰고 파일로 저장
    for idx, code in enumerate(html_codes):
        if len(code) < 10:
            print(f'({idx}) HTML code is empty or too short.')

        else:
            try:
                f = open(f'website_{input_text_with_underbar}_{idx}.html', 'w')
                f.write(code)
                f.close()

            except Exception as e:
                print(f'error: {e}')
