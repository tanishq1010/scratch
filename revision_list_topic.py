
import json

from common.es_search_queries import get_revision_list_topic_query
from config.es_index_config import get_index_config
from config.es_server_config import get_es_host_config
from elasticsearch import Elasticsearch, helpers


class RevisionListTopic(object):


    def __init__(self, env='dev', logger=None):
        self.env = env
        self.logger = logger
        self.doc_type ='doc'
        es_bundle = get_es_host_config(self.env)
        self.es_port = es_bundle.get("port")
        self.es_host = es_bundle.get("host")
        es_index_dict = get_index_config(env)

        self.TEST_ATTEMPTS = es_index_dict.get('SANITIZED_TEST_ATTEMPTS', '')
        self.PRACTICE_ATTEMPTS = es_index_dict.get('SANITIZED_PRACTICE_ATTEMPTS', '')

        try:
            self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        except Exception as e:
            logger.error("Can not connect to ES:"%e, exc_info=True)

    """
    This method is used to retrieve all the documents from elasticsearch
    """
    def get_es_data(self, es_query, es_index):
        try:
            es_response = helpers.scan(
                client=self.es,
                scroll='2m',
                query=es_query,
                index=es_index)

            attempts = []
            for document in es_response:
                attempts.append(document['_source'])

            return attempts
        except Exception as ex:
            print(ex)
            return []

    """
    Validates if all the mandatory parameters are present
    """
    def input_validation(self, params_dict):
        for key in params_dict.keys():
            if len(str(params_dict[key])) == 0:
                return key
        return None

    """
    Driver function for the class.
    """
    def get_revision_list_topic(self, params_dict):
        try:
            input_validation_output = self.input_validation(params_dict)

            if input_validation_output is not None:
                return {'Error': '{} parameter missing.'.format(input_validation_output)}

            for field in ['user_id', 'learnpath_name', 'learnpath_format']:
                if field not in params_dict:
                    return {'Error': '{} parameter missing.'.format(field)}

            user_id = params_dict.get('user_id', None)
            learnpath_name = params_dict.get('learnpath_name', None)
            learnpath_format = params_dict.get('learnpath_format', None)
            threshold_factor = int(params_dict.get('threshold_factor', None))
            section_name = params_dict.get('section_name', None)
            offset = params_dict.get('offset', None)
            limit = params_dict.get('limit', None)
            topic_code = params_dict.get('topic_code',None)


            test_query, practice_query = get_revision_list_topic_query(user_id, learnpath_name, learnpath_format, offset, limit)
            test_index = self.TEST_ATTEMPTS
            practice_index = self.PRACTICE_ATTEMPTS
            test_attempts, practice_attempts = [], []
            try:
                test_attempts = self.get_es_data(test_query, test_index)
                practice_attempts = self.get_es_data(practice_query, practice_index)
            except Exception as ex:
                return {'Error': 'Error while querying data store.'}
            if len(test_attempts)==0 and len(practice_attempts)==0:
                return {'Error': 'No attempts found for the given user_id and test_code.'}

            attempts = create_uniform_schema(test_attempts, practice_attempts)

            topic_stats_dict, topic_lm_dict = create_topic_wise_stats(attempts)

            response = create_final_response(topic_stats_dict, threshold_factor,topic_lm_dict,section_name,topic_code)

            return response
        except Exception as ex:
            print(ex)
            return None


def create_uniform_schema(test_attempts, practice_attempts):
    uniform_attempt_list = []
    for attempt in test_attempts:
        temp_attempt_dict = {"badge": attempt.get('badge',''),
                             'topic': attempt.get('lm_details',{}).get('new_topic_code',''),
                             'learnpath_name': attempt.get('lm_details',{}).get('learnpath_name',''),
                             'learnpath_code': attempt.get('lm_details',{}).get('learnpath_code',''),
                             'lm_code': attempt.get('lm_details',{}).get('lm_code',''),
                             'lm_format_reference': attempt.get('lm_details',{}).get('lm_format_reference','')
                             }
        uniform_attempt_list.append(temp_attempt_dict)

    for attempt in practice_attempts:
        if attempt['attemptTypeBadge'] == 'Wasted':
            attempt['attemptTypeBadge'] = 'wasted-attempt'
        elif attempt['attemptTypeBadge'] == 'OvertimeCorrect':
            attempt['attemptTypeBadge'] = 'overtime-correct'
        elif attempt['attemptTypeBadge'] == 'OvertimeIncorrect':
            attempt['attemptTypeBadge'] = 'overtime-incorrect'
        elif attempt['attemptTypeBadge'] == 'Incorrect':
            attempt['attemptTypeBadge'] = 'normal-incorrect'

        temp_attempt_dict = {"badge": attempt.get('attemptTypeBadge',''),
                             'topic': attempt.get('lm_details',{}).get('new_topic_code',''),
                             'learnpath_name': attempt.get('lm_details',{}).get('learnpath_name',''),
                             'learnpath_code': attempt.get('lm_details',{}).get('learnpath_code',''),
                             'lm_code': attempt.get('lm_details',{}).get('lm_code',''),
                             'lm_format_reference': attempt.get('lm_details',{}).get('lm_format_reference','')
                             }
        uniform_attempt_list.append(temp_attempt_dict)

    return uniform_attempt_list


