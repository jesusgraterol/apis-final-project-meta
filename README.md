# Meta: APIs' Final Project

This repository serves as my personal submission for the Final Project in the [APIs Course](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer) offered by Meta through Coursera in the [Back-End Developer Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer).





## Project Structure

```
apis-final-project-meta
    │
    LittleLemon/
    │    ├───LittleLemon/
    │    │       ├───asgi.py
    │    │       ├───settings.py
    │    │       ├───urls.py
    │    │       └───wsgi.py
    │    ├───LittleLemonAPI/
    │    │       ├───admin.py
    │    │       ├───apps.py
    │    │       ├───models.py
    │    │       ├───permissions.py
    │    │       ├───serializers.py
    │    │       ├───tests.py
    │    │       ├───urls.py
    │    │       └───views.py
    │    ├───db.sqlite3
    │    └───manage.py
    │
    README.md
```





## Getting Started

```bash
$ cd apis-final-project-meta/LittleLemon

$ pipenv shell

$ pipenv install

$ python3 manage.py makemigrations 

$ python3 manage.py migrate

$ python3 manage.py runserver
```





## `superuser` Credentials

**Username:** `admin`

**Email:** `admin@littlelemon.com`

**Password:** `admin@123!`





## Endpoints

[Postman Workspace](https://www.postman.com/jesusgraterol/workspace/apis-final-project-meta)




## Grading Criteria

1. [x] The admin can assign users to the manager group
2. [x] You can access the manager group with an admin token
3. [x] The admin can add menu items 
4. [x] The admin can add categories
5. [x] Managers can log in 
6. [x] Managers can update the item of the day
7. [x] Managers can assign users to the delivery crew
8. [ ] Managers can assign orders to the delivery crew
9. [ ] The delivery crew can access orders assigned to them
10. [ ] The delivery crew can update an order as delivered
11. [x] Customers can register
12. [x] Customers can log in using their username and password and get access tokens
13. [x] Customers can browse all categories 
14. [x] Customers can browse all the menu items at once
15. [x] Customers can browse menu items by category
16. [x] Customers can paginate menu items
17. [x] Customers can sort menu items by price
18. [x] Customers can add menu items to the cart
19. [x] Customers can access previously added items in the cart
20. [ ] Customers can place orders
21. [ ] Customers can browse their own orders