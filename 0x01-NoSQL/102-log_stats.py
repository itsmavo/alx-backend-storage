#!/usr/bin/env python3
''' Task 102 '''
from pymongo import MongoClient


def nginx_stats_check():
    """ provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient()
    collection = client.logs.nginx

    num_docs = collection.count_documents({})
    print("{} logs".format(num_docs))
    print("Methods:")
    methods_list = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods_list:
        method_cnt = collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_cnt))
    status = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

    print("IPs:")

    t_IPs = collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for t_ip in t_IPs:
        cnt = t_ip.get("count")
        ip_addr = t_ip.get("ip")
        print("\t{}: {}".format(ip_addr, cnt))

if __name__ == "__main__":
    nginx_stats_check()