def create_topic_wise_stats(attempts):
    topic_stats_dict = {}
    topic_lm_dict = {}

    for attempt in attempts:
        topic = attempt['topic']
        badge = attempt['badge']
        learnpath_name = attempt['learnpath_name']
        learnpath_code = attempt['learnpath_code']
        lm_code = attempt['lm_code']
        lm_format_reference = attempt['lm_format_reference']
        topic_lm_dict[topic] = {'learnpath_name': learnpath_name,
                                'learnpath_code': learnpath_code,
                                'lm_code':lm_code,
                                'lm_format_reference': lm_format_reference
                                }
        if topic in topic_stats_dict:
            temp_topic_dict = topic_stats_dict[topic]
            temp_topic_dict['total'] += 1
            if badge in temp_topic_dict:
                temp_topic_dict[badge] += 1
            else:
                temp_topic_dict[badge] = 1
        else:
            temp_topic_dict = {'total': 1, str(badge): 1}
            topic_stats_dict[topic] = temp_topic_dict

    return topic_stats_dict, topic_lm_dict

def filter_topic(topic_code,res_list):
    if topic_code:
        for i in res_list:
            if i['topic_code'] == topic_code:
                response = [i]
                break
            else:
                response = []
        return response
    else:
        return res_list

def create_final_response(topic_stats_dict, threshold_factor, topic_lm_dict, section_name, topic_code):
    response  = {}
    topics_i_made_careless_mistake = []
    topics_i_went_overtime_incorrect = []
    topics_i_went_overtime = []
    topics_i_went_wrong = []

    for key in topic_stats_dict.keys():
        topic_dict = topic_stats_dict[key]

        if 'wasted-attempt' in topic_dict:
            score = topic_dict['wasted-attempt']/topic_dict['total']*100
            if score > threshold_factor:
                topics_i_made_careless_mistake.append({"topic_code":key,
                                                       "score": score,
                                                       'learnpath_name': topic_lm_dict[key]['learnpath_name'],
                                                       'learnpath_code': topic_lm_dict[key]['learnpath_code'],
                                                       'lm_code': topic_lm_dict[key]['lm_code'],
                                                       'lm_format_reference': topic_lm_dict[key]['lm_format_reference']
                                                       })
        if 'overtime-incorrect' in topic_dict:
            score = topic_dict['overtime-incorrect']/topic_dict['total']*100
            if score > threshold_factor:
                topics_i_went_overtime_incorrect.append({"topic_code":key,"score": score,
                                                       'learnpath_name': topic_lm_dict[key]['learnpath_name'],
                                                       'learnpath_code': topic_lm_dict[key]['learnpath_code'],
                                                       'lm_code': topic_lm_dict[key]['lm_code'],
                                                       'lm_format_reference': topic_lm_dict[key]['lm_format_reference']
                                                         })
        if 'overtime-incorrect' in topic_dict or 'overtime-correct' in topic_dict:
            overtime_attempt_count = topic_dict.get('overtime-incorrect', 0) + topic_dict.get('overtime-correct', 0)
            score = overtime_attempt_count/topic_dict['total']*100
            if score > threshold_factor:
                topics_i_went_overtime.append({"topic_code":key,"score":score,
                                                       'learnpath_name': topic_lm_dict[key]['learnpath_name'],
                                                       'learnpath_code': topic_lm_dict[key]['learnpath_code'],
                                                       'lm_code': topic_lm_dict[key]['lm_code'],
                                                       'lm_format_reference': topic_lm_dict[key]['lm_format_reference']
                                               })
        if 'overtime-incorrect' in topic_dict or 'wasted-attempt' in topic_dict or 'normal-incorrect' in topic_dict:
            incorrect_attempt_count = topic_dict.get('overtime-incorrect', 0) + topic_dict.get('wasted-attempt', 0) + topic_dict.get('normal-incorrect', 0)
            score = incorrect_attempt_count/topic_dict['total']*100
            if score > threshold_factor:
                topics_i_went_wrong.append({"topic_code":key,"score": score,
                                                       'learnpath_name': topic_lm_dict[key]['learnpath_name'],
                                                       'learnpath_code': topic_lm_dict[key]['learnpath_code'],
                                                       'lm_code': topic_lm_dict[key]['lm_code'],
                                                       'lm_format_reference': topic_lm_dict[key]['lm_format_reference']})

    response['topics_i_made_careless_mistake'] = topics_i_made_careless_mistake
    response['topics_i_went_overtime_incorrect'] = topics_i_went_overtime_incorrect
    response['topics_i_went_overtime'] = topics_i_went_overtime
    response['topics_i_went_wrong'] = topics_i_went_wrong

    if section_name == 'topics_i_made_careless_mistake':
        response = filter_topic(topic_code,topics_i_made_careless_mistake)
    elif section_name == 'topics_i_went_overtime_incorrect':
        response = filter_topic(topic_code,topics_i_went_overtime_incorrect)
    elif section_name == 'topics_i_went_overtime':
        response = filter_topic(topic_code,topics_i_went_overtime)
    elif section_name == 'topics_i_went_wrong':
        response = filter_topic(topic_code,topics_i_went_wrongs)

    return response

