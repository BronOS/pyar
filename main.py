from pyar import PyAR, MySQLAdapter, ASQLModel, Relation, HasManyRelation, BelongToRelation, HasOneRelation, AModel, \
    JiraReaderAdapter

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

# Example - using many adapters
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