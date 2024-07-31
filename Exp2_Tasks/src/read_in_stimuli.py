# to read in all letter stimuli files and save in .py file
# coding=utf-8


import os


def read_txt_files(folder_path, output_script_path):
    with open(output_script_path, 'w') as output_script:
        output_script.write("# Auto-generated Python script with letter contents\n\n")

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".txt"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path)

                    # Extracting relevant components from the relative path
                    components = relative_path.split(os.sep)
                    # print(components)
                    n_back = components[0].split("_")[0]
                    practice_type = components[0].split("_")[-2]
                    run = components[1].split("_")[-1]
                    isi = components[-2].split("_")[-1]
                    trial_n = components[-1].split("_")[-1][:-4]

                    # Constructing variable names based on the specified format
                    if "letter_lists" in components:
                        variable_name = f"letters_{n_back}_back_{practice_type}_Run_{run}_ISI_{isi}_trial_{trial_n}"
                    elif "letter_type_lists" in components:
                        variable_name = f"letters_type_{n_back}_back_{practice_type}_Run_{run}_ISI_{isi}_trial_{trial_n}"
                    else:
                        # Skip files that are not in letter_lists or letter_type_lists
                        continue

                    with open(file_path, 'r') as txt_file:
                        file_content = txt_file.read()
                        contentList = file_content.split(sep='\n')[:-1]

                    # Write the content to the output script
                    output_script.write(f'# Contents of file: {relative_path}\n')
                    output_script.write(f'{variable_name} = {contentList}\n\n\n')


if __name__ == "__main__":
    input_folder = r"E:\Dissertation\Methods\Exp2_Demand_Choice\DARpy\stimuli"
    output_script_path = "letter_stimuli.py"

    read_txt_files(input_folder, output_script_path)
    print(f"Python script generated and saved to {output_script_path}")





