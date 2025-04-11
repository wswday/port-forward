## Usage:

1. command-line
	```
	python3 forward.py <source hostname> <source port> <destination hostname> <destination port>
	e.g.
	python3 forward.py localhost 8080 localhost 22
	```

2. Using config file
	```
	# update config file
	python3 forward.py
	```

---
All log will be write to log.txt


## rforward.py
实现ssh -CNR [REMOTE_BIND_ADDRESS:]REMOTE_PORT:LOCAL_HOST:LOCAL_PORT USER@REMOTE_SERVER

