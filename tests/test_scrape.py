# import os
#
# def _read_file(file_name):
#     """
#     Function to read a file from the resources folder
#     :param file_name: Name of the file to read
#     :return: Content of the file as a string
#     """
#     # Get the directory of the current script
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#
#     # Construct the path to the resources folder
#     resources_dir = os.path.join(current_dir, '..', 'resources')
#
#     # Construct the full path to the file
#     file_path = os.path.join(resources_dir, file_name)
#
#     # Read and return the file contents
#     with open(file_path, 'r') as f:
#         return f.read()
#
#
#
# def test_add():
#     input_html = _read_file('contact.html')
#     print(input_html)
#
