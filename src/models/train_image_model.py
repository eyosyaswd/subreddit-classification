from custom_dataset import Image_Data_Generator
from tensorflow.keras.applications import efficientnet
from tensorflow.keras.applications.efficientnet import EfficientNetB7
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'    # Ignore tf info messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Ignore tf warning messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'    # Ignore tf warning messages
import pandas as pd
import tensorflow as tf


def main():
    """[summary]
    """

    print("\nLoading in dataset...")

    # Load in csv files containing preprocessed data
    train_df = pd.read_csv(train_filepath)
    val_df = pd.read_csv(val_filepath)

    # Load in image data generators
    train_data_gen = Image_Data_Generator(train_df, batch_size=4)
    val_data_gen = Image_Data_Generator(val_df, batch_size=4)

    print("\nCreating Resnet model...")

    # Create VGG16 model
    efficientnet_model = EfficientNetB7(weights="imagenet")

    # Change last layer from 1000 outputs to num_classes

    print("\nTraining model...")

    print("\nLoading in and saving best weights...")


if __name__ == "__main__":

    # Check to make sure the GPU is being used
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

    # Specify parameters
    seed = 2021
    train_filepath = "../../data/interim/train_df.csv"
    val_filepath = "../../data/interim/val_df.csv"

    # Call main function    
    main()

