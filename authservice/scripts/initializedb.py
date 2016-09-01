from sqlalchemy import create_engine

from inventoryservice import models
from inventoryservice.models.meta import Base
from sqlalchemy.orm import sessionmaker


class InitializeDb(object):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def initialize_db(self):
        engine = create_engine(self.connection_string)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        # create a configured "Session" class
        Session = sessionmaker(bind=engine)

        # create a Session
        dbsession = Session()

        # t = models.ValueType('text')
        # i = models.ValueType('integer')
        # b = models.ValueType('boolean')
        # d = models.ValueType('decimal')
        # c = models.ValueType('currency')
        # dt = models.ValueType('datetime')
        # dbsession.add_all([t, i, b, d, c, dt])
        # dbsession.commit()
        #
        # man = models.Manufacturer(name='test', description='test manufacturer')
        # dbsession.add(man)
        # dbsession.commit()
        #
        # mod = models.Model(name='version', description='test', manufacturer_id=man.id)
        #
        # asset_key = models.AssetKey(key='serial_number', value_type_id=t.id, description='serial number', scannable=True)
        #
        # asset_type = models.AssetType(name='router', description='its a router')
        #
        # dbsession.add_all([mod, asset_type, asset_key])
        # dbsession.commit()
        #
        # asset_type_key = models.AssetTypeKey(asset_key_id=asset_key.id, asset_type_id=asset_type.id, required=True)
        #
        # asset = models.Asset(manufacturer_id=man.id, model_id=mod.id, asset_type_id=asset_type.id)
        #
        # dbsession.add_all([asset_type_key, asset])
        # dbsession.commit()
        #
        # asset_value = models.AssetValue(asset_type_key_id=asset_type_key.id,
        #                                 asset_type_id=asset_type.id,
        #                                 asset_id=asset.id,
        #                                 value='dkfjalkdj',
        #                                 value_type='text')
        #
        # dbsession.add(asset_value)
        # dbsession.commit()
