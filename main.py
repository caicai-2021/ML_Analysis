import pickle
# from .utils.data_scripts.scaler_data import Datascaler
from utils.data_plt import Viewplot
 
# 导出绘制散点图的数据
X_train,y_train,x_test,y_test,y_predict = Viewplot.pre_real_data()
# 导出重要性排序的数据
feature_names,Mean_values = Viewplot.shap_aver_value()
print('完成')