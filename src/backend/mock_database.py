"""
Mock database for testing when MongoDB is not available
"""

import copy
from typing import Dict, Any, List, Optional
from argon2 import PasswordHasher

# In-memory storage
_activities_data = {}
_teachers_data = {}

class MockCollection:
    def __init__(self, data_store):
        self.data_store = data_store
    
    def find_one(self, query):
        if "_id" in query:
            return self.data_store.get(query["_id"])
        return None
    
    def find(self, query=None):
        if query is None or query == {}:
            return [{"_id": k, **v} for k, v in self.data_store.items()]
        return []
    
    def insert_one(self, document):
        doc_id = document.pop("_id")
        self.data_store[doc_id] = document
        return type('Result', (), {'inserted_id': doc_id})()
    
    def update_one(self, query, update):
        if "_id" in query:
            doc_id = query["_id"]
            if doc_id in self.data_store:
                doc = self.data_store[doc_id]
                
                # Handle $push operation
                if "$push" in update:
                    for field, value in update["$push"].items():
                        if field in doc:
                            doc[field].append(value)
                        else:
                            doc[field] = [value]
                
                # Handle $pull operation
                if "$pull" in update:
                    for field, value in update["$pull"].items():
                        if field in doc and value in doc[field]:
                            doc[field].remove(value)
                
                # Handle $addToSet operation
                if "$addToSet" in update:
                    for field, value in update["$addToSet"].items():
                        if field in doc:
                            if "$each" in value:
                                for item in value["$each"]:
                                    if item not in doc[field]:
                                        doc[field].append(item)
                            elif value not in doc[field]:
                                doc[field].append(value)
                        else:
                            if "$each" in value:
                                doc[field] = list(value["$each"])
                            else:
                                doc[field] = [value]
                
                # Handle $pullAll operation
                if "$pullAll" in update:
                    for field, values in update["$pullAll"].items():
                        if field in doc:
                            doc[field] = [x for x in doc[field] if x not in values]
                
                return type('Result', (), {'modified_count': 1})()
        
        return type('Result', (), {'modified_count': 0})()
    
    def count_documents(self, query):
        return len(self.data_store)
    
    def aggregate(self, pipeline):
        results = []
        data = [{"_id": k, **v} for k, v in self.data_store.items()]
        
        for stage in pipeline:
            if "$unwind" in stage:
                field = stage["$unwind"].replace("$", "")
                new_data = []
                for doc in data:
                    field_parts = field.split(".")
                    value = doc
                    for part in field_parts:
                        if part in value:
                            value = value[part]
                        else:
                            value = []
                            break
                    
                    if isinstance(value, list):
                        for item in value:
                            new_doc = copy.deepcopy(doc)
                            # Set the unwound field to the single item
                            current = new_doc
                            for part in field_parts[:-1]:
                                current = current[part]
                            current[field_parts[-1]] = item
                            new_data.append(new_doc)
                data = new_data
            
            elif "$group" in stage:
                group_by = stage["$group"]["_id"]
                if group_by.startswith("$"):
                    group_field = group_by.replace("$", "")
                    groups = {}
                    for doc in data:
                        field_parts = group_field.split(".")
                        value = doc
                        for part in field_parts:
                            if part in value:
                                value = value[part]
                            else:
                                value = None
                                break
                        
                        if value is not None:
                            if value not in groups:
                                groups[value] = []
                            groups[value].append(doc)
                    
                    data = [{"_id": k} for k in groups.keys()]
            
            elif "$sort" in stage:
                sort_field = list(stage["$sort"].keys())[0]
                reverse = stage["$sort"][sort_field] == -1
                data.sort(key=lambda x: x.get(sort_field, ""), reverse=reverse)
        
        return data

# Create mock collections
activities_collection = MockCollection(_activities_data)
teachers_collection = MockCollection(_teachers_data)

def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""
    from .database import initial_activities, initial_teachers
    
    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})