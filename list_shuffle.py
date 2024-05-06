###############################
#    EEG list shuffle (Daisy)
###############################


import pandas as pd
import os
import random

# Step 1: Get a list of input files in the directory
input_folder = "txtlist" 

# Check if the folder exists
if not os.path.exists(input_folder):
    print("Input folder not found.")
    exit()

# Step 2: Loop through each input file
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)
        
        # Read the input file into a pandas DataFrame
        df = pd.read_csv(input_file, sep="\t")

        # Step 3: Randomly shuffle rows within each block
        output_df = pd.DataFrame(columns=df.columns)  # Initialize an empty DataFrame for the output

        for block in df['block'].unique():
            block_df = df[df['block'] == block].copy()  # Extract rows for the current block
            shuffled_rows = []

            # Shuffle rows within the block ensuring no more than 2 same speakers in a row
            while len(block_df) > 0:
                speakers = block_df['speaker'].unique()
                random.shuffle(speakers)

                for speaker in speakers:
                    speaker_rows = block_df[block_df['speaker'] == speaker]
                    if len(shuffled_rows) > 0 and shuffled_rows[-1] == speaker:
                        speaker_rows = speaker_rows.drop(speaker_rows.index[0])
                    if len(speaker_rows) > 0:
                        shuffled_row = speaker_rows.sample(n=1)
                        shuffled_rows.append(shuffled_row['speaker'].values[0])
                        output_df = pd.concat([output_df, shuffled_row])  # Concatenate the shuffled row to the output DataFrame
                        block_df = block_df.drop(shuffled_row.index)

        # Step 4: Output to tab-delimited txt file
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f"shuffled_{filename}")
        output_df.to_csv(output_file, sep="\t", index=False)
        print(f"Output saved to {output_file}")
