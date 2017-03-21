# Django Rest Framework 보충 

# 소개

## 조교 소개

- 여러분과 같은 비전공자. 
    - 16년 9월 경, 웹프스 3기 시작 = 프로그래밍 인생 시작
- 전 기수 수강할때 rest_framework를 처음들으면서, 큰 멘붕(멘탈 붕괴)를 겪으면서 힘들어 했던 1인.     
    *클래스베이스드뷰(CBV)가 뭐야.. 어려워..*
- 프로젝트 기간 잘못된 사용방법으로 접근해 놓고 왜 안되는지 궁금해서 소스코드에 `print`찍어가면서 다 뜯어보겠다며   
    몇날며칠 삽질했던 경험 보유자
- 안되면 `django-rest-framework` 깃헙에 이슈 열어서 안된다고 고치라고 땡깡 부렸던 경험 다 회 보유    
    (owner에게 문서보고 오라는 소리 들은적 있음)


   
## 목표

- 어떻게 작동하지? CBV가 적응이안되.. FBV랑 너무다르다.. 좀더 명확했으면 좋겠다!
    - `The Zen of Python - Explicit is better than implicit.`
    - 이해안되는 CBV rest.. 명확하게 이해되도록 뜯어봅니다.

- 지금도 충분히 숙제도 많고, 복습도많고.. 추가 수업은 부담되서 싫어..   
    - `The Zen of Python - Simple is better than complex.`

    - 적은 복습량, 수준에 따라서는 주의깊게 보기만해도 도움되는 수준으로 쉽게,    
        짧은 시간동안 볼 수 있게 간단하게 진행
  

- 여러분의 rest_framework가 시키는대로 작동하게 되길 바랍니다.  
    비록 잘못된 방법으로 시킬지라도..
    - 올바른 방법으로 코드를 디자인하고, 알맞은 방법으로 앱이 실행되는방법은 이미 강사님을 통해 배웠고,    
    문서에 있습니다. rest_framework의 작동방식을 이해하고 어떻게 조작할수있는지에대해서 배울겁니다.   

    
---

## 계획
### Rest Framework의 작동 흐름에 대한 이해가 목표

#### 1일차
--

- generics.View와 ModelSerializer에 대한 기본적인 작동방법을 다시 한번 확인하고 이를 사용한 커스터마이징  
    - 간단한 커스텀유저 모델을 적용하여, 회원가입 하기, 비밀번호에 대한 유효성검사(8자리 이상).   
    - `request`(사용자 요청)이 App application(Django-Rest-Framework)안에서 작동하는 흐름에 대해서 살펴보기


--
#### 2일차

- 원하는 데이터를 원하는 순간에!
    - 회원가입 후 hashed password를 보여주고 싶지 않을땐?  
        - read\_only,  write_only, ReturnDict조작
    - ReturnDict, OrdererDict, QueryDict, Dict은 언제? 무엇?   
    - view에서만 회원가입 완료시키기

--
#### 3일차(응용)


- 여러장에 사진파일을 동시 전송하는 방법 익히기  
    - NestedSerializer 사용
    - 다른 전송방식(json, form)에 대한 다른 사용방법   
    - Model Class의 property속성과, serializer의 Methodfield에 대해서 알아보고 사용하기  

--
   
수업종료후 20시까지 남아서 **이 내용에 관해서만** 질문 받습니다.
(화, 수, 금 예정)

---


#### 유의사항

* Python Class에 대한 기본적인 개념은 필수입니다.
    * 필수 keyword : instance, 상속, 다중 상속, 메소드와 함수의 차이, self, 오버라이딩    

* 튜토리얼은 최소 2회정도 반복했다는 가정하에 진행됩니다.

* 감을 잡기 위한 보충일뿐, 최고의 방법/최선의 방법을 배울 수 있는 시간은 아닙니다.   
> 진정한 배움은 강사님에게!


* 이미 정규 수업시간에 다 다뤄본 내용이거나, 그에대한 보충설명일 뿐입니다.
> 중복되거나 지루할 수 있습니다. 


**경고!** 많은 삽질에 대한 경험 공유일 뿐입니다. 저의 `안좋은 습관`까지 공유될수도 있습니다.   

> 연습은 완벽함을 만들지 않습니다. 완벽한 연습만이 완벽함을 만듭니다.   
> 안좋은 습관까지 같이 연습하지 마세요. 


---

# 진행

## Django app만들기

```
$ django-admin startproject day1
$ mv day1 django_app
$ cd django_app
$ python manage.py startapp member

```

#### CustomUserModel만들기

간단한 테스트를 위해, name과 password만 가지는 user model만들기

* 모델 구조

