from .base_test import BaseTestCase
from authservice.models.user import User
from authservice.models.group import Group
# from inventoryservice.manufacturer import Manufacturer


class FunctionalTests(BaseTestCase):

    def __init__(self):
        pass
    # def test_get_collection(self):
    #     man = Manufacturer(self.dbsession)
    #     item = ManufacturerModel(name='unique_test', description='test manufacturer')
    #     self.dbsession.add(item)
    #     self.dbsession.commit()
    #     collection = man.get_collection(dict(deleted=False, name='unique_test'))
    #     assert(len(collection) == 1)
    #     assert(collection[0].name == 'unique_test')
    #     item = ManufacturerModel(name='unique_test2', description='test')
    #     self.dbsession.add(item)
    #     self.dbsession.commit()
    #     collection = man.get_collection()
    #     assert(len(collection) > 1)
