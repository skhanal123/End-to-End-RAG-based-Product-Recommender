from .database import MongoEngine
from .config import settings


def fetch_userProfile(user_name):
    """
    This function is use to fetch user profile from mongo db
    """
    try:
        database = MongoEngine.client[settings.mongodb_userprofile]
        collection = database[settings.mongodb_userprofile_collection]
        profile = collection.find({"user_name": user_name})
        return profile[0]
    except Exception as e:
        return {"response": "Couldn't fetch user profile data from database"}


def update_userProfile(user_id, response):
    """This function is used to update the user profile whenever new attribute is found about user"""
    try:
        database = MongoEngine.client[settings.mongodb_userprofile]
        collection = database[settings.mongodb_userprofile_collection]

        query = {"user_id": user_id}
        profile = collection.find(query)
        categories = profile["preferences"]["categories"]

        updated_categories = categories.append(response["response"])

        if "No" in updated_categories:
            return {"response": "User profile need not update"}
        else:
            update_operation = {"$set": {"preference.categories": updated_categories}}

            collection.update_one(query, update_operation)

            return {"response": "User profile updated"}

    except Exception as e:
        return {"response": "User profile update failed"}
