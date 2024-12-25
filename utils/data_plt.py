import pandas as pd
import numpy as np
from .scaler_data import Datascaler
import shap
import pickle
 
# 使用pickle从文件中加载模型
with open('L:/data/2024/10code/model1_xgb.pkl', 'rb') as f:
    bst = pickle.load(f)
dataset = pd.read_excel('L:/data/2024/10code/ML_Analysis/data/processed/交互作用分析-删24h-电流.xlsx')
x_columns=['hours','temperature','humidity','lighting','ultraviolet','SO2','salt_spary']
y_columns=['i_corr(mA)']
data = Datascaler.standard_data(dataset,data=dataset,x_columns=x_columns,y_columns=y_columns,decimals_n=3)
data_default = np.array(data)

class Viewplot:
    def __init__(self):
        pass
    
    def pre_real_data(ratio:float=0.7,data:np.array=None):
        '''
        获取真实值和预测值的值，来绘制对角散点图
        ratio:划分训练和测试的比例，大小为0-1之间,默认0.7
        data:空为默认数据集
        
        返回：
        根据划分比例确定的五个数组
        X_train,y_train,x_test,y_test,y_predict
        '''
        if data == None:
            a = data_default[:,:-1]
            b = data_default[:,-1]
            train_test_split = int(ratio * len(data_default))
        else:
            a = data[:,:-1]
            b = data[:,-1]
            train_test_split = int(ratio * len(data))

        X_train= a[0: train_test_split]
        y_train = b[0: train_test_split]
        x_test = a[train_test_split: ]
        y_test = b[train_test_split: ]
        y_predict = bst.predict(x_test)
        print(f"X_train.shape: {X_train.shape}, y_train.shape: {y_train.shape},x_test.shape: {x_test.shape}, y_test.shape: {y_test.shape},y_predict.shape:{y_predict.shape}")
        return X_train,y_train,x_test,y_test,y_predict
    
    def shap_aver_value(data:np.array=None):
        '''
        获取SHAP计算的重要性均值
        ratio:划分训练和测试的比例，大小为0-1之间,默认0.7
        data:建议使用归一化的数据集np数组，包含自变量名称和因变量。空的话，使用默认数据集
        
        返回：
        返回影响因素的名字和对应数值两个数组
        feature_names,Mean_values
        '''
        if data == None:
            a = data_default[:,:-1]
            b = data_default[:,-1]
        else:
            a = data[:,:-1]
            b = data[:,-1]
        explainer = shap.TreeExplainer(bst)
        shap_values = explainer.shap_values(a)
        # 获取SHAP值的数组形式（对于回归问题，这通常是一个二维数组，其中每行代表一个样本，每列代表一个特征）
        # 计算每个特征的SHAP值的绝对值的平均值
        mean_abs_shap_values = np.mean(np.abs(shap_values),axis=0)
        
        feature_names = []
        Mean_values = []
        
        # 打印每个特征的mean(|SHAP value|)
        for feature_name, mean_abs_value in zip(x_columns, mean_abs_shap_values):
            feature_names.append(feature_name) 
            Mean_values.append(mean_abs_value)
        print(f"Feature: {feature_names}, Mean(|SHAP value|): {Mean_values}")
        return feature_names,Mean_values

    