import pandas as pd

def preprocess(df, region_df):
    # Filter only Summer Olympics
    df = df[df["Season"] == "Summer"].copy()

    # Merge NOC region data
    df = df.merge(region_df, on="NOC", how="left")

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # One-hot encode medals
    medal_dummies = pd.get_dummies(df["Medal"])
    df = pd.concat([df, medal_dummies], axis=1)

    return df