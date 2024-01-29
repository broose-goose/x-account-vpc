install-local:
	pipenv lock
	pipenv install

run-local:
	SANDBOX_2="http://localhost:5002" python app.py

build-local:
	docker image build -t sandbox-1 --build-arg SANDBOX_2="http://sandbox-2:5002" .

run-docker: build-local
	docker network create --driver bridge sandbox || true
	docker container run --network=sandbox -p 5001:5001/tcp --name sandbox-1 sandbox-1
