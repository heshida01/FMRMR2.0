#!/usr/bin/env python3
# -*- coding=utf-8 -*-

### 消除警告
def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from feature_Rank import feature_rank
import argparse
import sklearn.metrics
import time
import logging
import os
from scipy.io import arff
from sklearn.datasets import load_svmlight_file
from sklearn.datasets import dump_svmlight_file
from format import pandas2arff
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from math import ceil
from sklearn.preprocessing import LabelBinarizer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=int, help="start index", default=1)
    parser.add_argument("-i", type=str, help="input file", required=True)
    parser.add_argument("-e", type=int, help="end index", default=-1)
    parser.add_argument("-l", type=int, help="step length", default=1)
    parser.add_argument("-m", type=int, help="mrmd2.0 features top n", default=-1)
    parser.add_argument("-t", type=str, help="metric basline", default="f1")
    parser.add_argument("-o", type=str, help="output the metrics file", default=None)
    parser.add_argument("-c", type=str, help="output the dimensionality reduction file")

    args = parser.parse_args()

    return args


class Dim_Rd(object):

    def __init__(self, file_csv, logger):
        self.file_csv = file_csv
        self.logger = logger

    def read_data(self):  # default csv

        def read_csv():
            self.df = pd.read_csv(self.file_csv, engine='python').dropna(axis=1)
            datas = np.array(self.df)
            self.datas = datas
            self.X = datas[:, 1:]
            self.y = datas[:, 0]

        file_type = self.file_csv.split('.')[-1]
        if file_type == 'csv':
            read_csv()

    def range_steplen(self, start=1, end=1, length=1):
        self.start = start
        self.end = end
        self.length = length

    def Randomforest(self, X, y):
        clf = RandomForestClassifier(random_state=1, n_estimators=100)
        # cv_results=cross_validate(clf,X,y,return_train_score=False,cv=10,n_jobs=-1)

        ypred = sklearn.model_selection.cross_val_predict(clf, X, y, n_jobs=-1, cv=5)
        f1 = sklearn.metrics.f1_score(y, ypred, average='weighted')
        precision = sklearn.metrics.precision_score(self.y, ypred, average='weighted')
        recall = sklearn.metrics.recall_score(self.y, ypred, average='weighted')
        acc = sklearn.metrics.accuracy_score(self.y, ypred)
        lb = LabelBinarizer()
        lb.fit(self.y)

        y = lb.transform(self.y)
        ypred = lb.transform(ypred)
        auc = sklearn.metrics.roc_auc_score(y, ypred)

       

        return acc, f1, precision, recall, auc, ypred

    def Result(self, seqmax, clf, features, csvfile):
        ypred = sklearn.model_selection.cross_val_predict(clf, self.X[:, seqmax], self.y, n_jobs=-1, cv=5)
        # print(ypred)
        # confusion_matrix = sklearn.metrics.confusion_matrix(self.y,ypred,)
        #
        # TP = confusion_matrix[1, 1]
        # TN = confusion_matrix[0, 0]
        # FP = confusion_matrix[0, 1]
        # FN = confusion_matrix[1, 0]
        # logger.info('***confusion matrix***')
        #
        # s1 = '{:<15}'.format('')
        # #f.write(s1)
        # s2 = '{:<15}'.format('pos_class')
        # #f.write(s2)
        # s3 = '{:<15}'.format('neg_class')
        # #f.write(s3 )
        # logger.info(s1+s2+s3)
        #
        # s1 = '{:<15}'.format('pos_class')
        # #f.write(s1)
        # s2 = 'TP:{:<15}'.format(TP)
        # #f.write(s2)
        # s3 = 'FN:{:<15}'.format(FN)
        # #f.write(s3)
        # logger.info(s1 + s2 + s3)
        #
        # s1 = '{:<15}'.format('neg_class')
        # #f.write(s1)
        # s2 = 'FP:{:<15}'.format(FP)
        # #f.write(s2)
        # s3 = 'TN:{:<15}'.format(TN)
        # #f.write(s3)
        # logger.info(s1+s2+s3)
        f1 = sklearn.metrics.f1_score(self.y, ypred, average='weighted')
        # f.write('f1 ={}\n '.format(f1))
        logger.info(('f1 ={:0.4f} '.format(f1)))
        acc = sklearn.metrics.accuracy_score(self.y, ypred, )
        logger.info('accuarcy = {:0.4f} '.format(acc))
        # f.write('accuarcy = {:} \n'.format(acc))
        precision = sklearn.metrics.precision_score(self.y, ypred, average='weighted')
        logger.info('precision ={:0.4f} '.format(precision))
        # f.write('precision ={} \n'.format(precision))
        recall = sklearn.metrics.recall_score(self.y, ypred, average='weighted')
        logger.info(('recall ={:0.4f}'.format(recall)))
        # f.write('recall ={}\n '.format(recall))

        lb = LabelBinarizer()
        y = lb.fit_transform(self.y)
        ypred = lb.transform(ypred)
        auc = sklearn.metrics.roc_auc_score(y, ypred)
        # f.write('roc area = {}\n'.format(roc))
        logger.info('auc = {:0.4f}'.format(auc))

        columns_index = [0]
        columns_index.extend([i + 1 for i in seqmax])
        data = np.concatenate((self.y.reshape(len(self.y), 1), self.X[:, seqmax]), axis=1)
        features_list = (self.df.columns.values)

        ###实现-m参数
        if args.m == -1:
            pass
        else:
            columns_index = columns_index[0:args.m + 1]
            data = data[:, 0:args.m + 1]
        df = pd.DataFrame(data, columns=features_list[columns_index])
        df.iloc[0, :].astype(int)
        df.to_csv(csvfile, index=None)

    def Dim_reduction(self, features, features_sorted, outfile, csvfile):
        logger.info("Start dimension reduction ...")
        features_number = []
        for value in features_sorted:
            features_number.append(features[value[0]] - 1)
        stepSum = 0
        max = 0
        seqmax = []
        predmax = []
        scorecsv = outfile

        with open(scorecsv, 'w') as f:
            f.write('length,accuracy,f1,precision,recall,roc\n')
            for i in range(int(ceil((self.end - self.start) / self.length)) + 1):
                if (stepSum + self.start) < self.end:
                    n = stepSum + self.start
                else:
                    n = self.end

                stepSum += self.length

                ix = features_number[self.start - 1:n]
                acc, f1, precision, recall, auc, ypred = self.Randomforest(self.X[:, ix], self.y)

                if args.t == "f1":
                    benchmark = f1
                elif args.t == "acc":
                    benchmark = acc
                elif args.t == "precision":
                    benchmark = precision
                elif args.t == "recall":
                    benchmark = recall
                elif args.t == "auc":
                    benchmark = auc

                if benchmark > max:
                    max = benchmark
                    seqmax = ix

                logger.info(
                    'length={} f1={:0.4f} accuarcy={:0.4f} precision={:0.4f} recall={:0.4f} auc={:0.4f} '.format(
                        len(ix), f1, acc, precision, recall, auc))
                f.write('{},{:0.4f},{:0.4f},{:0.4f},{:0.4f},{:0.4f}\n'.format(len(ix), acc, f1, precision, recall, auc))

        logger.info('----------')
        logger.info('the max {} = {:0.4f}'.format(args.t, max))

        index_add1 = [x + 1 for x in seqmax]
        logger.info('{},length = {}'.format(self.df.columns.values[index_add1], len(seqmax)))
        logger.info('-----------')
        clf = RandomForestClassifier(random_state=1, n_estimators=100)
        self.Result(seqmax, clf, features, csvfile)
        logger.info('-----------')

    def run(self, inputfile):

        args = parse_args()
        file = inputfile

        outputfile = args_o
        #csvfile = args.c
        csvfile = os.getcwd() + os.sep + 'Results' + os.sep + os.path.basename(args.c)
        mrmr_featurLen = args.m
        features, features_sorted = feature_rank(file, self.logger, mrmr_featurLen)
        self.read_data()
        if int(args.e) == -1:
            args.e = len(pd.read_csv(file, engine='python').columns) - 1
        self.range_steplen(args.s, args.e, args.l)
        outputfile = outputfile
        csvfile = csvfile
        self.Dim_reduction(features, features_sorted, outputfile, csvfile)


