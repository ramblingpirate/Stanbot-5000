import os


def save_to_file(text, file_name):
    if os.path.exists('data/{}'.format(file_name)):
        with open('data/{}'.format(file_name), 'a') as f:
            f.write(text)
            f.write("\n")
    else:
        print("File does not exist, creating it now...")
        with open('data/{}'.format(file_name), 'a') as f:
            f.write(text)
            f.write("\n")
