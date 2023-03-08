

# RendOlives

RendOlives is a complex online e-commerce website for selling olives and etc built with Django.
it supports adding diffrent products and selling them.
you could analyse your income with admin panel.
and it is connected to sms API and ZARINPAL payment method

- - - - 
# Screenshots
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%201.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%202.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%203.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%204.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%205.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%206.png)
![screenshot](https://github.com/mazdakdev/rendOlives/blob/36084ee2d021685c7b808ef03f4e36c477c4872b/images/screenshot%207.png)
- - - -

# Tools Used to develope this web-app🎯

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![redis](https://img.shields.io/badge/Redis-3776AB?style=for-the-badge&logo=Redis&logoColor=red)
![celery](https://img.shields.io/badge/Celery-092E20?style=for-the-badge&logo=Celery&logoColor=green)
![git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![firefox](https://img.shields.io/badge/Firefox_Browser-FF7139?style=for-the-badge&logo=Firefox-Browser&logoColor=white)
![macos](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)
![appple](https://img.shields.io/badge/Apple-laptop-999999?style=for-the-badge&logo=apple&logoColor=white)
![vscode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![tailwind.css](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![djangorest](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

- - - -

# How to Setup and Run ⚡️

- - - -

## Setup Variables in code :

### 1/2 Config secret Key

Location :  `( rendOlives/settings.py ~ line 33)`

```python
   # SECURITY WARNING: keep the secret key used in production secret!
   SECRET_KEY = ''
```

### 2/2 Config ZARINPAL API TOKEN 

Location :  `(rendOlives/settings.py ~ line 66 ~ 68)`

```python
     'ZARINPAL': {
           'MERCHANT_CODE': '',
       },
   
   },
```
- - - -

# Setup


install requires modules

```console
user@host:~$ pip3 install -r requirements.txt
```

run development server

```console
user@host:~$ python3 manage.py runserver
```

    
# Contributions :

   Feel free to give your opinion and show my issues for my improvement 
