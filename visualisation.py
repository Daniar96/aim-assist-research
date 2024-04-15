import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def box_plot_scores(data: pd.DataFrame):
    print(data)
    # Filter the data for the categories 'CWO', 'CW', 'MK'
    filtered_data = data[data['category'].isin(['CWO', 'CW', 'MK'])]
    print(filtered_data)

    # Create a boxplot to compare scores
    plt.figure(figsize=(10, 6))
    plt.boxplot([filtered_data[filtered_data['category'] == 'CWO']['score'],
                 filtered_data[filtered_data['category'] == 'CW']['score'],
                 filtered_data[filtered_data['category'] == 'MK']['score']],
                labels=['CWO', 'CW', 'MK'])
    plt.title('Comparison of Scores between Categories CWO, CW, and MK')
    plt.ylabel('Score')
    plt.xlabel('Category')
    plt.grid(True)
    plt.show()
    return


if __name__ == "__main__":
    filename = input("Enter the name of your file (e.g. 'taskData_labeled.csv'): ")
    # filename = 'Jelmer_LABELED.csv'
    data = pd.read_csv(filename)
    box_plot_scores(data)
