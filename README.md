PyAR
====
The Python Active Record / Object Related Mapper.

Introduction
===
The PyAR can be used with any type of data through adapter. PyAR modes can use different adapters to read and write data.
All find methods of the model are using read adapter and other write.

Quick example:
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

Model
===


Adapter
===
Adapter is a data provider which is realized IAdapter interface and provides 4 methods to use (CRUD):
  * create
  * read
  * update
  * delete
  
All this methods are takes IModel as first parameter and realized own logic based on given model. 

SQL
===


Associations
===

