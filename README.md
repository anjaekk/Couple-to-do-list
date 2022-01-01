# Couple to do list
최종 목표는 Couple to do list를 만드는 것이나 공부해보고 싶은 기능들을 이것, 저것 구현하면서 하다보니 언제 완성될지는 미정입니다!

<br/> 
<br/> 

## 기술 스택
Python, Django(Django-REST-framework), MySQL     
Docker compose

<br/> 
<br/> 

## 현 기능
- 회원가입시 비밀번호 유효성 검사
- 리스트 조회시 Pagination
- 비밀번호 set_password()를 이용하여 해싱 저장
- 기존에 팔로우 한사람을 재팔로우시 팔로우가 취소되도록 구현
- 마이페이지에선 팔로우와 팔로잉 수 확인 가능하고 팔로우와 팔로잉 엔드포인트를 따로 두어 확인하도록 구현
- Timestamp(created_at, updated_at) table을 추상화하고 User table에서 상속받도록 구현 

<br/> 
<br/> 

## API 명세
### API 명세 링크(Postman)
🔗 [API 명세 바로가기](https://documenter.getpostman.com/view/16450829/UUxxgUAt)

### 구현한 API 리스트


|HTTP method|URI|Description|
|:-:|:-:|:-:|
|POST|/users/signup|회원가입|
|POST|/users/login|로그인|
|POST|/users/logout|로그아웃|
|GET|/users|전체 유저 리스트 조회|
|POST|/users/{user_id}/follow|특정 유저 팔로우|
|GET|/users/{user_id}|마이페이지 조회|
|GET|/users/{user_id}/follower|특정 유저 팔로우 리스트 조회|
|GET|/users/{user_id}/following|특정 유저 팔로잉 리스트 조회|

<br/> 
<br/> 
