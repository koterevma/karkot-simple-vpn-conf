BIN_DIR=/usr/local/bin
PROG_NAME=create_new_client
CUR_DIR=$(shell pwd)

install: setup
	sudo ln -sf ${CUR_DIR}/${PROG_NAME}.sh ${BIN_DIR}/${PROG_NAME} 

setup: env
	. env/bin/activate && pip install -r ./requirements.txt

env:
	python3 -m venv env

uninstall:
	sudo rm -f ${BIN_DIR}/${PROG_NAME}
	rm -rf env

