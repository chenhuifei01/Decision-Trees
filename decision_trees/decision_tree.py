import math
import sys
import pandas as pd
import numpy as np

class Node:
    def __init__(self, df):
        self.df = df
        self.children = []
        self.str = None


def gini_gain2(target, split): #3 to 111
    kinds = split.unique()
    names = target.columns
    total = target.shape[0]

    stat = target.groupby([split, target[names[-1]]]).size().to_dict()
    stat2 = split.value_counts().to_dict()
 
    answer = 0
    for k, v in stat2.items():
        first = 0
        second = 0
        if (k,0) in stat.keys():
            first = (stat[(k,0)]/v)**2
        if (k,1) in stat.keys():
            second = (stat[(k,1)]/v)**2
        temp = 1
        temp = (temp - first - second) * v
        answer = answer + temp

    return answer / total


def best_attr(df, names):
    bestgini = 100
    bestname = ''
    for i in names:
        temp = gini_gain2(df,df[i])
        if  temp < bestgini:
            bestgini = temp
            bestname = i
    return bestname


def decision_tree(df, n, names):
    curbest = best_attr(df,names[:-1])
    if curbest == '':
        return
    if gini_gain2(df,df[curbest]) == 0:
        return
    if len(df[df.columns[-1]].unique()) == 1:
        return
    
    if len(df[curbest].unique()) == 1:
        return
    n.str = curbest
    names.remove(curbest)

    for i in df[curbest].unique(): #high medium low
        newnode = Node(df[df[curbest] == i])
        n.children.append(newnode)
        decision_tree(newnode.df,newnode,names)
    if curbest not in names:
        names.insert(0,curbest)


def notfound(startnode,dic):
    cur = startnode
    while cur.str != None:
        escape = 1
        for i in cur.children:
            if dic[cur.str] in i.df[cur.str].unique():
                cur = i
                escape = 0
                break
        if escape:
            break
    return cur.df[cur.df.columns[-1]].mode()[0]


def classify(arr, startnode, dic): #arr represents np array
    curnode = startnode
    while len(curnode.children) != 0:
        temp = curnode.df.copy()
        out = 1
        for i in curnode.children:
            if (i.df[i.df.columns[:-1]] == arr).all(1).any(): #check if this is right
                out = 0
                curnode = i
                break
        if out == 1:
            return notfound(startnode, dic)
    mask = (curnode.df[curnode.df.columns[:-1]] == arr).all(1)
    matched = curnode.df[mask]
    result = matched[matched.columns[-1]].value_counts().tolist()
    if (len(result) == 2) and (result[0] == result[1]):
        return 0
    else:
        return matched[matched.columns[-1]].mode()[0]


def go(training_filename, testing_filename):
    """
    Construct a decision tree using the training data and then apply
    it to the testing data.

    Inputs:
      training_filename (string): the name of the file with the
        training data
      testing_filename (string): the name of the file with the testing
        data

    Returns (list of strings or pandas series of strings): result of
      applying the decision tree to the testing data.
    """
    # TODO: implement this method and remove this comment
    answer = []
    df = pd.read_csv(training_filename)
    startnode = Node(df)
    names = list(df.columns)

    decision_tree(df,startnode,names)
    
    df2 = pd.read_csv(testing_filename)
    df2 = df2[df2.columns[:-1]]
    nparr = np.array(df2)

    for i in range(df2.shape[0]):
        if i == 23:
            print(nparr[i])
        answer.append(str(classify(nparr[i],startnode,dict(zip(df2.columns,nparr[i])))))
        
    return answer


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "usage: python3 {} <training filename> <testing filename>".format(
                sys.argv[0]
            )
        )
        sys.exit(1)

    for result in go(sys.argv[1], sys.argv[2]):
        print(result)
