from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
import numpy as np

# 파일 경로 설정
file_path = './popular_books_with_analysis.xlsx'

# '도서명'에서 ':' 기준으로 split 후 첫 번째 부분 저장, '장편소설', '단편소설'을 공백으로 대체하고 영어, '/', '='을 제거하는 함수
def clean_title(title):
    title = title.split(':')[0].replace('장편소설', '').replace('단편소설', '').strip()
    title = re.sub(r'[a-zA-Z/=\']', '', title)
    return title.strip()

# 셀레니움 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# 셀레니움으로 알라딘 접속
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.aladin.co.kr/home/welcome.aspx')

# 데이터를 50권씩 처리하기 위해 시작 인덱스와 끝 인덱스 설정
start_idx = 0
batch_size = 50

# 무한 루프를 사용하여 계속해서 50권씩 데이터를 수집
while True:
    # 엑셀 파일에서 데이터 로드
    df = pd.read_excel(file_path)
    
    # '검색용 도서명'이 존재하지 않으면 새로 생성
    if '검색용 도서명' not in df.columns:
        df['검색용 도서명'] = df['도서명'].apply(clean_title)

    # 처리할 도서명 리스트 추출
    book_titles = df['검색용 도서명'].tolist()[start_idx:start_idx + batch_size]
    
    # 결과 저장 리스트 초기화
    results = []

    # 50권씩 도서명 검색 및 결과 추출
    for title in book_titles:
        search_box = driver.find_element('id', 'SearchWord')
        search_box.clear()
        search_box.send_keys(title)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(0.5)
        
        try:
            book_elements = driver.find_elements('css selector', '.ss_book_box')
            
            for book_element in book_elements:
                if 'eBook' in book_element.text:
                    continue
                
                try:
                    cover_image_link = book_element.find_element('css selector', '.cover_area_other a img').find_element('xpath', '..')
                except:
                    try:
                        cover_image_link = book_element.find_element('css selector', '.cover_area a').find_element('xpath', '..')
                    except:
                        print(f"이미지 링크를 찾을 수 없습니다: {title}")
                        continue
                
                cover_image_link.click()
                time.sleep(1)
                
                book_name = driver.find_element('css selector', '.Ere_bo_title').text.strip()
                
                try:
                    # 평점을 텍스트로 추출한 후 실수로 변환 시도
                    book_rating = driver.find_element('css selector', '.Ere_sub_pink.Ere_fs16.Ere_str').text.strip()
                    book_rating = float(book_rating)  # 실수형으로 변환
                except:
                    book_rating = np.nan  # 평점이 없을 경우 NaN으로 처리
                
                results.append({'결과 도서명': book_name, '평점': book_rating})
                print(f"결과 도서명: {book_name}, 평점: {book_rating}")
                
                driver.back()
                time.sleep(0.1)
                break
        
        except Exception as e:
            results.append({'결과 도서명': None, '평점': np.nan})
            print(f"{title}에 대한 검색 결과를 가져오는 데 문제가 발생했습니다: {e}")

    # 수집한 결과를 DataFrame으로 변환
    result_df = pd.DataFrame(results)
    
    # 기존 데이터프레임에 '결과 도서명'과 '평점' 열 추가
    if not result_df.empty:
        result_df.index = range(start_idx, start_idx + len(result_df))  # 인덱스를 맞춰줌
        
        df.loc[result_df.index, '결과 도서명'] = result_df['결과 도서명']
        df.loc[result_df.index, '평점'] = result_df['평점']
    
    # 수정된 데이터프레임을 엑셀 파일에 저장
    df.to_excel(file_path, index=False)
    print('임시 저장')
    # 다음 배치를 위해 시작 인덱스 증가
    start_idx += batch_size
    
    # 더 이상 처리할 도서명이 없으면 종료
    if start_idx >= len(df):
        break

# 작업 완료 후 드라이버 종료
driver.quit()

# 최종 결과 출력
print(f"결과가 파일에 저장되었습니다: {file_path}")
