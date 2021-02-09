import os
from pathlib import Path

my_folder = os.getenv('PWD')
my_parent_folder = Path(my_folder).parent

print('my folder is: {}'.format(my_folder))
print('my parent folder is: {}'.format(my_parent_folder))