import httpx
import asyncio
import csv
import xlsxwriter

# API 정보
auth_key = '''YOUR API KEY'''
base_url = 'http://data4library.kr/api/loanItemSrch?format=json'
output_csv = '/kaggle/working/popular_books.csv'
output_xlsx = '/kaggle/working/popular_books.xlsx'

#2010-01-01 ~ 2024-08-10 기간의 문학 인기 도서 2000권 수집
async def fetch_books(page_no, auth_key):
    url = f"{base_url}&kdc=8&authKey={auth_key}&startDt=2010-01-01&endDt=2024-08-10&pageNo={page_no}&pageSize=200"
    print(f"\n[Request URL] {url}\n")
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # 'docs' 필드가 응답에 있는지 확인
            if 'response' in data and 'docs' in data['response']:
                books = []
                for doc in data['response']['docs']:
                    # 각 doc 필드 접근
                    doc_info = doc['doc'] if 'doc' in doc else {}
                    book_data = {
                        "순위": doc_info.get('ranking', 'N/A'),
                        "도서명": doc_info.get('bookname', 'N/A'),
                        "저자명": doc_info.get('authors', 'N/A'),
                        "출판사": doc_info.get('publisher', 'N/A'),
                        "출판년도": doc_info.get('publication_year', 'N/A'),
                        "ISBN": doc_info.get('isbn13', 'N/A'),
                        "주제분류명": doc_info.get('class_nm', 'N/A'),
                        "대출건수": doc_info.get('loan_count', 'N/A')
                    }
                    books.append(book_data)
                    print(f"순위: {book_data['순위']} | 도서명: {book_data['도서명']}")
                return books
            else:
                print("응답에 'docs' 필드가 없습니다.")
                return []
        except httpx.TimeoutException:
            print("요청 시간이 초과되었습니다.")
            return []
        except httpx.RequestError as e:
            print(f"요청 실패: {e}")
            return []
        
async def main():
    page_no = 1
    all_books = []

    while True:
        print(f"페이지 가져오는 중: {page_no}")
        books = await fetch_books(page_no, auth_key)
        if not books:
            break
        all_books.extend(books)
        if page_no == 10: # 임시로 n페이지까지만 가져오도록 설정
            break
        page_no += 1

    # CSV 파일로 저장
    if all_books:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["순위", "도서명", "저자명", "출판사", "출판년도", "ISBN", "주제분류명", "대출건수"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in all_books:
                writer.writerow(book)
        print(f"CSV 파일로 저장 완료: {output_csv}")

        # Excel 파일로 저장
        workbook = xlsxwriter.Workbook(output_xlsx)
        worksheet = workbook.add_worksheet()

        # 헤더 작성
        for col_num, header in enumerate(fieldnames):
            worksheet.write(0, col_num, header)
        
        # 데이터 작성
        for row_num, book in enumerate(all_books, start=1):
            for col_num, field in enumerate(fieldnames):
                worksheet.write(row_num, col_num, book[field])
        
        workbook.close()
        print(f"Excel 파일로 저장 완료: {output_xlsx}")
    else:
        print("저장할 데이터가 없습니다.")

# 현재 이벤트 루프가 이미 실행 중인지 확인하고, 아니면 새로 실행
loop = asyncio.get_event_loop()
if loop.is_running():
    # 현재 실행 중인 루프에서 직접 실행
    task = loop.create_task(main())
    await task
else:
    # 새로운 루프를 실행
    asyncio.run(main())
