import pandas as pd
import ast
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def remove_redundant_data(data: pd.DataFrame()):
    # Only ultimate mode (10)
    data = data[data['mode'].isin([10])]
    # Redundant columns
    columns_to_drop = ['aimlab_map', 'aimlab_version', 'weaponType', 'weaponName', 'workshopId', 'playId',
                       'endedAt', 'hasReplay', 'weaponSkin', 'klutch_id', 'create_date', 'mode']
    data.drop(columns_to_drop, axis=1, inplace=True)

    # Redundant tasks
    tasks_to_keep = ['strafetrack', 'switchtrack', 'gridshot', 'microshot']
    return data[data['taskName'].isin(tasks_to_keep)]


def create_row(row):
    if row['performanceClass'] == "TrackData":
        data = {
            'OTR/acc': row['OTR'],
            'avgTimeOn/rt': row['avgTimeOn'],
            'avgTimeOff/targets': row['maxTimeOn'],
            'maxTimeOn/shots': row['avgTimeOff'],
            'maxTimeOff/kps': row['maxTimeOff'],
            'miss/killTotal': row['missTotal']
        }
    else:
        data = {
            'OTR/acc': row['accTotal'],
            'avgTimeOn/rt': row['rtTotal'],
            'avgTimeOff/targets': row['targetsTotal'],
            'maxTimeOn/shots': row['shotsTotal'],
            'maxTimeOff/kps': row['killsPerSec'],
            'miss/killTotal': row['killTotal']
        }
    data['taskId'] = row['taskId']
    return pd.Series(data)


def normalise_performance(data: pd.DataFrame()):
    # Convert the performance column from string to dict if needed
    data['performance'] = data['performance'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    print(data)
    print(len(data))

    data_expanded = pd.json_normalize(data['performance'])
    data.reset_index(inplace=True)
    data_expanded['taskId'] = data['taskId']
    data_expanded['performanceClass'] = data['performanceClass']
    print(data_expanded)
    print(len(data_expanded))
    data_expanded['missTotal'] = data_expanded[
        ['missUp', 'missUpLeft', 'missUpRight', 'missLeft', 'missRight', 'missDown', 'missDownLeft',
         'missDownRight']].sum(axis=1)
    # An empty DataFrame to collect the normalized 'performance' data
    performance_df = data_expanded.apply(create_row, axis=1)
    performance_df = performance_df[
        ['taskId','OTR/acc', 'avgTimeOn/rt', 'avgTimeOff/targets', 'maxTimeOn/shots', 'maxTimeOff/kps', 'miss/killTotal']]
    # Add performance df to original df
    merged_df = data.merge(performance_df, on='taskId')
    merged_df['participantId'] = None
    merged_df['category'] = None
    merged_df.drop('performance', axis=1, inplace=True)
    return merged_df


if __name__ == "__main__":
    filename = input("Enter the name of your file (e.g. 'taskData.json'): ")
    # filename = "taskData_Daniar2.json"
    df = pd.read_json(filename)
    clear_df = remove_redundant_data(df)
    normalised_df = normalise_performance(clear_df)

    # Remove "json"
    filename = os.path.splitext(filename)[0]
    # Save csv
    normalised_df.to_csv(f"{filename}.csv", index=False)
