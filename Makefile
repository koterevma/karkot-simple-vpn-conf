
install: setup
	echo Here will be instalation code

setup:
	python3 -m venv env
	. env/bin/activate
	pip install -r ./requirements.txt
