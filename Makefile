hello:
	echo "Hello world!"

test:
	pytest love_letter/test_main.py --capture=no