``` 
# Member Class fields  

name = models.CharField(max_length=20, unique=True)   
is_staff = models.BooleanField()

```

* settings.py 설정

```
#settings.py

AUTH_USER_MODEL = 'member.CustomUser'

INSTALLED_APPS = [
    ...
    member.apps.MemberConfig
]
```

* 유저 만들기

`$ python manage.py createsuperuser`

---
 
## Rest-Framework

```
$ pip install djangorestframework
```

```
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

#### member/serializers.py

```
from rest_framework import serializers
from .models import CustomUser

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = 'name', 'password'

```


#### member/views.py

```
from rest_framework import generics
from .serializers import SignUpSerailizer

class UserCreate(generics.CreateAPIView):
    serializer_class = SignUpSerializer

```

#### urls.py 설정

```
# day1/urls.py

from django.conf.urls import url, include

urlpatterns = [
    ...
    url(r'^user/', include('member.urls'))
    
]

# member/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.UserCreate.as_view()),
]

```



#### POSTMAN확인

#### *제대로 잘 만들어지는가요??*

#### python manage.py shell에서 확인

```
>>> from member.models import CustomUser
>>> user = CustomUser.objects.last()
>>> user.name
: '이름'
>>> user.password
: 'raw password'

```

# ???????????????

password는 settings.py에 있는 secretkey를 통해 암호화되서 저장된다고 알고있는데??   

**무언가 잘못되었습니다.**

> 지금상태라면 로그인도 되지 않습니다.  

#### 어떤 흐름으로 만들어지고 있는걸까?


### **request흐름을 따라가보면서, 확인해보겠습니다.**

---

## request의 흐름 in View


**DJANGO MVT 모델**

* templates이 없는 지금은..??
* MSV-C(model, serializer, view, client)   

    > 이해를 위해 급조한 단어입니다. 어디가서 쓰지마세요. 아무도 모릅니다.
 
    1. client가 지정된 url에 요청(정보)을 보냅니다.
    > Mobile Apps, SPA(single page applcation) 등

    1. client가 보내온 정보를, view에서 받습니다.   
    1. view에서 serializer를 조작합니다. 
    1. serializer에서는 유효성검사 및 DB에 저장합니다.  

사용자가 보낸 `request`는 urls를 통해 view로 넘어옵니다. 

generics.View안에서는 `GET`, `POST`, `DELETE`, `PUT`, `PATCH` method에 따라서 별도의 흐름으로 데이터가 흐릅니다.

```
참고 : request.method == 'GET'
기억하나시나요??
```


이는 generic.view안에(정확히는 View안에) 있는 `dispatch`라는 메소드에서 request.method를 인식하여서 알맞은 길로(알맞은 메소드로) 보내줍니다.

```
참고 : 상속관계    
generics.View > GenericAPIView > views.APIVIEW > View
```

지금 회원가입에서는 메소드를 'POST'를 사용합니다.   
POST(create)를 따라가봅시다.

```
참고 : METHOD에 따른 호출 메소드  
GET => get -> (list or retrieve) # 설정에 따라서
POST => post -> create
DELETE = > delete -> destroy
PUT => put -> update
PATCH = > patch -> partial_update -> update # 인자로 partial=True
```

```
# 아래내용을 UserCreaet(view)에 오버라이딩 해줍시다.
from rest_framework.response import Response
from rest_framework import status

...생략...
    # in class
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # 1
        serializer.is_valid(raise_exception=True) #2
        self.perform_create(serializer) #3
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) #4

    def perform_create(self, serializer):
        serializer.save()


```
### *`print(request.data)` 해보세요*


```
참고 : Q. 어떤 동작을 하기위해서 어떤 메소드를 오버라이딩해야되는지 알려면 다 뜯어봐야되나요. 싫다..
        A. 네 뜯어보면 알 수 있습니다. 
        하지만 문서를 봐도 어떤 동작할때 어떤 메소드를 불러와서 해라 라는 예제가 다 있습니다.
        뜯어볼건지, 문서볼건지 선택하시면 됩니다.
