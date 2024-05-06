###############################
#    EEG list shuffle (Daisy)
###############################


'''
print("test!")

import pandas as pd
import random
import os

def shuffle_speakers_within_blocks(input_file):
    # Read the data from the txt file into a DataFrame
    df = pd.read_csv(input_file, sep='\t')

    # Shuffle the orders of speakers within each block while ensuring no more than 2 same speakers in a row
    shuffled_data = []
    for _, group in df.groupby('block'):
        speakers = group['speaker'].tolist()
        while True:
            random.shuffle(speakers)
            valid = True
            for i in range(1, len(speakers)):
                if speakers[i] == speakers[i-1] and speakers[i] == speakers[i-2]:
                    valid = False
                    break
            if valid:
                break
        shuffled_data.extend(speakers)

    # Add the shuffled speakers back to the DataFrame
    df['Shuffled_Speaker'] = shuffled_data

    # Save the shuffled DataFrame to a new txt file
    output_file = input_file.replace('.txt', '_shuffled.txt')
    df.to_csv(output_file, sep='\t', index=False)

    print(f"Shuffled data saved to {output_file}")

# Replace 'input_file.txt' with the path to your input txt file
#input_file = '317-list_init.txt'
#shuffle_speakers_within_blocks(input_file)

# Directory containing input files
input_directory = 'txtlist/'

# List all files in the input directory
input_files = [file for file in os.listdir(input_directory) if file.endswith('.txt')]

# Loop through each input file and shuffle speakers
for input_file in input_files:
    input_file_path = os.path.join(input_directory, input_file)
    shuffle_speakers_within_blocks(input_file_path)

    


#----------------------------------------------------------------------------

import pandas as pd
import random
import os

def shuffle_speakers_within_block(file_path):
    # Read the data from the txt file into a pandas DataFrame
    df = pd.read_csv(file_path, sep='\t')
    
    # Create a dictionary to store shuffled sequences for each block
    shuffled_sequences = {}
    
    # Iterate over each block
    for block, block_df in df.groupby('block'):
        # Initialize a list to store the shuffled rows
        shuffled_rows = []
        
        # Iterate over each row in the block
        for index, row in block_df.iterrows():
            # Get the current speaker
            current_speaker = row['speaker']
            
            # Initialize a list to store potential next speakers
            next_speakers = [s for s in ['s1', 's2', 's3', 's4'] if s != current_speaker]
            
            # Shuffle the next speakers
            random.shuffle(next_speakers)
            
            # Iterate over the shuffled next speakers
            for next_speaker in next_speakers:
                # Check if adding this speaker would violate the constraint
                if len(shuffled_rows) >= 2 and shuffled_rows[-1]['speaker'] == next_speaker and shuffled_rows[-2]['speaker'] == next_speaker:
                    continue
                
                # Add the row with the shuffled speaker to the shuffled rows list
                shuffled_rows.append(row)
                row['speaker'] = next_speaker
                
                # Break out of the loop since we found a valid next speaker
                break
        
        # Add the shuffled rows to the dictionary
        shuffled_sequences[block] = shuffled_rows
    
    # Concatenate the shuffled sequences into a single DataFrame
    shuffled_df = pd.concat(shuffled_sequences.values(), ignore_index=True)
    
    return shuffled_df

'''
#-------------------------------------------------------------
import pandas as pd
import os
import random

# Step 1: Import text file
input_file = "input.txt"  # Change this to your input file name

# Check if the file exists
if not os.path.exists(input_file):
    print("Input file not found.")
    exit()

# Read the input file into a pandas DataFrame
df = pd.read_csv(input_file, sep="\t")

# Step 2: Randomly shuffle rows within each block
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

# Step 3: Output to tab-delimited txt file
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "shuffled_output.txt")
output_df.to_csv(output_file, sep="\t", index=False)
print(f"Output saved to {output_file}")



#this works-- just need to change this to loop through all the files