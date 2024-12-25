
class DataCleaner:
    def __init__(self, data):
        """
        初始化DataCleaner对象
        :param data: 要清洗的原始数据，假设是一个列表的列表（二维数组）
        """
        self.data = data
        self.cleaned_data = []

    def remove_empty_rows(self):
        """
        移除空行
        """
        self.cleaned_data = [row for row in self.data if row]
        return self  # 支持链式调用

    def remove_duplicates(self, key_columns):
        """
        移除重复行，基于指定的列
        :param key_columns: 用于判断重复的关键列索引列表
        """
        seen = set()
        unique_data = []
        for row in self.cleaned_data:
            key = tuple(row[i] for i in key_columns)
            if key not in seen:
                unique_data.append(row)
                seen.add(key)
        self.cleaned_data = unique_data
        return self  # 支持链式调用

    def fill_missing_values(self, fill_value):
        """
        填充缺失值
        :param fill_value: 用于填充缺失值的值
        """
        self.cleaned_data = [[fill_value if x is None else x for x in row] for row in self.cleaned_data]
        return self  # 支持链式调用

    def convert_to_numeric(self, columns):
        """
        将指定列转换为数值类型
        :param columns: 要转换的列索引列表
        """
        try:
            self.cleaned_data = [
                [float(row[i]) if i in columns else row[i] for i in range(len(row))]
                for row in self.cleaned_data
            ]
        except ValueError as e:
            print(f"Error converting to numeric: {e}")
            # 可以选择抛出异常、记录日志或忽略错误
        return self  # 支持链式调用

    def get_cleaned_data(self):
        """
        获取清洗后的数据
        """
        return self.cleaned_data

# 使用示例
raw_data = [
    [1, 'Alice', None, 'New York'],
    [2, 'Bob', 30, 'Los Angeles'],
    [3, 'Alice', 25, 'New York'],  # 重复行
    [],  # 空行
    [4, 'Charlie', '28', 'Chicago']  # 非数值数据
]

cleaner = DataCleaner(raw_data)
cleaned_data = cleaner.remove_empty_rows() \
                      .remove_duplicates([0, 1, 2]) \
                      .fill_missing_values('N/A') \
                      .convert_to_numeric([2]) \
                      .get_cleaned_data()

for row in cleaned_data:
    print(row)