def arff2csv(file):
    data = arff.loadarff(file)
    df = pd.DataFrame(data[0])
    df['class'] = df['class'].map(lambda x: x.decode())

    # eg: 0  1    2     3     4  mean =>>  mean   0     1     2    3    4 in dataframe
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    file_csv = file + '.csv'
    df.to_csv(file_csv, index=None)
    return file_csv


def libsvm2csv(file):
    data = load_svmlight_file(file)
    df = pd.DataFrame(data[0].todense())
    df['class'] = pd.Series(np.array(data[1])).astype(int)

    # eg: 0  1    2     3     4  mean =>>  mean   0     1     2    3    4 in dataframe
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    file_csv = file + '.csv'
    df.to_csv(file_csv, index=None)

    return file_csv


def tsne_scatter(file):
    df = pd.read_csv(file, engine='python')
    tsne = TSNE()

    label_name = df.columns.values[0]
    fea_data = df.drop(columns=[label_name])  # 取出所有特征向量用于降维
    redu_fea = tsne.fit_transform(fea_data)  # 将数据降到2维进行后期的可视化处理
    labels = df.iloc[:, 0]
    redu_data = np.vstack((redu_fea.T, labels.T)).T  # 将特征向量和正反例标签整合
    tsne_df = pd.DataFrame(
        data=redu_data, columns=['Dimension1', 'Dimension2', "label"])

    scaler = MinMaxScaler()
    tsne_df[['Dimension1', 'Dimension2']] = scaler.fit_transform(tsne_df[['Dimension1', 'Dimension2']])
    p1 = tsne_df[(tsne_df.iloc[:, 2] == 1)]
    p2 = tsne_df[(tsne_df.iloc[:, 2] == 0)]
    x1 = p1.values[:, 0]
    y1 = p1.values[:, 1]
    x2 = p2.values[:, 0]
    y2 = p2.values[:, 1]

    # 绘制散点图
    plt.plot(x1, y1, 'o', color="#3dbde2", label='positive', markersize='1')
    plt.plot(x2, y2, 'o', color="#b41f87", label='negative', markersize='1')
    plt.xlabel('Dimension1', fontsize=9)
    plt.ylabel('Dimension2', fontsize=9)

    plt.legend(loc="upper right", fontsize="x-small")

