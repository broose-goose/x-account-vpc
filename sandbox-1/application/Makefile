install-local:
	pipenv lock
	pipenv install

run-local:
	SANDBOX_2="http://localhost:5002" python app.py

build-local:
	docker image build -t sandbox-1:current --build-arg SANDBOX_2="http://sandbox-2:5002" .

run-docker: build-local
	docker network create --driver bridge sandbox || true
	docker container run --network=sandbox -p 5001:5001/tcp --name sandbox-1 sandbox-1:current

push-docker:
	docker image build -t 066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_1-d45f769:main \
		--build-arg SANDBOX_2="http://10.2.0.0:5002" .
	aws ecr get-login-password | docker login --username AWS --password-stdin 066540957026.dkr.ecr.us-east-1.amazonaws.com
	docker push 066540957026.dkr.ecr.us-east-1.amazonaws.com/sandbox_1-d45f769:main