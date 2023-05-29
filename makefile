up-sawtooth:
	docker compose -f sawtooth-default.yaml up -d
down-sawtooth:
	docker compose -f sawtooth-default.yaml down -t 1
bash-sawtooth:
	docker exec -it sawtooth-dev-default bash
client:
	docker exec sawtooth-dev-default bash -c "python3 /sawtooth/client/client.py"
server:
	docker exec sawtooth-dev-default bash -c "python3 /sawtooth/entrypoint.py"
