"""

Creates encoded labels for data and splits dataset in train, val, and test data.

"""


from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle


def create_labels(df):
    """[summary]

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Create label encoding for dataset; OneHotEncoder() can't take in strings so 
    # first do integer encoding then convert integer encoding into one-hot encoding
    le, ohe = LabelEncoder(), OneHotEncoder(sparse=False)
    df["int_label"] = le.fit_transform(df["subreddit_name"])
    df["onehot_label"] = ohe.fit_transform(np.array(df["int_label"]).reshape(-1,1)).tolist()

    return df, le


def split_stratified_into_train_val_test(df_input, stratify_colname='y',
                                         frac_train=0.6, frac_val=0.15, frac_test=0.25,
                                         random_state=None):
    '''
    Splits a Pandas dataframe into three subsets (train, val, and test)
    following fractional ratios provided by the user, where each subset is
    stratified by the values in a specific column (that is, each subset has
    the same relative frequency of the values in the column). It performs this
    splitting by running train_test_split() twice.

    Source: https://stackoverflow.com/questions/50781562/stratified-splitting-of-pandas-dataframe-into-training-validation-and-test-set

    Parameters
    ----------
    df_input : Pandas dataframe
        Input dataframe to be split.
    stratify_colname : str
        The name of the column that will be used for stratification. Usually
        this column would be for the label.
    frac_train : float
    frac_val   : float
    frac_test  : float
        The ratios with which the dataframe will be split into train, val, and
        test data. The values should be expressed as float fractions and should
        sum to 1.0.
    random_state : int, None, or RandomStateInstance
        Value to be passed to train_test_split().

    Returns
    -------
    df_train, df_val, df_test :
        Dataframes containing the three splits.
    '''

    if frac_train + frac_val + frac_test != 1.0:
        raise ValueError('fractions %f, %f, %f do not add up to 1.0' % \
                         (frac_train, frac_val, frac_test))

    if stratify_colname not in df_input.columns:
        raise ValueError('%s is not a column in the dataframe' % (stratify_colname))

    X = df_input # Contains all columns.
    y = df_input[[stratify_colname]] # Dataframe of just the column on which to stratify.

    # Split original dataframe into train and temp dataframes.
    df_train, df_temp, y_train, y_temp = train_test_split(X,
                                                          y,
                                                          stratify=y,
                                                          test_size=(1.0 - frac_train),
                                                          random_state=random_state, 
                                                          shuffle=True)

    # Split the temp dataframe into val and test dataframes.
    relative_frac_test = frac_test / (frac_val + frac_test)
    df_val, df_test, y_val, y_test = train_test_split(df_temp,
                                                      y_temp,
                                                      stratify=y_temp,
                                                      test_size=relative_frac_test,
                                                      random_state=random_state, 
                                                      shuffle=True)

    assert len(df_input) == len(df_train) + len(df_val) + len(df_test)

    return df_train, df_val, df_test



def main():
    """[summary]
    """
    
    # Read in dataframe containing data
    df = pd.read_csv(data_filepath)

    # Create labels for data
    df, le = create_labels(df)

    # Save label_encoder (to be used during testing later)
    pickle.dump(le, open(f"../../data/interim/image_label_encoder.pickle", "wb"))

    # Split dataset into train, val, and test data
    df_train, df_val, df_test = split_stratified_into_train_val_test(df, 
                                    stratify_colname="subreddit_name", 
                                    frac_train=0.8, 
                                    frac_val=0.1, 
                                    frac_test=0.1, 
                                    random_state=seed)
    
    # Output prepared data
    df.to_csv("../../data/interim/df.csv")
    df_train.to_csv("../../data/interim/train_df.csv")
    df_val.to_csv("../../data/interim/val_df.csv")
    df_test.to_csv("../../data/interim/test_df.csv")


if __name__ == "__main__":

    # Specify parameters
    seed = 2021
    data_filepath = "../../data/raw/all-reddit-data.csv"

    main()