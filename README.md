PyAR
====
The Python Active Record / Object Related Mapper.


Introduction
===
The PyAR is an open source ORM library based on the ActiveRecord pattern. This library was inspired by Ruby on Rails 
implementation and therefore borrows many of its conventions and ideas. The library is licensed under the MIT License 
and so you are completely free to do whatever you want with it.

#### Quick example:
```
from pyar import PyAR, MySQLAdapter, ASQLModel, Relation, HasManyRelation, BelongToRelation, HasOneRelation
  
PyAR.add_adapter(MySQLAdapter(host='localhost', database='test', user='root', passwd=''))


class Project(ASQLModel):
    pass
    
    
project = Project()
project.title = 'My Project'
project.save()

print(Project.find_by_id(1).to_dict())
# {'id': 1, 'title': 'My Project'}
print(Project.get_last_query())
# SELECT project.* FROM project WHERE project.id = 1
```


Adapter
===
Adapter is a data provider which is realized IAdapter interface and provides 4 base methods to use (CRUD):
  * create
  * read
  * update
  * delete
  
All this methods are takes IModel as first parameter and realized own logic based on given model. 

#### Example - using 2 adapters to read and write to different data sources.
```
# Main adapter
PyAR.add_adapter(MySQLAdapter(host='localhost', database='srt', user='root', passwd=''))
# JIRA rest api reader adapter
PyAR.add_adapter(JiraReaderAdapter('https://jira.loc', 'user', 'pass'), 'jira')


class User(AModel):
    _read_adapter_ = 'jira'


# Read data from JIRA rest api.
user = User.find_one(username='user1')
# Create user in the MySQL database.
user.create()
```


Model
===
PyAR modes can use different adapters to read and write data.
All find methods of the model are using read adapter and other write.
Models stores own data into the __data private attribute and use __seattr__, __getattr__, ... magic methods 
to manipulate of it. 


Model resource
===
The models attribute _resource_ is used by adapters through get_resource() method. For example MySQL adapter 
maps _resource_ to the table name.
By default _resource_ equals to None, so get_resource() method is transformed models name to the uncamelaized view separated by "_".
For example: Project resource will be looks like "project" and UserHistory - user_history.

It is possible to define separate read and write resources by setting _read_resource_ and _write_resource_. 
Read/write resources will be override main resource.  

 
#### Example - using custom resource
```
class User(AModel):
    _resource_ = 'admin_users'

```


Model associations
===
PyAR model can contains association with other models which instance will be created automatically when model sets data.

#### Example - using models associations:
```
class Project(AModel):
    pass


class User(AModel):
    project = Project


data = {
    'first_name': 'FIRSTNAME',
    'last_name': 'LASTNAME',
    'project': {
        'title': 'My Project'
    }
}
user = User(data)
print(user.get_data())
{'last_name': 'LASTNAME', 'project': <__main__.Project object at 0x10c792438>, 'first_name': 'FIRSTNAME'}
print(user.project.get_data())
{'title': 'My Project'}
```


SQL
===
The main idea of the PyAR SQL is a gives easy way to work with sql databases without hard writing of SQL in common cases.


SQL Basic CRUD
===
#### Create
This is where you save records into your database. 
Here we create a new project by instantiating a new object and then invoking the save() method.
Save method calls create or update method by "is_new" flag.
```
project = Project()
project.title = 'My Project'
project.user_id = 1
project.save() # same with project.create(), flag "is_new" = True
# INSERT INTO project (title, user_id) VALUES ('My Project', 1)
```

#### Read
These are your basic methods to find and retrieve records from your database. 
See the SQL Finders section for more details.
```
for project in Project.find(title='My Project'):
    print(project.title) # 'My Project'
    print(project.id) # 1

project = Project.find_by_id(1)
print(project.title) # 'My Project'
print(project.id) # 1

# Same with find_by_id
project = Project.find_one(id=1)
print(project.title) # 'My Project'
print(project.id) # 1
```

#### Update
To update you would just need to find a record first and then change one of its attributes. 
```
project = Project.find_one(where='title LIKE :title', params={'title': 'My%'})
project.title = 'My Project 2'
project.save() # same with project.update(), flag "is_new" = False
# UPDATE project SET id = 1, title = 'My Project 2' WHERE id = 1
```

#### Delete
Deleting a record will not destroy the object. This means that it will call sql to delete the record in your database, 
however, you can still use the object. Object, after deleting, changes "is_new" state to "True" and removes value 
of primary key.
```
project = Project.find_by_id(1)
project.delete()
# DELETE FROM project WHERE id = 1 LIMIT 1
```


SQL Finders
===




SQL Relations
===

