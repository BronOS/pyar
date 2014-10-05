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


Adapter
===
Adapter is a data provider which is realized IAdapter interface and provides 4 methods to use (CRUD):
  * create
  * read
  * update
  * delete
  
All this methods are takes IModel as first parameter and realized own logic based on given model. 


Model
===
PyAR modes can use different adapters to read and write data.
All find methods of the model are using read adapter and other write.
Models stores own data into the __data private attribute and use __seattr__, __getattr__, ... magic methods to manipulate of it. 


Model resource
===
The models attribute _resource_ is used by adapters through get_resource() method. For example MySQL adapter maps _resource_ to the table name.
By default _resource_ equals to None, so get_resource() method is transformed models name to the uncamelaized view separated by "_".
For example: Project resource will be looks like "project" and UserHistory - user_history.


Model associations
===
PyAR model can contains association with other models which instance will be created automatically when model sets data.

Example:
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


Abstract Model API
===
pyar.model.AModel = class AModel(IModel, AModelData, AModelAdapter)
 |  PyAR abstract model.
 |  
 |  Method resolution order:
 |      AModel
 |      IModel
 |      AModelData
 |      AModelAdapter
 |      IModelAdapter
 |      IModelData
 |      IModelNew
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, data=None, is_new=True)
 |      Constructor.
 |      Sets models data.
 |      
 |      :param data: Models data.
 |      :type data: dict
 |  
 |  is_new(self)
 |      Returns whether this model is new.
 |      
 |      :rtype: bool
 |  
 |  set_is_new(self, value)
 |      Sets is new state for model.
 |      
 |      :param value: Value of state.
 |      :type value: bool
 |      :rtype: None
 |  
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |  
 |  get_resource() from pyar.model.ModelMetaRegister
 |      Returns models resource name.
 |      
 |      :rtype: str
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from AModelData:
 |  
 |  __delattr__(self, key)
 |      Removes models attribute.
 |      
 |      :param key: Attribute name.
 |      :type key: str
 |      :rtype: None
 |  
 |  __getattr__(self, key)
 |      Returns attributes value if key exists and None otherwise.
 |      
 |      :param key: Attribute name.
 |      :type key: str
 |      :rtype: str|list|dict|None
 |  
 |  __setattr__(self, key, value)
 |      Sets models attribute.
 |      
 |      :param key: Attribute name.
 |      :type key: str
 |      :param value: Attribute value.
 |      :type value: str|dict|list
 |      :rtype: None
 |  
 |  del_attr(self, attr)
 |      Returns attributes value if it exists and None otherwise.
 |      
 |      :param attr: Attribute name.
 |      :type attr: str
 |      :rtype: str|list|dict|None
 |  
 |  get_attr(self, attr)
 |      Returns attributes value if it exists and None otherwise.
 |      
 |      :param attr: Attribute name.
 |      :type attr: str
 |      :rtype: str|list|dict|None
 |  
 |  get_data(self, with_models=True)
 |      Returns models data.
 |      
 |      :param with_models: Adds information about nested models to the dict.
 |      :type with_models: bool
 |      :rtype: dict
 |  
 |  get_data_models(self)
 |      Returns dict of model's fields of this model.
 |      
 |      :rtype: dict
 |  
 |  get_origin_data(self)
 |      Returns models origin data.
 |      
 |      :rtype: dict
 |  
 |  set_data(self, data)
 |      Sets models data.
 |      Replace all old value.
 |      
 |      :param data: Models data.
 |      :type data: dict
 |      :rtype: None
 |  
 |  to_dict(self, with_models=True)
 |      Returns dict representation of model.
 |      
 |      :param with_models: Adds information about nested models to the dict.
 |      :type with_models: bool
 |      :rtype: dict
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from AModelAdapter:
 |  
 |  create(self, **kwargs)
 |      Creates model.
 |      
 |      :rtype: bool
 |  
 |  delete(self, **kwargs)
 |      Deletes model.
 |      
 |      :rtype: bool
 |  
 |  save(self, **kwargs)
 |      Saves model.
 |      
 |      :rtype: bool
 |  
 |  update(self, **kwargs)
 |      Updates model.
 |      
 |      :rtype: bool
 |  
 |  ----------------------------------------------------------------------
 |  Class methods inherited from AModelAdapter:
 |  
 |  find(**kwargs) from pyar.model.ModelMetaRegister
 |      Find entities and returns it as list of models.
 |      
 |      :rtype: list
 |  
 |  find_one(**kwargs) from pyar.model.ModelMetaRegister
 |      Returns firs element of found entities.
 |      
 |      :rtype: IModel|None
 |  
 |  get_read_adapter() from pyar.model.ModelMetaRegister
 |      Returns models read adapter name.
 |      
 |      :rtype: str
 |  
 |  get_read_adapter_inst() from pyar.model.ModelMetaRegister
 |      Returns read adapter instance.
 |      
 |      :rtype: IAdapter
 |  
 |  get_write_adapter() from pyar.model.ModelMetaRegister
 |      Returns models write adapter name.
 |      
 |      :rtype: str
 |  
 |  get_write_adapter_inst() from pyar.model.ModelMetaRegister
 |      Returns write adapter instance.
 |      
 |      :rtype: IAdapter
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from IModelAdapter:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)


SQL
===



SQLModel
===



SQLModel API
===



Relations
===

