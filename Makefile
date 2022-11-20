hello:
	echo "Hello world!"

test:
	#pytest love_letter/test_main.py --capture=no
	pytest love_letter/test_main.py::test_read_main --capture=no

