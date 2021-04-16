import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitap_pazari.settings') #modelleri view ve diğer şeyyleri kullanmak için söylememiz lazım. yolu gösterdik. aşağıda kullanacağız.

import django  #djangoya haber verdik.
django.setup() #kaydettik. gerekli olduğunda isticez.


### Modellerimize ve django içeriklerine erişmek için yukarıdaki gibi ayarlamaları yapmamız lazım
### SIRALAMA ÇOK ÖNEMLİ

from django.contrib.auth.models import User

from faker import Faker
import requests


def set_user():

    fake = Faker(['en_US'])

    f_name= fake.first_name()
    l_name =fake.last_name()
    u_name = f'{f_name.lower()}_{l_name.lower()}'
    email =f'{u_name}@{fake.domain_name()}'
    print(f_name,l_name,email)

    user_check = User.objects.filter(username=u_name) #böyle bir username var mı

    while user_check.exists(): #aynı kullanıcı adı varsa bunu sonuna sayı vererek kullanıcı adını değiştirerek kontrol ediyoruz.
        u_name = u_name+ str(random.randrange(1,99))
        user_check = User.objects.filter(username=u_name)


    user = User( #kullanıcı yaratmak istiyoruz.
        username = u_name,
        first_name =f_name,
        last_name = l_name,
        email = email,
        is_staff=fake.boolean(chance_of_getting_true=50) #yüzde ellisini superuser yapıyor sanıırm. staff status ile geliyor. yeşil tik var yanlarında
    )

    user.set_password('testing321..') #hepsine aynı parolayı verdik. zamanı gelince lazım olur diye.
    user.save()
    print('Kullanıcı kaydedildi',u_name)


from pprint import pprint
from kitaplar.api.serializers import KitapSerializer

#zor bir konuydu. 2. bölüm 10. video Datayı çekme ve veri tabanına kaydetme işlemi var.
def kitap_ekle(konu=None):

    fake = Faker(['en_US'])

    url = 'http://openlibrary.org/search.json'
    payload ={ 'q' : konu}
    response = requests.get(url, params=payload)
    
    if response.status_code != 200:
        print('Hatalı istek yapıldı.', response.status_code)
        return  

    jsn = response.json()
    kitaplar = jsn.get('docs') #json docs içindeki her bir kitap.(100 kitap var.)

    for kitap in kitaplar:

        kitap_adi = kitap.get('title')
        data = dict(
            isim = kitap.get('title'),
            yazar = kitap.get('author_name')[0], #yazar listesinden ilkini aldı.
            aciklama = '-'.join(kitap.get('text')),
            yayin_tarihi = fake.date_time_between(start_date='-10y', end_date='now', tzinfo=None),
        
        )
        serializer = KitapSerializer(data=data) #serileştirdik 
        if serializer.is_valid():
            serializer.save()
            print('Kitap kaydedildi.', kitap_adi)
        else:
            continue
        
        







