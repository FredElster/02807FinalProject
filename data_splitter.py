import pandas as pd
from sklearn.model_selection import train_test_split

# Input file
input_file = "merged_with_features.csv"

# Output files
train_file = "train.csv"
test_file = "test.csv"

# Split settings
test_size = 0.2        # 20% test, 80% train
random_state = 42       # for reproducibility

def main():
    # Load the data
    df = pd.read_csv(input_file)

    # Split using sklearn
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    # Save outputs
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    print("Done!")
    print(f"Training rows: {len(train_df)}")
    print(f"Testing rows: {len(test_df)}")

if __name__ == "__main__":
    main()
