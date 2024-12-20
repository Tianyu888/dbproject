This project is a demo about using LLM to help user acquire financial information from natural language. 
<img width="900" alt="index" src="https://github.com/user-attachments/assets/5e0fa01e-282a-44a9-8d48-1e520a4cf9a0" />

#### Environment
Python 3.11.4

```pip install django```
```pip install openai```
```pip install mysqlclient```

#### How to use

#### Configure Mysql
go to mysql in command line by 
```mysql -u root -p```
Then load the schema of the table by 
```source /Directory/to/table/schema```
```source /Directory/to/table/data```

In dbprject/settings.py, configure mysql database in django framework
'NAME': 'NameOfDababase',
'USER': 'root',
'PASSWORD': 'YourPassword'



##### Configure Django
go to the top level directory and execute 
```python manage.py makemigrations``` 
```python manage.py migrate``` 
```python manage.py runserver```

Then visit http://127.0.0.1:8000/api using your web server