```

결국 지금 여기서는 `request`는 지정된 url로 들어오게되면,   
지정한 views.UserCrate.as_view()메소드에 보내집니다.   
그다음  
`dispatch`메소드를 만나서 `request.METHOD`에 맞는    
`post`메소드에 보내지고, `post`메소드는 `request`를    
`create`메소드로 보냅니다.   

이 간단한 흐름을 제외하면,

#### **request**는 `create`메소드안에서 동작하는게 전부입니다.  
고작 다섯줄이 실행된 후, `Response`로 나갑니다. (사용자에게 응답됩니다.)

약간에 비약을 사용한다면, 지금 django app에서 회원가입기능은 저 5줄이 끝입니다.  

저 5줄만 이해하면, `POST` 요청일때, 어떻게 작동하는지 명확하게 알수 있게됩니다.   
다른 `METHOD`에 대해서 비슷하게 작동하기때문에, 금방이해하는데 도움이 됩니다.  

--

#### 한줄씩 뜯어보기

* `serializer = self.get_serializer(data=request.data) # 1
`    
  
    * `self.get_serialzer`메소드는 view에서 선언한 (serializer_class='사용자지정 serializer')   
serializer를 가져온다음에, request.data를 넣어서 반직렬화를 진행합니다.  
(반직렬화, 직렬화란??  -------- tutorial 한번 더..)

* `serializer.is_valid(raise_exception=True) #2`
    * serializer(직렬화된 request.data)가 지정한 필드에 맞게 들어왔는지 확인합니다.  
패스워드 올바르게 사용했는지 확인하고싶다면?   
serializer class에서 할 수 있을거같은 힌트가 주어진것 같네요

* `self.perform_create(serializer) #3`
    * `perfrom_create`메소드는 사용자가 오버라이딩하기 편하게 하기 위해서 만들어준 메소드입니다.   
serializer가 저장되기 전에 어떤 작업을 하기 위해서 `create`메소드를 다 가져올 필요가 없어졌습니다.   

        > 추가적인 import를 할필요가 없는게 가장 큰 장점입니다.   
        > DB를 수정하기전 추가적인 작업을 위해서 디자인되었습니다.   
        >  - create, update, destroy에는 모두 `perform_<name>`이 있습니다.  

* `return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) #4`  
    * 중간어디에서 오류가 발생하지 않았다면, (다른 return을 만나지 않았다면 )  
사용자 요청에따른 작업이 **성공적으로** 완료될때 발생하는 return입니다.   
그에 따른 응답을 사용자에게 해줍니다.

--

그럼 잘못된 패스워드가 저장된 이유를 찾아봅시다.  
다시 한번 말씀드리면 지금 작동하는 흐름은 view안에 `create`메소드에 보여진게 전부입니다.  

데이터베이스 저장(save)이 잘못됬으니,   
`serializer.save()`가 범인인것 같으니 찾아가보겠습니다.  

## DB는 어디서 만들어지나

결국에 `ModelSerializer`안에 create에서 모델이 만들어지는걸 알 수 있습니다.

`ModelClass = self.Mate.model`  
에서 우리가 정의한 `model`을 가져와서

`ModelClass.objects.create(**validated_data)`로 모델이 만들어지는것이 보입니다.

> `CustomUserManage`에서 정의하기를.. `create_user`로 만들었는데..  

커스터마이징하기위해서 오버라이딩해줍니다.




```
# member/serializers.py 
# SignUpSerializer class안에..

    def create(self, validated_data):
        instance = CustomUser.objects.create_user(**validated_data)
        return instance
```

```
참고 : ModelSerializer가 아닌 Serializer 를 사용하면,
create메소드를 명시적으로 작성해줘야합니다.  
(내부에 create메소드가 없습니다.)  
지금은 ModelSerializer이기 때문에,   
자동으로 Model과 연결되어 생성해주기 때문에, 내부에 create 메소드가 존재합니다.
+ 유효성검사를 위해서 fields의 종류도 직접 지정해줘야됩니다.  그렇지 않으면 validation을 통과하지 못합니다.  
```

#### POSTMAN확인

```
# 결과

{
  "name": "sol",
  "password": "pbkdf2_sha256$30000$QgyJwPBIoU6j$f01YhlklL/q0fvfFHuyk4k506Uf9viTDECcWY2DJCws="
}

```

> '패스워드를 구지 보여줄 필요가 있을까.. 아무리 해쉬화 됬지만..'  
> 와 같은 욕구는 내일 해결하겠습니다.

---

### 비밀번호 유효성 검사

아까 힌트를 얻었습니다.  

```
# view
    def create(self, request, *args, **kwargs):
        ...
        serializer.is_valid(raise_exception=True) #2
        ...

```
```
참고 : view에도 create메소드가 있고, serializer에도 create메소드가 있습니다.   
두개는 다릅니다.      
view에 있는 create메소드는 POST요청(create)이 들어올때 호출되는 메소드이고,   
serializer에 있는 create메소드는 Model Instance를 만들때 호출되는 메소드입니다.  
```
> 유효성검사도 `serializer`에서 실행됨을 알 수 있습니다.

> 여유가있으시다면 뜯어보셔도 좋습니다.

> 하지만 지금은 소스코드를 뜯어보지 않겠습니다. 굉장히 복잡합니다.  


문서를 다 봐야하는 이유가 여기 있습니다.

