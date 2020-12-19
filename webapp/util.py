from webapp import db
from webapp.db_models import Interestarea


def get_interest_from_db(i,company_details_id):
    db_instance = Interestarea.query.filter_by(name = i).first()
    if db_instance: #exist in db
        #check if that one already belongs to company, if so don't add again
        if company_details_id in db_instance.companydetails:
            return None
        return db_instance
    return Interestarea(name=i)

def get_interests(interests_string,company_details_id):
    interests_array = interests_string.split(",")

    for index, i in enumerate(interests_array):
        i = i.lstrip()
        i = i.rstrip()
        interests_array[index] = i

    interest_objects = []

    for i in interests_array:
        if len(i) == 0:continue # do not count empty string
        obj = get_interest_from_db(i,company_details_id)
        if obj:
            interest_objects.append(obj)

    return interest_objects

def get_business_keywords(user):
    ads = user.company_details.advertisements
    
    business_keywords = []
    for ad in ads:
        keys = ad.keywords
        if len(keys)>0:
            for key in keys:
                if key not in business_keywords:
                    business_keywords.append(key)


    if len(business_keywords) > 10:
        return business_keywords[0:10]
    elif len(business_keywords) == 0:
        return None
    else : return business_keywords