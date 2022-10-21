from dash_app.utils.prepared_date import load_dataset_from_hugging_face


class DataSet:

    def __init__(self, name, mapper_values, target_col):
        self.name = name
        self.mapper_values = mapper_values
        self.target_col = target_col
        self.data = load_dataset_from_hugging_face(name, mapper_values, target_col)