def main(args_i,args_s=1,args_e=-1,args_l=1,args_m=-1,args_t='f1',args_c='',args_o_=''):




    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_path = os.getcwd() + os.sep + 'Logs' + os.sep
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # logging.basicConfig(level=logging.INFO,
    #                     format='[%(asctime)s]: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
    formatter = logging.Formatter('[%(asctime)s]: %(message)s')
    # 文件
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # 控制台
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("---mrmd 2.0 start----")

    args = parse_args()

    args.i, args.s,args.e,args.l,args.m,args.t,args.c,args.o = \
        args_i, args_s , args_e , args_l , args_m , args_t , args_c , args_o_





    file = args.i
    file_type = file.split('.')[-1]
    if file_type == 'csv':
        pass
    elif file_type == 'arff':
        file = arff2csv(file)
    elif file_type == 'libsvm':

        file = libsvm2csv(file)
    else:
        assert "format error"
    # format : arff or libsvm to csv
    plt.figure(figsize=(2 * 4.7, 1 * 4.7))
    plt.subplot(1, 2, 1)
    tsne_scatter(file)

    if int(args.e) == -1:
        args.e = len(pd.read_csv(file, engine='python').columns) - 1

    global args_o
    if args.o == None:
        args.o = ''.join(args.i.split('.')[:-1]) + '.metrics.csv'
    args_o = args.o

    d = Dim_Rd(file, logger)
    d.run(inputfile=file)
    outputfile = os.getcwd() + os.sep + 'Results' + os.sep + os.path.basename(args_o)
    csvfile = os.getcwd() + os.sep + 'Results' + os.sep + os.path.basename(args.c)
    logger.info("The output by the terminal's log has been saved in the {}.".format(logfile))
    logger.info('metrics have been saved in the {}.'.format(outputfile))

    plt.subplot(1, 2, 2)
    tsne_scatter(csvfile)

    pngpath = os.path.abspath('./Results') + os.sep + os.path.basename(args.i) + '.png'
    plt.savefig(pngpath)
    logger.info('Scatter charts visualized by t-SNE dataset has been saved in the {}.'.format(pngpath))

    # 处理输出文件的类型
    outputfile_file_type = args.c.split('.')[-1]
    if outputfile_file_type == 'csv':
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    elif outputfile_file_type == 'arff':
        df = pd.read_csv(csvfile, engine='python')
        filename, ext = os.path.splitext(args.i)

        if df['class'].dtype == np.float:
            df['class'] = df['class'].astype(int)
        temp = df['class']
        df = df.drop(columns=['class'], axis=1)
        df['class'] = temp
        DimensionReduction_filename = os.path.abspath('./Results') + os.sep + args.c
        pandas2arff.pandas2arff(df, filename=r'./Results/{}'.format(args.c), wekaname=filename,
                                cleanstringdata=False,
                                cleannan=True)

        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(DimensionReduction_filename))
        # clean_csv(csvfile)

    elif outputfile_file_type == 'libsvm':
        df = pd.read_csv(csvfile, engine='python')
        for x in df.columns:
            if x.lower() == 'class':
                label = x
                break
        y = df[label]
        X = df.drop(columns=label, axis=1)

        inputfile = args.i
        # filename ,ext = os.path.splitext(inputfile)
        DimensionReduction_filename = os.path.abspath('./Results') + os.sep + args.c
        dump_svmlight_file(X, y, DimensionReduction_filename, zero_based=True, multilabel=False)
        # clean_tmpfile.clean_csv(csvfile)
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(DimensionReduction_filename))
    else:
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    logger.info("---mrmd 2.0 end---")


