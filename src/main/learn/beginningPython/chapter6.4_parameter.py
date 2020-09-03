# -*- coding: UTF-8 -*-

def init(data):
    data['first'] = {}
    data['middel'] = {}
    data['last'] = {}

def lookup(data, label, name):
    return data[label].get(name)


def store(data, full_name):
    names = full_name.split()
    if len(names) == 2 : names.insert(1, '')
    labels = 'first', 'middle', 'last'
    for label, name in zip(labels, names):
        people = lookup(data, label, name)
        if people:
            people.append(full_name)
        else:
            data[label][name] = [full_name]

def chapter6_parameter():
    my_name = {}
    init(my_name)
    store(my_name, 'Cao Weidong')
    lookup(my_name, 'middle', 'lie')


