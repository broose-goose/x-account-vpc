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

push-docker:
	docker image build -t 066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_2-7092655:main .
	aws ecr get-login-password | docker login --username AWS --password-stdin 066540957026.dkr.ecr.us-east-1.amazonaws.com
	docker push 066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_2-7092655:main