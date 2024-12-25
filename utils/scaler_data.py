import pandas as pd
from sklearn import preprocessing
import numpy as np

class Datascaler:
    def __init__(self, data):
        """
        初始化Datascaler对象
        :param data: 要标准化的数据，假设是一个列表的列表（二维数组）
        """
        self.data = data
        self.scalered_data = []

    def x_scaler(self,data,x_columns):
        """
        自变量标准化
        示例：x_colums=['hours','temperature','humidity','lighting','ultraviolet','SO2','salt_spary']
        """
        df = data
        scaler = preprocessing.MinMaxScaler().fit(df[x_columns])
        final_df_scaler = scaler.transform(df[x_columns])
        print('归一化后的自变量数据形状',final_df_scaler.shape)
        self.scalered_data = final_df_scaler
        return self  # 支持链式调用

    def standard_data(self, data,x_columns,y_columns,decimals_n):
        """
        自变量和标签都进行标准化，且对自变量取近似
        :param x_columns: 用于标准化的自变量列索引列表
        """
        df = data
        # x_columns=['hours','temperature','humidity','lighting','ultraviolet','SO2','salt_spary']
        scaler = preprocessing.MinMaxScaler().fit(df[x_columns])
        final_df_scaler = scaler.transform(df[x_columns])
        # y_columns=['i_corr(mA)']
        normalized_df = pd.DataFrame(final_df_scaler, columns=x_columns)
        standardized_data_rounded = np.around(normalized_df, decimals=decimals_n)
        combined_df = pd.concat([standardized_data_rounded, df[y_columns]], axis=1)
        print('标准化后的前五行数据',combined_df.head())
        self.scalered_data = combined_df
        return self  # 支持链式调用