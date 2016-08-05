## Before you start

Install libraries:

	$ pip install -r requirements.txt

Create a local file

	$ cp CommentIsMee/settings/_example.py CommentIsMee/settings/_ENV_.py

Install database:

	$ ./manage.py makemigrations articles
	$ ./manage.py migrate

Collect static (production only)

	$ ./manage.py collectstatic
