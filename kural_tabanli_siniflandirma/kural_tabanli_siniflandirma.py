import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# region Information about persona.csv:

# Persona.csv Variables:
# --------------------------------
# Price: Customer Spend Amount
# Source: Customer Device Type
# Sex: Customer Sex
# Country: Customer Country
# Age: Customer Age

# endregion

df = pd.read_csv("persona.csv")


def overview_df(dataframe):
    """
    An overview of the dataframe

    Parameters
    ----------
    dataframe: DataFrame
        Name of the dataframe

    """
    print(f"------------------------------------ OVERVIEW ------------------------------------")
    print(f"------------------------------------")
    print(f"Number of Records     --> {dataframe.shape[0]}")
    print(f"Number of Variables   --> {dataframe.shape[1]}")
    print(f"Name of The Variables --> {dataframe.columns}")
    print(f"------------------------------------")
    print(f"Variable Types:  \n{dataframe.dtypes}")
    print(f"------------------------------------")
    print(f"First 5 Record:  \n{dataframe.head()}")
    print(f"------------------------------------")
    print(f"Last 5 Record:   \n{dataframe.tail()}")
    print(f"------------------------------------")
    print(f"Number of NaN:   \n{dataframe.isnull().sum()}")
    print(f"------------------------------------")


overview_df(df)


def get_cols(dataframe, cat_th=10):
    """
    Select categorical and numerical variables within the dataframe that has been given

    Parameters
    ----------
    dataframe: dataframe
        Name of the dataframe
    cat_th: int, float
        threshold of the number of classes in numerical variables

    Returns
    -------
    cat_cols: list
        Categorical Variables
    num_cols: list
        Numerical Variables

    """
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int64", "float64", "int32", "float32"]]
    cat_cols = cat_cols + num_but_cat

    num_cols = [col for col in df.columns if df[col].dtypes in ["int64", "float64", "int32", "float32"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Categorical Variables: {len(cat_cols)}")
    print(f"Numerical Variables  : {len(num_cols)}")

    return cat_cols, num_cols


categorical_variables, numerical_variables = get_cols(df, 5)


def overview_cat_col(dataframe, col_name):
    """
    An overview of categorical variables

    Parameters
    ----------
    dataframe
    col_name

    """
    print(f"{col_name} Summary:")
    print("-------------------")
    print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
                        "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))


for cat_col in categorical_variables:
    overview_cat_col(df, cat_col)
    print("-------------------------------------")


def overview_num_col(dataframe, col_name, plot=False):
    """
    An overviwe of numerical variables

    Parameters
    ----------
    dataframe
    col_name: str
        Variable name
    plot: bool
        True gives histogram graph

    """
    print(f"{col_name} Summary:")
    print("-------------------")
    print(f"Count --> {dataframe[col_name].describe()[0]}")
    print(f"Mean  --> {dataframe[col_name].describe()[1]}")
    print(f"Std   --> {dataframe[col_name].describe()[2]}")
    print(f"Min   --> {dataframe[col_name].describe()[3]}")
    print(f"Max   --> {dataframe[col_name].describe()[7]}")
    if plot:
        dataframe[col_name].hist()
        plt.xlabel(col_name)
        plt.title(col_name)
        plt.show(block=True)


for num_col in numerical_variables:
    overview_num_col(df, num_col, plot=True)
    print("-------------------------------------")

# Use groupby to see average PRICE for other variables.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})

# Sort dataframe in a descending order by PRICE.
agg_df.sort_values(by="PRICE", ascending=False, inplace=True)
agg_df.reset_index(inplace=True)

# Create a new categorical varible using AGE variable.
cut_bins = [0, 16, 22, 30, 40, agg_df["AGE"].max()]
cut_labels = ["0_16", "17_22", "23_30", "31_40", "41_" + str(agg_df["AGE"].max())]
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], cut_bins, labels=cut_labels)
agg_df["AGE_CAT"].unique()
str(agg_df["AGE_CAT"].dtype)

# Create one variable that has all the info you need and get rid of the other ones.
agg_df["customers_level_based"] = ["_".join(val).upper() for val in agg_df[["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]].values]
agg_df = agg_df[["customers_level_based", "PRICE"]]

# I ignored AGE and use AGE_CAT instead. By doing this I aggregated different records under one name.
# I should use groupby and get PRICE averages instead.
agg_df["customers_level_based"].value_counts()
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.reset_index(inplace=True)

# Define a new variable named "SEGMENT" and segmentize customers based on their value.
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 5, labels=["low", "low-mid", "mid", "high-mid", "high"])
agg_df.groupby("SEGMENT").agg({"PRICE": ["mean", "min", "max", "sum"]})


# Get customer information from user and check new customers' segmentation.
def get_new_customer():
    """
    Create a new entry

    Returns
    -------
    new_customer: str

    """
    while True:
        entry = int(input("Will there be a new entry? 1:YES | 0:NO"))
        if entry == 1:
            print("Country Codes: bra | can | tur | fra | usa | deu")
            country_in = input("Enter Country Code -->")
            print("Source : android | ios")
            source_in = input("Enter Source -->")
            print("Sex: male | female")
            sex_in = input("Enter Sex -->")
            print("Age: a number between 0 and 66")
            age_in = int(input("Enter Age -->"))
            if 0 <= age_in <= 66:
                age_cat_in = ""
                if 0 <= age_in <= 16:
                    age_cat_in += "0_16"
                elif 17 <= age_in <= 22:
                    age_cat_in += "17_22"
                elif 23 <= age_in <= 30:
                    age_cat_in += "23_30"
                elif 31 <= age_in <= 40:
                    age_cat_in += "31_40"
                else:
                    age_cat_in += "41_66"
                new_customer = str(country_in) + "_" + str(source_in) + "_" + str(sex_in) + "_" + str(age_cat_in)
                new_customer = new_customer.upper()
                return new_customer
            else:
                print("Wrong entry. Keep your inputs inside pre-selected items.")
        else:
            print("Good-bye.")
            break


def show_new_customer():
    print("------------------ NEW CUSTOMER INFO ------------------")
    print(agg_df[agg_df["customers_level_based"] == get_new_customer()])


show_new_customer()
