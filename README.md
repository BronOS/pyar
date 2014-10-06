PyAR
====
The Python Active Record / Object Related Mapper.


Introduction
===
The PyAR is an open source ORM library based on the ActiveRecord pattern. This library was inspired by Ruby on Rails 
implementation and therefore borrows many of its conventions and ideas. The library is licensed under the MIT License 
and so you are completely free to do whatever you want with it.

## Quick example:
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

## Example - using 2 adapters to read and write to different data sources.
```
# Main adapter
PyAR.add_adapter(MySQLAdapter(host='localhost', database='srt', user='root', passwd=''))
# JIRA rest api reader adapter
PyAR.add_adapter(JiraReaderAdapter('https://jira.loc', 'user', 'pass'), 'jira')


class User(AModel):
    _read_adapter_ = 'jira'


# Read from JIRA rest api.
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
 
## Example - using custom resource
```
class User(AModel):
    _resource_ = 'admin_users'

```


Model associations
===
PyAR model can contains association with other models which instance will be created automatically when model sets data.

## Example - using models associations:
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
PyAR provides 


SQLModel
===



SQLModel API
===



Relations
===

