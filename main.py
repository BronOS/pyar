from pyar import PyAR, MySQLAdapter, ASQLModel, Relation, HasManyRelation, BelongToRelation, HasOneRelation, AModel

# PyAR.add_adapter(MySQLAdapter(host='localhost', database='srt', user='root', passwd=''))


# # Example - quick start
# class Project(ASQLModel):
#     pass
#
#
# project = Project()
# project.title = 'My Project'
# project.save()
#
# print(Project.find_by_id(1).to_dict())


# Example - model associations
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
print(user.project.get_data())
