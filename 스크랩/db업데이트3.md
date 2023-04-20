그 중에서, 필자가 어떤 것을 써야하나 매번 헷갈렸던 것들 위주로 정리해보자면 다음과 같다.

1. Model.save()
2. QuerySet.update()
3. QuerySet.bulk_update()

위 3개의 메소드 모두 업데이트할 때 쓰일 수 있다. 무엇이 다른가??

# [Model.save()](https://docs.djangoproject.com/en/3.2/ref/models/instances/#saving-objects)

DB에 모델 객체를 저장할 때 사용되는 API다.

```
>>> article = Article(title="My First Article")
>>> article.save()
```

이런 식으로 사용할 수 있다.

그런데, 이게 과연 **INSERT**일까, **UPDATE**일까??

> 짧게 말하자면 django가 알아서 해준다.
> 

길게 말하자면, 아래의 절차를 따른다.

![https://velog.velcdn.com/images%2Ffregataa%2Fpost%2F194b901f-ceac-41b8-b4bc-f1cbfc2d36af%2Fimage.png](https://velog.velcdn.com/images%2Ffregataa%2Fpost%2F194b901f-ceac-41b8-b4bc-f1cbfc2d36af%2Fimage.png)

## 정리

하나의 모델 객체를 바탕으로 DB에 새로 생성하거나 업데이트할 때 사용.

참고로, 특정 필드만 업데이트 하는 경우에는 `[update_field` 인자](https://docs.djangoproject.com/en/3.2/ref/models/instances/#specifying-which-fields-to-save)를 설정해주면 더 효율적이다.

# [QuerySet.update()](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#update)

django QuerySet API 중 하나다.

아무것도 return하지 않고, **즉시** 적용된다.

즉, QuerySet의 특징인 [laziness](https://velog.io/@fregataa/django-Database-Optimization#querysets-are-lazy)가 해당되지 않는다.

```
>>> Item.objects.filter(create_dt__year=2020).update(available=False)
```

이렇게 작성하면 **"생성 연도가 2020년인 모든 아이템"**에 대한 업데이트 쿼리가 실행된다.

개별 모델 인스턴스마다 `save()`를 실행하는 것보다 훠어어얼씬 빠르다!

## 정리

QuerySet으로 여러 DB레코드에 한번에 업데이트를 할 때 사용한다.

만약 모델 객체나 QuerySet의 반환값이 딱히 필요하지 않다면 아래처럼 `Model.save()`를 쓰기보단,

```
>>> item = Item.objects.get(id=1)
>>> item.available = False
>>> item.save()
```

아래처럼 `QuerySet.update()`를 쓰는 것이 더 효율적이다.

```
>>> Item.objects.filter(create_dt__year=2020).update(available=False)
```

# [QuerySet.bulk_update()](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#bulk-update)

여러 모델 인스턴스에 대한 `update`를 한 번에 실행시킬 때 사용된다.

**QuerySet**이 아니라 **여러 모델 인스턴스**이다.

예시는 아래와 같다.

```
>>> objs = [
...    Entry.objects.create(headline='Entry 1'),
...    Entry.objects.create(headline='Entry 2'),
... ]
>>> objs[0].headline = 'This is entry 1'
>>> objs[1].headline = 'This is entry 2'
>>> Entry.objects.bulk_update(objs, ['headline'])
```

내부적으로 `QuerySet.update()` 메소드를 사용한다. 한 번 확인해보시라.

Github link: [QuerySet.bulk_update()](https://github.com/django/django/blob/main/django/db/models/query.py#L904)

## 정리

~~솔직히, 어떤 상황에서 사용되어야 좋을지 잘 모르겠다...~~

~~내부적으로도 여러 작업을 거쳐 결국 `QuerySet.update()` 메소드를 실행시키기 때문에 굳이 bulk_update()까지 써야할 이유가 있나 싶다...~~

모델 인스턴스 리스트(혹은 튜플)을 만들어서 넘겨야하는데, 이런 상황이 자주 발생하는가??

---

**2021.10.28** 업데이트

왜인지는 모르겠지만, 이 API에 대해 잘못 알고 있었다.

`QuerySet.bulk_update()`는 굉장히 유용하다!

```
entries = Entry.objects.all()
for i, entry in enumerate(entries):
    entry.headline = f"{i} - Headline"

Entry.objects.bulk_update(entries, ["headline"])
```

이런 식으로 사용할 수 있다.

`bulk_update()` API 공식문서에서 인자로 `objs`를 넘겨주는 것으로 보고, 단순히 `list`나 `tuple` 형태만 받을 수 있을 줄 알았다.

허나 소스코드를 직접 보니, 결국 `tuple`로 타입 변환이 가능하기만 하면 상관없었다...

확인해보기: [django.db.models.query.QuerySet.bulk_update()](https://github.com/django/django/blob/afeafd6036616bac8263d762c1610f22241c0187/django/db/models/query.py#L542)

결국 `QuerySet` 타입의 데이터도 가능하다는 이야기다. (단, 모든 element가 id를 attribute로 갖고 있어야 한다..!)

`QuerySet`의 각 element인 모델 인스턴스마다 조금씩 다르게 update를 해주고 싶다면 `QuerySet.update()` API를 쓰기 복잡할 수 있다.

이럴 때 `bulk_update()`가 유용하다.!!