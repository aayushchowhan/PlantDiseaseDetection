from google.cloud.firestore_v1.document import DocumentReference
from typing import List
from firebaseconfig.firebase import add_data_one , add_subcollection_data , get_ref
import json

from datetime import datetime
with open('./PlantDiseaseDetection/cache/FarmField.json' , 'r') as f:
    FarmField=json.load(f)


class FarmerField:
    # Properties
    num_of_node: int
    dimention : str
    ref: DocumentReference

    # Constructor
    def __init__(self, num_of_node, dimention='1000mx1000m'):
        self.num_of_node = num_of_node
        self.dimention=dimention

    # Method to create a new shoe document
    def create(self):
        da={
                'num_of_node':self.num_of_node,
                'dimention':self.dimention
                
            }
        self.ref = add_data_one(
            collection='FarmerField',
            data=da
        )
        with open('./cache/FarmField.json' , 'w') as f:
            FarmField[self.ref.id]=self.to_dict()
            json.dump(FarmField,f,indent=6)
        return self

    # Method to convert shoe data to a dictionary
    def to_dict(self):
        return {
            'num_of_node':self.num_of_node,
            'dimention':self.dimention
        }

# Class for representing brand data
class Node:
    # Properties
    no_of_hands:int
    farmerfieldRef:DocumentReference
    ref: DocumentReference

    class Hand:
        # Properties
        no_of_sensors:int
        ref: DocumentReference
        # Constructor
        def __init__(self , outer, no_of_sensors ):
            self.no_of_sensors=no_of_sensors
            self.outer=outer


        def update(self):
            self.ref = add_subcollection_data(
                collection='Node',
                subcollection='Hand',
                doc_id=self.outer.ref.id,
                data={
                    'no_of_sensors':self.no_of_sensors,
                },
                subCollectionDocId=self.ref.id
            )
            return self

        def create(self):
            self.ref = add_subcollection_data(
                collection='Node',
                subcollection='Hand',
                doc_id=self.outer.ref.id,
                data={
                    'no_of_sensors':self.no_of_sensors,
                }
            )
            with open('./cache/FarmField.json' , 'w') as f:
                dict=self.to_dict()
                if 'hands' in  FarmField[self.outer.farmerfieldRef.id]['nodes'][self.outer.ref.id]:
                    FarmField[self.outer.farmerfieldRef.id]['nodes'][self.outer.ref.id]['hands'][self.ref.id]=dict
                else :
                    FarmField[self.outer.farmerfieldRef.id]['nodes'][self.outer.ref.id]['hands']={}
                    FarmField[self.outer.farmerfieldRef.id]['nodes'][self.outer.ref.id]['hands'][self.ref.id]=dict
                json.dump(FarmField,f,indent=6)
            return self

        # Method to convert brand data to a dictionary
        def to_dict(self):
            return {
                    'no_of_sensors':self.no_of_sensors,
                }
    # Constructor
    def __init__(self, no_of_hands , farmerfieldRef):
        self.no_of_hands=no_of_hands
        self.farmerfieldRef=farmerfieldRef
    
    @classmethod
    def get(cls,docid):
        cls.ref=get_ref('Node',doc_id=docid)
        return cls
    def update(self):
        self.ref = add_data_one(
            collection='Node',
            data={
                'no_of_hands':self.no_of_hands,
                'farmerfieldRef':self.farmerfieldRef
            },
            doc_id=self.ref.id
        )
        return self
    
    def create(self):
        self.ref = add_data_one(
            collection='Node',
            data={
                'no_of_hands':self.no_of_hands,
                'farmerfieldRef':self.farmerfieldRef
            }
        )
        with open('./PlantDiseaseDetection/cache/FarmField.json' , 'w') as f:
            dict=self.to_dict()
            del dict['farmerfieldRef']
            if 'nodes' in  FarmField[self.farmerfieldRef.id]:
                FarmField[self.farmerfieldRef.id]['nodes'][self.ref.id]=dict
            else :
                FarmField[self.farmerfieldRef.id]['nodes']={}
                FarmField[self.farmerfieldRef.id]['nodes'][self.ref.id]=dict
            json.dump(FarmField,f,indent=6)
        return self

    # Method to convert brand data to a dictionary
    def to_dict(self):
        return {
                'no_of_hands':self.no_of_hands,
                'farmerfieldRef':self.farmerfieldRef
            }
    

class FieldData:
    # Properties
    HandRef:DocumentReference
    phsensor_value:int
    moituresensor_value:int
    ref: DocumentReference

    # Constructor
    def __init__(self, HandRef, phsensor_value=0,moituresensor_value=0):
        self.HandRef=HandRef
        self.phsensor_value=phsensor_value
        self.moituresensor_value=moituresensor_value

    # Method to create a new shoe document
    def create(self):
        da={
                'HandRef':self.HandRef,
                'phsensor_value':self.phsensor_value,
                'moituresensor_value':self.moituresensor_value,
                'createdAt': datetime.now()
                
            }
        self.ref = add_data_one(
            collection='FieldData',
            data=da
        )
        return self

    # Method to convert shoe data to a dictionary
    def to_dict(self):
        return {
                'HandRef':self.HandRef,
                'phsensor_value':self.phsensor_value,
                'moituresensor_value':self.moituresensor_value,
                
            }