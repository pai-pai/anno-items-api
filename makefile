IMAGE_REG ?= ghcr.io
IMAGE_REPO ?= pai-pai/anno-items-api
IMAGE_TAG ?= latest


SRC_DIR := src

image:  ## 🔨 Build container image from Dockerfile 
	docker build . --file build/Dockerfile \
	--tag $(IMAGE_REG)/$(IMAGE_REPO):$(IMAGE_TAG)

run: venv
	. $(SRC_DIR)/.venv/bin/activate \
	&& python src/run.py

test: venv
	. $(SRC_DIR)/.venv/bin/activate \
	&& pytest -v

venv: $(SRC_DIR)/.venv/touchfile

$(SRC_DIR)/.venv/touchfile: $(SRC_DIR)/requirements.txt
	python3 -m venv $(SRC_DIR)/.venv
	. $(SRC_DIR)/.venv/bin/activate; pip install -Ur $(SRC_DIR)/requirements.txt
	touch $(SRC_DIR)/.venv/touchfile
