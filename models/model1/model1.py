# 超参数最优搜索
# 使用随机搜索确定最佳参数
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from scipy.stats import randint, uniform
import pandas as pd
from utils.scaler_data import  Datascaler
import pickle

class Model_bst:
    # def __init__()
        # self.data = data
        # self.model = self.get_best_model(self,data,label)
        
    def get_best_model(self,data, label):
        X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=42)

        # 定义参数网格
        param_dist = {
            'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2],  # 使用列表简化，虽然这不是真正的随机搜索
            'max_depth': randint(3, 10),
            'min_child_weight': randint(1, 10),
            'subsample': [0.6, 0.8, 1.0],  # 这些也可以是连续分布，比如uniform，但为了简化使用列表
            'colsample_bytree': [0.6, 0.8, 1.0],
            'n_estimators': randint(50, 300)
        }
        print("正在进行最优搜索请勿关闭..... ")
        # 定义XGBRegressor
        xgb_reg = xgb.XGBRegressor(n_estimators=100, random_state=42)

        # 使用RandomizedSearchCV进行随机搜索
        random_search = RandomizedSearchCV(xgb_reg, param_distributions=param_dist, n_iter=100,
                                           cv=5, scoring='r2',
                                           random_state=42)
        # 拟合模型
        random_search.fit(X_train, y_train)

        # 输出最佳参数和最佳分数
        print("Best parameters found: ", random_search.best_params_)
        print("Best cross-validation score: ", random_search.best_score_)  # 注意取负值

        # 使用最佳参数进行预测
        bst = random_search.best_estimator_

        self.model = bst  # 训练好的模型进行存储
        return self.model
    
    # def predict(self, X):
    #     # 使用训练好的模型进行预测
    #     return self.model.predict(X)

    # def score(self, X, y):
    #     # 评估模型的性能
    #     # 这里使用R^2分数作为示例
    #     from sklearn.metrics import r2_score
    #     y_pred = self.predict(X)
    #     return r2_score(y, y_pred)

# 利用数据进行训练和寻优，返回最优模型进行打包

# dataset = pd.read_excel('.../data/processed/交互作用分析-删24h-电流.xlsx')
dataset = pd.read_excel('L:/data/2024/10code/ML_Analysis/data/processed/交互作用分析-删24h-电流.xlsx')
# print(dataset.shape)
# # 打印前5行
# print(dataset.head(5))
x_columns=['hours','temperature','humidity','lighting','ultraviolet','SO2','salt_spary']
y_columns=['i_corr(mA)']
# data = Datascaler(dataset)
data = Datascaler.standard_data(dataset,data=dataset,x_columns=x_columns,y_columns=y_columns,decimals_n=3)
# print('ok')

# 进行寻优脚本
model = Model_bst.get_best_model(Model_bst,data=data.iloc[:,:-1],label=data.iloc[:,-1])

# 打包模型
# 使用pickle将模型序列化并保存到文件
with open('model1_xgb.pkl', 'wb') as f:
    pickle.dump(model, f)
print('xgb模型已经打包至model1_xgb.pkl，可随时调用')