# 🏠 Team OurBnB 🏠


## Team Members 👥

- FE : 강민지, 김연주, 허혜성
- BE : 심규보, 양한아, 최호진


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
- 다양한 필터링 옵션, pagenation

#### 결제
- 결제 페이지
- 결제 처리 및 결제 후 숙소에 예약 날짜 반영

#### 마이페이지
- 시간별 예약 내역 확인

#### 호스트 숙소 등록
- S3를 이용하여 다중 이미지 업로드 기능 구현


## Reference
- 이 프로젝트는 airbnb 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.


