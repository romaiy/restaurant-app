import pandas as pd

def upload_file(file_path):
    if not file_path:
        return

    try:
        menu_df = pd.read_csv(file_path)

        required_columns = {'name', 'price', 'gram', 'description'}
        if not required_columns.issubset(menu_df.columns):
            raise ValueError("Файл должен содержать следующие столбцы: name, price, gram, description")


        dishes = menu_df[['name', 'price', 'gram', 'description']].to_records(index=False)
        dishes = [(row.name, float(row.price), int(row.gram), row.description) for row in dishes]

        return dishes

    except Exception as e:
        print(e)