문서를 찾아보면 다양한 방법으로 유효성검사를 하는방법이 친절하게 나옵니다.

하지만 지금은 맘대로 해볼겁니다.

view에 들어오는 password를 확인한다음에 오류를 띄우겠습니다.

#### view에서 멋대로 유효성검사

```
class UserCreate(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        if len(request.data['password']) < 10: # 이부분 추가
            return Response("안되!")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

```

10글자 이상일땐 잘 만들어지지만 10글자보다 짧으면 아래와 같은 응답이 옵니다.


#### POSTMAN확인

```
"안되!"
```

---

## request의 흐름 in serializer


근데 serializer 인스턴스를 처음만들때 넣은 request.data는 어떻게 흐를까요?
> serializer에는 request.data를 넣어줬습니다.   
> `self.get_serializer(data=request.data)`  
> 여기서는 정확하게는 request의 흐름이아닌 request.data의 흐름을 살펴봅니다
 
serializer에는 데이터가 어디있을까요

#### serializer에서 ..
```
# member/serializers.py
# SignUpSerializer class안 create메소드에 추가

    def create(self, validated_data):
        print(self.initial_data)
        print(self.validated_data)
        print(self.data)
        instance = CustomUser.objects.create_user(**validated_data)
        return instance

```
출력 결과

```
<QueryDict: {'password': ['123'], 'name': ['sol25']}>
OrderedDict([('name', 'sol25'), ('password', '123')])
{'password': '123', 'name': 'sol25'} # ReturnDict
```

serializer에는 `view`에서 에서`self_get_serializer(data=request.data)`  
가 작동하면 `request.data`의 값이 최초 `serializer.initial_data`에 저장됩니다.  

그다음에 `run_validation` 메소드가 호출되면서, 
유효성검사를 진행하고 통과한 값들은,

`validate_data`에 저장되고

`serializer.save()`를 통과하면서 모델에 인스턴스가 만들어지면

인스턴스의 값들이 `serializer.data`에 저장됩니다.


##### serializer에서 데이터생성 정리

1. 최초 serializer 인스턴스가 만들어 진 다음   
`get_serializer(data=request.data)` => `serializer.initial_data` 에 저장

2. 유효성검사가 완료후에   
`serializer.is_valid()` => `serializer.validated_date` 에 저장

3. 모델에 저장된 후에   
`serializer.save()` => `serializer.data` 에 저장
      
  

```
참고 : view에서 위에 흐름 확인하기.
- serializer.is_valid()가 호출되기 전에 
  serializer.validate_date출력

- serializer.save()가 호출되기 전에
  serializer.data출력
  
  해보면 둘다 오류가 납니다.

```

serializer에서 request.data가 어떻게 변해가는지 확인했습니다. 

---

만약 포스트맨에서 회원가입할때  

```
title = '제목입니다.'
content = '내용입니다. 배고파..'
```

라는 내용도 같이 포함해서 보내면 어떻게되는지 확인해보겠습니다.

이 값들은 serializer에서 지정한 `fields`가 아니기때문에
validate를 통과하지 못합니다.  
따라서 `serializer.validated_data`와 `serializer.data`에는 없지만,   
`request.data` 와 `serializer.initial_data`에는 포함되있기 때문에   
원한다면 마음대로, 원하는 곳에서 model을 만든다던지의 작업을 할 수 있습니다.

이에 대해서는 내일 더 진행해보도록 하겠습니다.





## 정리

`genericsView`와 `ModelSerializer`를 사용하여,   
view에서 사용자요청이(request)가 들어와서 어떤 순서로, 어떠한 동작을 했습니다.   
또 serializer에서는 request.data가 어떻게 변하는지 확인했습니다.  

## 더 원하신다면..    

> 본수업에 방해가 되면 절대 안됩니다. 수업전까지만, 수업준비가 필요하신분들은 주말에 하시는걸 추천드립니다.

1. 위에서 사용한 django app에서 ModelSerializer가 아닌 Serializer로 동일한 작동을하게 만들어보세요.
2. view에서 `create` 메소드 5줄을, 한줄씩 뜯어본 것 처럼,    
    `list`, `retrieve`, `destroy`, `update`메소드도 뜯어보세요.
    
    > `generics.view`건, `APIVIEW`건, `mixinview`건, `viewset`이건 간에 결국엔   
    같은 클래스들(`mixinview`)을 상속받아오기 때문에 동일한 메소드를 사용합니다.  
    

    
    
*만약 지금 내용이 이해가지 않았다면, python class에 대한 개념이 부족합니다.(상속, 메소드, 오버라이딩, instance) class에 대한 부분을 복습하신 후에 다시 보시기 바랍니다.*

