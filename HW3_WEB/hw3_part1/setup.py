from setuptools import setup, find_namespace_packages

setup(name = 'clean_folder',
      version = '1.0.0',
      description = 'script for folders cleaning',
      url = '',
      author= 'Yakovlieva Yana',
      author_email= 'yanayakovleva362@gmail.com',
      license= 'MIT',
      packages=  find_namespace_packages(),
      entry_points ={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)