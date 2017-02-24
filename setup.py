from setuptools import setup

setup(name='command_line_blog',
      version='0.1.2',
      description='Publish to the web with just curl!',
      url='http://github.com/seanbehan/command_line_blog',
      author='Sean Behan',
      author_email='inbox@seanbehan.com',
      license='MIT',
      packages=['command_line_blog'],
      zip_safe=False,
      install_requires=[
        'flask', 'dataset'
      ])
