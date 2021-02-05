import pymongo
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
from tqdm import tqdm
import time


def connect_to_cg():
    client = MongoClient(
        "mongodb://ro_dsl:EHJpUwVO2vgMuk@10.141.11.78/contentgrail?authSource=contentgrail&replicaSet=cg-mongo-prod&readPreference=secondaryPreferred")
    db = client["contentgrail"]
    return db


def is_in(x, valid_list):
    return any([_x in valid_list for _x in x])


def get_all_books(cg_db, valid_goals_list, valid_exams_list):
    collection = cg_db.learning_map_formats
    query = {"type": "book",
             "locales.en.status": "active"}

    if valid_goals_list != None:
        query["locales.en.content.syllabuses"] = {"$in": valid_goals_list}
        query["content.grade"] = {"$in": valid_exams_list}

    get_all_books = collection.find(query)

    books = []
    for book in list(get_all_books):
        for exam in book['content']['grade']:
            if exam in valid_exams_list:
                rank = 999
                try:
                    if 'rank' in book['content']:
                        for exam_rank in book['content']['rank']:
                            if exam_rank.split('--')[1] == exam.lower():
                                rank = book['content']['rank'][exam_rank]
                except Exception as e:
                    pass

                book_doc = {
                    'Book Code': book['content']['book_code'],
                    'Exam': exam,
                    'Exam Wise Rank': rank
                }

                book_doc["Book Id"] = book.get("path", "Na")
                if 'subjects' in book['locales']['en']['content']:
                    book_doc['Subject'] = book['locales']['en']['content']['subjects']
                else:
                    book_doc['Subject'] = ""

                book_doc['Book Name'] = None
                if 'display_name' in book['locales']['en']:
                    book_doc['Book Name'] = book['locales']['en']['display_name']

                book_doc['Publisher'] = None
                if 'publication' in book['content']:
                    book_doc['Publisher'] = book['content']['publication']

                # book_doc['Author'] = None
                # if 'authors' not in book['content']:
                # 	book_doc['Author'] =  ", ".join(book['content']['authors'])

                book_doc['Author'] = None
                if 'authors' in book['content']:
                    book_doc['Author'] = ", ".join(book['content']['authors'])

                books.append(book_doc)

    df_books = pd.DataFrame(books)

    df_books = df_books.sort_values(by=['Exam', 'Exam Wise Rank'])
    return df_books


