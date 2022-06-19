import json


def str2txt(str_: str, filename: str = None):
    with open(filename, 'a+') as f:
        f.write("%s\n" % str_)


def list2txt(list_: list, filename: str = None):
    with open(filename, 'a+') as f:
        for item in list_:
            f.write("%s\n" % item)


def list2json(list_: list, filename: str = None):
    # json_object = json.dumps(list_, indent=4)
    # with open(filename, "w") as outfile:
    #     json.dump(json_object , outfile)

    with open(filename, 'w') as fp:
        json.dump(list_, fp, indent=4)
