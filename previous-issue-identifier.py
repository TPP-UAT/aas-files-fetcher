import os

# Specify the folder path
folder_path = "./my_folder"

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Specify the file path inside the folder
file_path = os.path.join(folder_path, "my_file.txt")

# Create and save a file inside the folder
with open(file_path, "w") as file:
    file.write("This is the content of my file.")

print(f"Folder '{folder_path}' and file '{file_path}' have been created.")
