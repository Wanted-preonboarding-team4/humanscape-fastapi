# [Assignment 4] 8PERCENT  

## 팀원  
| **이름** | **Github Link** |
|:------|:-------------|
| 강대훈 | https://github.com/daehoon12 |
| 김훈태 | https://github.com/kim-hoontae |
| 이무현 | https://github.com/PeterLEEEEEE |



## 과제  안내

### Documentation API  

### 모델링  
![image](https://user-images.githubusercontent.com/32921115/142034117-6a11471b-7906-4d7b-bb52-a237b4f50080.png)  


### API 목록
- 수집한 임상정보 리스트 API (특정 임상정보 읽기(키 값은 자유))
- 수집한 임상정보에 대한 API (최근 일주일내에 업데이트(변경사항이 있는) 된 임상정보 리스트)


### 상세설명

---

**1)** 임상정보를 수집하는 **batch task**  

- 공공기관의 Open API를 매 주기마다 가져오게 했습니다.

거래내역 API는 다음을 만족해야 합니다.


**2)**- 수집한 임상정보에 대한 **API**  
- 특정 임상정보 읽기(키 값은 자유)  


**3)** 수집한 임상정보 리스트 **API**

출금 API는 다음을 만족해야 합니다.

- 최근 일주일내에 업데이트(변경사항이 있는) 된 임상정보 리스트  


## 사용한 기술 스택

Back-end : <img src="https://img.shields.io/badge/Python 3.8-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/FastAPI 3.2-092E20?style=for-the-badge&logo=Django&logoColor=white"/>&nbsp;

<p>
Tool : <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white"/>
</p>

## 모델링  

<img width="772" alt="스크린샷 2021-11-12 오전 3 26 36" src="https://user-images.githubusercontent.com/78228444/141350250-cf0f31b4-3905-46e9-ac6b-e390f516ad4d.png">


## 파일 구조  
- `./common`
  - `./config.py`    
- `./dao`
  - `./dao.py`
- `./database`
  - `./conn.py`
  - `./models.py`  
  - `./schema.py`  
- `./router`  
  -`./router.py`  
- `./service`  
  -`./service.py`  
  

## 구현기능  

### 수집한 임상정보에 대한 API
**endpoint** : `/search`
```number```
- ```계좌생성 성공시``` : status_code : 200

```
- JSON
{
    "MESSAGE": "SUCCESS",
}
```

- ```계좌생성 실패시``` : 
1. 비밀번호가 숫자 4자리 아닐시 status_code : 400, 
2. 키에러가 발생했을시 status_code : 400
```
- JSON
{
    "MESSAGE":"숫자 4자리를 입력해주세요.",
    "MESSAGE": "KEY_ERROR"   
}

``` 

### 수집한 임상정보 리스트 API
**endpoint** : `/account/deposit`

- ```Body Message```
```
- JSON
{
    'name': '강대훈',
    'account_id': 1,
    'password': '8647',
    'amount': 5000,
    'user_id': 2
}
```
- ```입금 성공시``` : status 200,
```
- JSON
{
    'MESSAGE': '입금 성공'
}
``` 

- ```일치하는 계좌가 없을 때``` : status 404, 
``` 
- JSON
{
    'MESSAGE': '일치하는 계좌가 없습니다.'
}
```

- ```본인의 계좌가 아닐 때``` : status 404, 
``` 
- JSON
{
    'MESSAGE': '본인의 계좌가 아닙니다.'
}
```

- ```패스워드가 틀렸을 때``` : status 404, 
``` 
- JSON
{
    'MESSAGE': '비밀번호가 틀렸습니다.'
}
```



# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
