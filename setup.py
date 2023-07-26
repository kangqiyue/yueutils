from setuptools import setup, find_packages

setup(
  name='yueutils',        # How you named your package folder (foo)
  packages=find_packages(),   # Chose the same as "name"
  package_dir={'yueutils': 'src/yueutils'},
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='afl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'common utils function',   # Give a short description about your library
  author = 'Alex',                   # Type in your name
  install_requires=[["toml", "jsonlines"]],
  # classifiers=[
  #   'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
  #   'Intended Audience :: Developers',      # Define that your audience are developers
  #   'Topic :: Software Development :: Build Tools',
  #   'License :: OSI Approved :: MIT License',   # Again, pick a license
  #   'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  #   'Programming Language :: Python :: 3.4',
  #   'Programming Language :: Python :: 3.5',
  #   'Programming Language :: Python :: 3.6',
  # ],
)