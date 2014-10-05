from pyar import PyAR, MySQLAdapter, ASQLModel, Relation, HasManyRelation, BelongToRelation, HasOneRelation

PyAR.add_adapter(MySQLAdapter(host='localhost', database='srt', user='root', passwd=''))


class Project(ASQLModel):
    pass


project = Project()
project.title = 'My Project'
project.save()

print(Project.find_by_id(1).to_dict())