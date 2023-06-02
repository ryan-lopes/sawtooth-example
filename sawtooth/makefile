up:
	docker compose -f sawtooth-default.yaml up -d
down:
	docker compose -f sawtooth-default.yaml down -t 1
restart:
	docker compose -f sawtooth-default.yaml down -t 1 && docker compose -f sawtooth-default.yaml up -d
bash:
	docker exec -it sawtooth-dev-default bash
dapp:
	docker exec -t sawtooth-dev-default bash -c "cd sawtooth/client/ ; python3 dapp.py"
server:
	docker exec -t sawtooth-dev-default bash -c "cd sawtooth/server/ ; python3 main.py"