if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_path = os.getcwd() + os.sep + 'Logs' + os.sep
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = log_path + rq + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # logging.basicConfig(level=logging.INFO,
    #                     format='[%(asctime)s]: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置
    formatter = logging.Formatter('[%(asctime)s]: %(message)s')
    # 文件
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # 控制台
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("---mrmd 2.0 start----")

    args = parse_args()
    file = args.i
    file_type = file.split('.')[-1]
    if file_type == 'csv':
        pass
    elif file_type == 'arff':
        file = arff2csv(file)
    elif file_type == 'libsvm':

        file = libsvm2csv(file)
    else:
        assert "format error"
    # format : arff or libsvm to csv
    plt.figure(figsize=(2 * 4.7, 1 * 4.7))
    plt.subplot(1, 2, 1)
    tsne_scatter(file)

    if int(args.e) == -1:
        args.e = len(pd.read_csv(file, engine='python').columns) - 1

    global args_o
    if args.o == None:
        args.o = ''.join(args.i.split('.')[:-1]) + '.metrics.csv'
    args_o = args.o

    d = Dim_Rd(file, logger)
    d.run(inputfile=file)
    outputfile = os.getcwd() + os.sep + 'Results' + os.sep + os.path.basename(args_o)
    csvfile = os.getcwd() + os.sep + 'Results' + os.sep + os.path.basename(args.c)
    logger.info("The output by the terminal's log has been saved in the {}.".format(logfile))
    logger.info('metrics have been saved in the {}.'.format(outputfile))

    plt.subplot(1, 2, 2)
    tsne_scatter(csvfile)

    pngpath = os.path.abspath('./Results') + os.sep + os.path.basename(args.i) + '.png'
    plt.savefig(pngpath)
    logger.info('Scatter charts visualized by t-SNE dataset has been saved in the {}.'.format(pngpath))

    # 处理输出文件的类型
    outputfile_file_type = args.c.split('.')[-1]
    if outputfile_file_type == 'csv':
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    elif outputfile_file_type == 'arff':
        df = pd.read_csv(csvfile, engine='python')
        filename, ext = os.path.splitext(args.i)

        if df['class'].dtype == np.float:
            df['class'] = df['class'].astype(int)
        temp = df['class']
        df = df.drop(columns=['class'], axis=1)
        df['class'] = temp
        DimensionReduction_filename = os.path.abspath('./Results') + os.sep + args.c
        pandas2arff.pandas2arff(df, filename=r'./Results/{}'.format(args.c), wekaname=filename, cleanstringdata=False,
                                cleannan=True)

        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(DimensionReduction_filename))
        # clean_csv(csvfile)

    elif outputfile_file_type == 'libsvm':
        df = pd.read_csv(csvfile, engine='python')
        for x in df.columns:
            if x.lower() == 'class':
                label = x
                break
        y = df[label]
        X = df.drop(columns=label, axis=1)

        inputfile = args.i
        # filename ,ext = os.path.splitext(inputfile)
        DimensionReduction_filename = os.path.abspath('./Results') + os.sep + args.c
        dump_svmlight_file(X, y, DimensionReduction_filename, zero_based=True, multilabel=False)
        # clean_tmpfile.clean_csv(csvfile)
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(DimensionReduction_filename))
    else:
        logger.info('Reduced dimensional dataset has been saved in the {}.'.format(csvfile))

    logger.info("---mrmd 2.0 end---")
