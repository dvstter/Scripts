#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import redis
import json
import re
import argparse

class Database:
    Pool = None
    Init = False

    def __init__(self):
        if not type(self).Init:
            try:
                type(self).Pool = redis.BlockingConnectionPool(host="127.0.0.1", port=6379)
                type(self).Init = True
            except redis.exceptions.ConnectionError as _:
                self.conn = None
                print("Cannot create ConnectionPool")

        self.conn = redis.StrictRedis(connection_pool=type(self).Pool)

    def get_all_ids(self):
        return [x.decode("ascii")[5:] for x in self.conn.keys("href:*")]

    def get_title(self, jid):
        return self.conn.get("title:"+jid).decode("utf-8")

    def get_href(self, jid):
        return self.conn.get("href:"+jid).decode("utf-8")

    def get_players(self, jid):
        return [x.decode("utf-8") for x in self.conn.lrange("players:"+jid, 0, -1)]
        
    def store(self, filename):
        f = open(filename, "r", encoding="utf-8")
        infos = f.readlines()
        f.close()
        for idx in range(int(len(infos) / 6)):
            href = infos[idx*6+1].strip()[5:]
            jid = infos[idx*6+2].strip()[4:]
            title = infos[idx*6+3].strip()[6:]
            players = re.findall(r"'(.+?)'", infos[idx*6+4].strip()[8:])
    
            if self.conn.keys("href:"+jid):
                print("id ({}) existed, will not store into database.".format(jid))
                continue
        
            self.conn.set("href:"+jid, href)
            self.conn.set("title:"+jid, title)
            for each in players:
                self.conn.lpush("players:"+jid, each)

            print("id ({}) infos have been store.".format(jid))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true", default=False, help="list all the JAV ids")
    parser.add_argument("-t", "--title", help="show title of JAV id")
    parser.add_argument("-L", "--link", help="show url of JAV id")
    parser.add_argument("-a", "--actress", help="show all actress of JAV id")
    parser.add_argument("-s", "--search", help="search title from all JAV, all elements joined with +")
    args = parser.parse_args()

    dbs = Database()
    if args.list:
        for each in dbs.get_all_ids():
            name = dbs.get_title(each)
            print("{}:{}".format(each, name))
    elif args.title:
        print(dbs.get_title(args.title))
    elif args.link:
        print(dbs.get_href(args.link))
    elif args.actress:
        for each in dbs.get_players(args.actress):
            print(each)
    elif args.search:
        elements = args.search.split("+")
        for e_id in dbs.get_all_ids():
            e_name = dbs.get_title(e_id)
            flag = True
            for e_ele in elements:
                if e_ele not in e_name:
                    flag = False
                    break
            if flag:
                print("{}:{} matched".format(e_id, e_name))
    else:
        print("Please input -h to get help message.")
