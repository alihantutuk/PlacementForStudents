from webapp import db
from webapp.db_models import User,Studentdetail,Advertisement,Keyword


# from sklearn.feature_extraction.text import CountVectorizer
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity


def get_student_keywords():

    keywords = []
    userids = []

    users = User.query.all()
    for u in users:

        if u.type == False:continue
        if u.student_details is None:continue

        user_keywords = u.student_details.keywords
        if user_keywords is not None and len(user_keywords)>0:
            keyword_string = ""
            for k in user_keywords:
                keyword_string += (k.name).replace(' ','') +" "

            keywords.append(keyword_string)
            userids.append(u.id)



    return keywords,userids

#ad id
def get_matching(id):
    ad = Advertisement.query.filter_by( id=id ).first()
    ad_keywords = ""
    if ad.keywords is None or len(ad.keywords) == 0:
        print("Non Key Error")
        return

    for k in ad.keywords:
        ad_keywords+=k.name.replace(' ','')+" "

    keywords,userids = get_student_keywords()
    keywords.append(ad_keywords)
    print("keywords : ",keywords," ids : ",userids)


    # df = pd.DataFrame(keywords,columns=['keywords'])
    # cv = CountVectorizer(token_pattern = '[a-zA-Z0-9$&+,:;=?@#|<>.^*()%!-]+')
    # count_matrix = cv.fit_transform(df['keywords'])

    # similarity_scores = cosine_similarity(count_matrix)

    # studentpoints = similarity_scores[-1][:-1]
    # studentindex = [i[0] for i in sorted(enumerate(studentpoints), key=lambda x:x[1],reverse=True)]
    # selected_ids = []
    # for i, s in enumerate(studentindex):
    #    if i>=20:break
    #    selected_ids.append(ids[s])

    #BUNDAN SONRA BU OGRENCI ID DEGERLERINI MATCHING OLARAK EKLE !


get_matching(1)




