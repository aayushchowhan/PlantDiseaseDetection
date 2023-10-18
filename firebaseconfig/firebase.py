from firebase_admin import firestore,credentials
import typing
from google.cloud.firestore_v1.document import DocumentReference
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./PlantDiseaseDetection/firebaseconfig/cred.json'
cred = credentials.Certificate("./PlantDiseaseDetection/firebaseconfig/cred.json")
# Initialize Firestore client
db = firestore.Client()

# Function to get a DocumentReference for a specific collection and document ID
def get_ref(collection, doc_id):
    return db.collection(collection).document(doc_id)

# Function to add/update data to a document in a collection
def add_data_one(collection, data, doc_id=None):
    if doc_id is None:
        doc_ref = db.collection(collection).document()
    else:
        doc_ref = db.collection(collection).document(doc_id)
    doc_ref.set(data, merge=True)
    return doc_ref

# Function to add/update data to a subcollection document
def add_subcollection_data(collection, doc_id, subcollection, data, subCollectionDocId=None):
    if subCollectionDocId is None:
        doc_ref = db.collection(collection).document(doc_id).collection(subcollection).document()
    else:
        doc_ref = db.collection(collection).document(doc_id).collection(subcollection).document(subCollectionDocId)
        
    doc_ref.set(data, merge=True)
    return doc_ref
