# 📚 Movie-based Book Recommendation System

## 🌟 Project Overview | 프로젝트 개요
This project is designed to recommend books based on movies that a user enjoys. It utilizes a dataset of approximately 14,000 movies and 2,000 books. The system uses collaborative filtering, content-based filtering, and hybrid models to provide personalized book recommendations.

이 프로젝트는 사용자가 좋아하는 영화를 바탕으로 도서를 추천하는 시스템입니다. 약 14,000개의 영화 데이터와 2,000권의 도서 데이터를 기반으로 협업 필터링, 콘텐츠 기반 필터링, 그리고 하이브리드 모델을 사용하여 개인화된 도서 추천을 제공합니다.


## 🧑‍🤝‍🧑 **Team member | 팀원**
- **비타민 13기 : 서영우, 이형석, 한재선**
- **비타민 14기 : 박예슬, 이채연**

## 📅 **Progress period | 진행 기간**
- **2024.07.13 ~ 2024.08.30**

## 📊 Data collection | 데이터 수집
- **Book rating data | 도서 평점 데이터 : Aladin**
- **Book data | 도서 데이터 : 도서관 정보나루 API**
- **Movie data | 영화 데이터 : Naver** 
## 🚀 Features | 기능 소개
- **Movie Data Analysis | 영화 데이터 분석**: Extract key information and features from movie data.
- **Book Recommendation System | 도서 추천 시스템**: Recommend books based on the similarity between movies and books.
- **Model Performance Evaluation | 모델 성능 평가**: Evaluate the performance of various recommendation models.

## 📂 Project Structure | 프로젝트 구조
![Project Structure | 프로젝트 구조도](./static/architecture.png)

### 📁 Key Directories and Files | 주요 디렉토리 및 파일
- `data/`: Movie and book data files. | 영화 및 도서 데이터 파일.
- `models/`: Recommendation model scripts. | 추천 모델 관련 코드.
- `notebooks/`: Data analysis and model training Jupyter notebooks. | 데이터 분석 및 모델 학습 Jupyter 노트북.
- `scripts/`: Data preprocessing and utility scripts. | 데이터 전처리 및 유틸리티 스크립트.
- `static/`: Static files such as images. | 정적 파일 (이미지 등).
- `tests/`: Test scripts. | 테스트 코드.
- `docs/`: Documentation files. | 문서화 파일들.

## 🛠️ Installation and Execution | 설치 및 실행 방법
Follow these steps to run the project locally. | 프로젝트를 로컬에서 실행하기 위해 아래 단계를 따라 주세요.

1. **Clone the repository | 저장소 클론**:
    ```bash
    git clone https://github.com/username/movie-book-recommendation.git
    cd movie-book-recommendation
    ```

2. **Install required packages | 필수 패키지 설치**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the project | 프로젝트 실행**:
    ```bash
    python main.py
    ```

## 📖 Usage | 사용 방법
- Explore data analysis methods in the `EDA.ipynb` notebook. | `EDA.ipynb` 노트북에서 데이터 분석 방법을 확인할 수 있습니다.
- Follow the model training and validation process in the `model_training.ipynb` notebook. | `model_training.ipynb` 노트북에서 모델 학습 및 검증 과정을 따라갈 수 있습니다.

## 📜 License | 라이선스
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details. | 이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참고하세요.