def get_active_book_list():
    goal_to_check, exam_to_check = None, None
    # print("Getting all active books from CG")
    cg_db = connect_to_cg()
    if exam_to_check != None:
        valid_goals_list = [goal_to_check]
        valid_exams_list = [exam_to_check]
    else:
        valid_goals_list = ["CBSE",
                            "ICSE",
                            "Tamil Nadu Board",
                            "Maharashtra Board",
                            "Rajasthan Board",
                            "Engineering",
                            "Medical",
                            "Banking",
                            "Insurance",
                            "Railways",
                            "SSC",
                            "Teaching",
                            "Defence",
                            "Jammu and Kashmir Board",
                            "National Recruitment Agency",
                            "Telangana Board",
                            "Karnataka Board",
                            "Kerala Board",
                            "Uttar Pradesh Board"]
        valid_exams_list = ["1st CBSE",
                            "2nd CBSE",
                            "3rd CBSE",
                            "4th CBSE",
                            "5th CBSE",
                            "6th CBSE",
                            "7th CBSE",
                            "8th CBSE",
                            "9th CBSE",
                            "10th CBSE",
                            "11th CBSE",
                            "12th CBSE",
                            "1st ICSE",
                            "2nd ICSE",
                            "3rd ICSE",
                            "4th ICSE",
                            "5th ICSE",
                            "6th ICSE",
                            "7th ICSE",
                            "8th ICSE",
                            "9th ICSE",
                            "10th ICSE",
                            "11th ICSE",
                            "12th ICSE",
                            "1st Tamil Nadu State Board",
                            "2nd Tamil Nadu State Board",
                            "3rd Tamil Nadu State Board",
                            "4th Tamil Nadu State Board",
                            "5th Tamil Nadu State Board",
                            "6th Tamil Nadu State Board",
                            "7th Tamil Nadu State Board",
                            "8th Tamil Nadu State Board",
                            "9th Tamil Nadu State Board",
                            "10th Tamil Nadu State Board",
                            "11th Tamil Nadu State Board",
                            "12th Tamil Nadu State Board",
                            "1st Maharashtra Board",
                            "2nd Maharashtra Board",
                            "3rd Maharashtra Board",
                            "4th Maharashtra Board",
                            "5th Maharashtra Board",
                            "6th Maharashtra Board",
                            "7th Maharashtra Board",
                            "8th Maharashtra Board",
                            "9th Maharashtra Board",
                            "10th Maharashtra Board",
                            "11th Maharashtra Board",
                            "12th Maharashtra Board",
                            "1st RBSE",
                            "2nd RBSE",
                            "3rd RBSE",
                            "4th RBSE",
                            "5th RBSE",
                            "6th RBSE",
                            "7th RBSE",
                            "8th RBSE",
                            "9th RBSE",
                            "10th RBSE",
                            "11th RBSE",
                            "12th RBSE",
                            "JEE Main",
                            "JEE Advanced",
                            "MHT-CET",
                            "BITSAT",
                            "AP EAMCET",
                            "VITEEE",
                            "VITEEE (with Biology)",
                            "KCET (UG)",
                            "SRMJEEE (UG)",
                            "BITSAT (with Biology)",
                            "AMU-AT (B.Tech.)",
                            "TS EAMCET",
                            "NEET",
                            "Bihar Cooperative Bank Assistant Prelims",
                            "RBI Assistant Prelims",
                            "IBPS PO Mains",
                            "IBPS RRB Officer Scale-I Prelims",
                            "IBPS Clerk Prelims",
                            "IBPS Clerk Mains",
                            "IBPS RRB Office Assistant Mains",
                            "IBPS RRB Office Assistant Prelims",
                            "IBPS PO Prelims",
                            "SBI PO Mains",
                            "IBPS RRB Officer Scale-I Mains",
                            "SBI Clerk Prelims",
                            "SBI Clerk Mains",
                            "SBI PO Prelims",
                            "LIC AAO Prelims",
                            "NIACL Assistant Prelims",
                            "LIC Assistant Prelims",
                            "Insurance",
                            "RPF Sub Inspector CBT 1",
                            "RPF Constable CBT 1",
                            "RRC Group D CBT",
                            "RRB NTPC CBT 1",
                            "Railways",
                            "IB Security Assistant or Executive Tier 1",
                            "SSC Stenographer Grade C and D",
                            "SSC CPO Paper-I",
                            "Delhi Police Constable CBT",
                            "SSC MTS Tier I",
                            "SSC CHSL Tier-I",
                            "SSC CGL Tier-I",
                            "SSC",
                            "CTET Paper 1",
                            "CTET Paper 2",
                            "DRDO MTS Tier I",
                            "CISF Head Constable",
                            "Defence",
                            "1st Jammu and Kashmir Board",
                            "2nd Jammu and Kashmir Board",
                            "3rd Jammu and Kashmir Board",
                            "4th Jammu and Kashmir Board",
                            "5th Jammu and Kashmir Board",
                            "6th Jammu and Kashmir Board",
                            "7th Jammu and Kashmir Board",
                            "8th Jammu and Kashmir Board",
                            "9th Jammu and Kashmir Board",
                            "10th Jammu and Kashmir Board",
                            "11th Jammu and Kashmir Board",
                            "12th Jammu and Kashmir Board",
                            "NRA CET - Graduate Level",
                            "NRA CET - Higher Secondary Level",
                            "NRA CET - Matriculation Level",
                            "1st Telangana State Board",
                            "2nd Telangana State Board",
                            "3rd Telangana State Board",
                            "4th Telangana State Board",
                            "5th Telangana State Board",
                            "6th Telangana State Board",
                            "7th Telangana State Board",
                            "8th Telangana State Board",
                            "9th Telangana State Board",
                            "10th Telangana State Board",
                            "11th Telangana State Board",
                            "12th Telangana State Board",
                            "1st Karnataka State Board",
                            "2nd Karnataka State Board",
                            "3rd Karnataka State Board",
                            "4th Karnataka State Board",
                            "5th Karnataka State Board",
                            "6th Karnataka State Board",
                            "7th Karnataka State Board",
                            "8th Karnataka State Board",
                            "9th Karnataka State Board",
                            "10th Karnataka State Board",
                            "11th Karnataka State Board",
                            "12th Karnataka State Board",
                            "1st Kerala Board",
                            "2nd Kerala Board",
                            "3rd Kerala Board",
                            "4th Kerala Board",
                            "5th Kerala Board",
                            "6th Kerala Board",
                            "7th Kerala Board",
                            "8th Kerala Board",
                            "9th Kerala Board",
                            "10th Kerala Board",
                            "11th Kerala Board",
                            "12th Kerala Board",
                            "9th Uttar Pradesh Board",
                            "10th Uttar Pradesh Board",
                            "11th Uttar Pradesh Board",
                            "12th Uttar Pradesh Board"]
    # get_all_books(cg_db, valid_goals_list, valid_exams_list)
    df_books = get_all_books(cg_db, valid_goals_list, valid_exams_list)
    df_books.to_csv("Books_List.csv", encoding='utf-8', index=False)

    print("Done\n")