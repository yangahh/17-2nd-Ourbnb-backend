# 🏠 Team OurBnB 🏠


## Team Members 👥

- FE : 강민지, 김연주, 허혜성
- BE : 심규보, 양한아, 최호진

<br>

## 기술스택 🔧

- Python
- Django
- AQueryTool
- MySQL
- CORS Header
- PyJWT
- AWS S3, AWS EC2, AWS RDS
- Docker
- Git
- Kakao API

<br>

## 기능구현 ⌨️

#### 모델링 및 데이터 구성
- AQueryTool을 사용하여 DB모델링
![image](https://user-images.githubusercontent.com/49216894/115713189-b15a7880-a3b0-11eb-84f3-ab2dcdd8514b.png)

- 초기데이터 csv파일을 python 파일을 이용하여 업로드

#### 회원가입 & 로그인
- 카카오 로그인 API를 통해 소셜 로그인 기능 구현
- 로그인 시 JWT 토큰 발급
- login decorator를 만들어서 인가 확인

#### 숙소 리스트 및 상세 페이지
- Django ORM의 다양한 메소드를 활용하여 기능 구현
- select_related, prefetch_related를 통해 쿼리 성능 개선
- pagenation 구현

#### 결제
- 결제 페이지
- 결제 처리 및 결제 후 숙소에 예약 날짜 반영 기능 구현

#### 마이페이지
- 하나의 API로 현재 날짜 기준으로 예약 내역 확인 기능 구현

#### 호스트 숙소 등록
- AWS의 S3를 연동하여 다중 이미지 업로드 기능 구현

#### 각 기능별 Unit-test 작성
- 외부 API 및 S3연동 부분은 파이썬 unittest모듈의 patch와 MagicMock을 활용하여 unit test 구현
- setUpTestDate 클래스 메소드를 사용하여 unit-test 성능 개선

<br>

## Reference
- 이 프로젝트는 airbnb 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.


