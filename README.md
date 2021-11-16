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
**endpoint** : `api/search`/```number (number는 Open API에 있는 연구번호 속성)```  
- ```읽어오기 성공``` : status_code : 200

```
- JSON
{
    "RESULT":
    {
        "research_number": "C130011",  
        "research_name": "대한민국 쇼그렌 증후군 코호트 구축",  
        "research_subject_count":500,  
        "research_period": "6년",  
        "research_created_at" : 2021.11.15 02:08:55",  
        "research_updated_at" : 2021.11.15 02:08:55",  
        "department_name" : "Rheumatology",
        "hospital_name" : "가톨릭대 서울성모병원",  
        "type_name" : "관찰연구",  
        "scope_name" : "국내다기관",  
        "stage_name": "코호트"
    }
}
```

- ```실패시``` : status_code : 404
```
- JSON
{
    "MESSAGE":"NOT LIST"
}

``` 

### 수집한 임상정보 리스트 API
**endpoint** : `api/list`?```skip=(int)&limit(int)```

```
- JSON
{
    "RESULT":[
    {
        "id" :1  
        "number": "C160009",  
        "name": "한국인 알코올 사용장애 임상결과 및 생물정신사회적 오인 규명을 위한 임상 및 지역기관 융합연구",  
        "subject_count":540,  
        "period": "5년",  
        "research_created_at" : 2021.11.16  02:08:55",  
        "research_updated_at" : 2021.11.16 02:08:55",  
        "department_name" : "Psychiatry",  
        "hospital_name" : "가톨릭대 서울성모병원",  
        "type" : "관찰연구",  
        "scope" : "국내다기관",  
        "stage": "코호트"
    },
    {
        "id" :2  
        "number": "C130011",  
        "name": "대한민국 쇼그렌 증후군 코호트 구축",  
        "subject_count":500,  
        "period": "6년",  
        "created_at" : 2021.11.15 02:08:55",  
        "updated_at" : 2021.11.15 02:08:55",  
        "department" : "Rheumatology",
        "hospital" : "가톨릭대 서울성모병원",  
        "type" : "관찰연구",  
        "scope : "국내다기관",  
        "stage": "코호트"  
    },
    .
    .
    .
    
    ]
}
```

- ```실패시``` : status_code : 404
```
- JSON
{
    "MESSAGE":"NO DATA"  
}




# Reference
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 8퍼센트에서 출제한 과제를 기반으로 만들었습니다.
