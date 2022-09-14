# mock oauth2 server
flask + authlib, no database, configuration is extremely simple

### preparation
```bash
$ git clone https://github.com/psylity/oauth2mock
$ cd oauth2mock
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install -r requirements.txt
```

### configuration
You may edit or not `app.py` to adjust oauth2 server to your app. Most often it is the `scope` parameter.

### execution
```bash
$ flask run
```
Now you can navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000). It is default url, you can modify it 
by specifying port/host parameters, like that:
```bash
$ flask run --host 0.0.0.0 --port 8080
```