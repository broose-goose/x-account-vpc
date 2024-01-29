install-local:
	pipenv lock
	pipenv install

run-local:
	python app.py

build-local:
	docker image build -t sandbox-2 .

run-docker: build-local
	docker network create --driver bridge sandbox || true
	docker container run --network=sandbox -p 5002:5002/tcp --name sandbox-2 sandbox-2