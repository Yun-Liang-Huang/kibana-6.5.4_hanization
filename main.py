#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import json

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    pass


class Translate(object):
    def __init__(self, dir):
        self.kibana_dir = dir
        self.tran_file_ext = ["js", "html", "json"]
        f = open("./config/kibana_resource.json", "r", encoding="utf-8")
        self.resource = json.loads(f.read())
        f.close()

    def tran(self):
        for root, dirs, files in os.walk(self.kibana_dir):
            for file in files:
                if self.checkFile(file, self.tran_file_ext) == False:
                    continue
                source_path = "%s/%s"%(root.replace('\\', '/'), file.replace('\\', '/'))
                f = open(source_path, "r", encoding="utf-8")
                content = f.read()
                f.close()
                changed = False  # flag to show whether this document has changed
                for item in self.resource:
                    path = item.get("path", "")
                    if source_path.find(str(path)) == -1:
                        continue
                    en = item.get("en", "")
                    cn = item.get("cn", "")
                    if en == "" or cn == "":
                        continue
                    if content.find(str(en)) != -1:
                        content = content.replace(en, cn)  # translate words
                        changed = True
                if changed:
                    print("[%s] has translated" %source_path)
                    f = open(source_path, "w", encoding="utf-8")
                    f.write(str(content))
                    f.close()


    def checkFile(self, file, whitelist):
        if whitelist == []:
            return True
        ext = os.path.splitext(file)[1]
        if ext.strip('.') in whitelist:
            return True
        else:
            return False

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            dir = sys.argv[1]
            obj = Translate(dir)
            obj.tran()
            print("Kibana translated successfully")
        except Exception as e:
            print("Kibana failed to translate")
    else:
        print("example: python main.py \"/opt/kibana-5.6.2-darwin-x86_64/\"")