#!/usr/bin/env python3
''' Task 11 '''

def schools_by_topic(mongo_collection, topic):
    ''' Returns schools by specific topics '''
    topic_fil = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
                },
            },
        }
    return [doc for doc in mongo_collection.find(topic_fil)]
