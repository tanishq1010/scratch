from pymongo import MongoClient
import pandas as pd
def learning_objects_collection():
    client = MongoClient(
        "mongodb://ro_dsl:EHJpUwVO2vgMuk@10.141.11.78/contentgrail")
    database = client["contentgrail"]

    return database["learning_objects"]


def learning_maps_collection():
    client = MongoClient(
        "mongodb://ro_dsl:EHJpUwVO2vgMuk@10.141.11.78/contentgrail")
    database = client["contentgrail"]

    return database["learning_maps"]


def getLmCodes(questions):
    collection = learning_objects_collection()
    query = {}
    query["id"] = {"$in": questions}

    return list(collection.distinct("content.question_meta_tags.learning_maps", query))


def getLearningMapByLMCode(lm_codes):
    collection = learning_maps_collection()
    query = {}
    query['code'] = {"$in": lm_codes}
    query['status'] = "active"

    projection = {}
    projection["learnpath_name"] = 1.0
    projection["code"] = 1.0

    cursor = collection.find(query, projection=projection)
    lms = {}

    for doc in list(cursor):
        lms[doc.get("code")] = doc.get("learnpath_name")

    return lms


def getLearnpathForQuestionId(questions):
    lm_code_mapping = getLearningMapByLMCode(getLmCodes(questions))

    collection = learning_objects_collection()
    query = {}
    query["id"] = {"$in": questions}

    projection = {}
    projection["id"] = 1.0
    projection["content.question_meta_tags.learning_maps"] = 1.0

    cursor = collection.find(query, projection=projection)

    questionLearnPathMap = {}
    for doc in list(cursor):
        _id = doc.get("id")
        learning_maps = []
        for question_meta_tag in doc.get("content", {}).get("question_meta_tags", []):
            for lm in question_meta_tag.get("learning_maps", []):
                if lm_code_mapping.get(lm) != None:
                    learning_maps.append(lm_code_mapping.get(lm))

            questionLearnPathMap[_id] = str(set(learning_maps))[1:-1]

    return questionLearnPathMap


def get_question_data():
    collection = learning_objects_collection()
    querry = {}
    querry['status'] = {'$in': ['Published', 'published', 'Published UAT Accepted']}
    querry['type'] = 'Video'
    projection = {}
    projection['id'] = 1
    projection['_id'] = 0
    projection['content.augmented_attributes.app_title'] = 1
    cursor = collection.find(querry, projection=projection)
    df = pd.DataFrame(columns=['id', 'Title'])
    for doc in list(cursor):
        try:
            title = doc['content']['augmented_attributes']['app_title']
        except:
            title = 'NONE'
        try:
            id = doc['id']
        except:
            id = "NONE"
        df.loc[len(df)] = [id, title]

    return df


def CG_identifier():
    df1 = get_question_data()
    question_id_list = df1['id'].to_list()
    learnpathForQuestionId = getLearnpathForQuestionId(question_id_list)
    # print(learnpathForQuestionId)
    df = pd.DataFrame(columns=['Goal', 'Exam', 'Id', 'Question_code', 'Learnpath_name', 'Title'])
    for key in learnpathForQuestionId:
        LIST = learnpathForQuestionId[key]
        LIST = ''.join(LIST.split("'"))
        LIST = LIST.split(',')
        df_test = df1.loc[df1['id'] == key]
        df_test.reset_index(inplace=True)
        title = df_test['Title'][0]
        for lp in LIST:
            try:
                goal = lp.split('--')[0]
                exam = lp.split('--')[1]

                df.loc[len(df)] = [goal, exam, key, '', lp, title]
            except:
                df.loc[len(df)] = ['', '', key, '', lp, title]
    # print(df)
    df = df[['Goal', 'Exam', 'Id', 'Learnpath_name', 'Title']]
    df.to_csv('CG_DATA.csv', index=False)
CG_identifier()
