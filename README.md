# celery-template
A template to manage workflows using a distributed task queue system

Features
- TBD

### Use cases
- TBD

### Installation guide

**Module setup**
1. `python3 -m venv .env` and `pip3 install --upgrade pip` 
2. `cd .env/scripts ` then `activate`
3. Modify `setup.cfg` and `src`
4. `pip3 install -e .`
5. Setup desired broker and backend 
	- broker:`sudo apt-get install rabbitmq-server` then `sudo service rabbitmq-server restart`
	- backend: See PostgreSQL backend database setup
6. `python3 -m app` as a seperate screen
7. Define [celery configurations](https://github.com/NeelRoshania/celery_template/blob/main/src/celery_template/__init__.py#L14)

If you run into issues with `psycopg2`, consider the following;
1. `sudo chmod 774 psycopg2_setup.sh`
2. `./psycopg2_setup.sh`
3. `pip3 install psycopg2`

**PostgreSQL backend database setup**
1. Create role, database and assign privalages
2. [Define connection string](https://docs.celeryq.dev/en/latest/userguide/configuration.html#database-backend-settings) per SQLAlchemy

**Task Queue setup** (to be refined)
1. Start services
    - postgresql: `service postgresql restart`
    - rabbitmq-server, `service rabbitmq-server restart`
2. Check message queues: `rabbitmqctl list_queues name messages messages_ready messages_unacknowledged`
3. Start worker, `celery -A celery_template worker --loglevel=INFO`
4. Run tests
	- Run a task: `res = add.apply_async(args=(5, 7), queue="celery_template_queue")`
	- Check tasks on backend database - `celery_taskmeta`
    		- If new task_id's are not generated, 
        		- check message queues
        	- ensure celery worker server is running
	- Check logs generated in worker server 

**PostgreSQL installation & setup**
1. See (Ubuntu PostgreSQL)[https://help.ubuntu.com/community/PostgreSQL] for complete guide
2. Run `install_start_server.sh` - this will install and start the service
3. Check that the service is running `[ + ]  postgresql`
    - `service --status-all`
4. `sudo service postgresql restart` - to restart the service if required

**Jupyter kernel setup**
1. `jupyter kernelspec uninstall .example_env` - remove existing kernels called .example_env
2. `python -m ipykernel install --user --name=.example_env`- install new kernel

**Testing**
1. `pytest -v`

**Environment & application setup**
1. `pytest -v`
2. `pytest tests/scripts/test_psqlconnect.py > tests/test_outcomes/010123` to dump results to file. Use `grep` to search through dump

### Repository setup
1. Authenticate with github 
    - SSH Agent
        - `eval "$(ssh-agent -s)"` to start agent 
        - `ssh-add -l` to check for existing keys
        - `ssh-add ~/.ssh/id_ed25519` to add SSH private key to ssh-agen
    - Test connection & authenticate, 
        - `ssh -T git@github.com`. See [Github SSH Authentication](https://docs.github.com/en/authentication).
2. Authentication troubleshooting
    - [Permission denied (publickey)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

References
1. Celery
    - [First steps]('https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html')
    - [API Reference](https://docs.celeryq.dev/en/stable/reference/index.html)
    - [Database backend settings](https://docs.celeryq.dev/en/latest/userguide/configuration.html#database-backend-settings)
    - [Inspecting queues](https://docs.celeryq.dev/en/stable/userguide/monitoring.html#inspecting-queues)
        - `rabbitmqctl list_queues name messages messages_ready messages_unacknowledged`
    - [Logging](https://docs.celeryq.dev/en/latest/userguide/tasks.html#logging)
    - [Configuration and defaults](https://docs.celeryq.dev/en/stable/userguide/configuration.html)
    - [Routing Tasks](https://docs.celeryq.dev/en/stable/userguide/configuration.html)
    - [Flower Monitoring Tool](https://flower.readthedocs.io/en/latest/)

2. PostgreSQL
    - [Client Applications](https://www.postgresql.org/docs/current/reference-client.html) 
	- `ls -al /usr/lib/postgresql/15/bin`
    - Debugging
        ```
        psql: could not connect to server: No such file or directory
              Is the server running locally and accepting connections on Unix domain socket "/tmp/.s.PGSQL.5432"?
        ```
        - Check that the server is running, `service --status-all`. 
            - Restart if neccesary, `sudo service postgresql restart`

3. Others
    - [subprocess](https://docs.python.org/3/library/subprocess.html#) - Subprocess Management
    - [Kill processes by command name](https://stackoverflow.com/questions/160924/how-can-i-kill-a-process-by-name-instead-of-pid-on-linux)
