import text_to_website as t2w

if __name__ == '__main__':

    # 텍스트 입력
    print('input text for creating website :')
    input_text = input()

    # 텍스트를 이미지로, 이미지를 웹사이트로 변환
    t2w.convert_text_to_website(input_text)
