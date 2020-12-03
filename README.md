# copycat
Test data runner


### Setup 

Use python 3.9
``` 
pip install -r requirements.txt
```

### Run
To run locally you should have `IDENTITY_USERNAME` and `IDENTITY_PASSWORD` in your system environment variables

``` 
flask run
``` 

### Endpoint: 
```
http://127.0.0.1:5000/validate/org_id/{{org_id}}/design/{{design_name}}
```

### Run unit tests with coverage

```
pytest
```

### Run linter

```bash
flake8 .
isort -rc -c .

```
### To atomically run isort against a project, only applying changes if they don't introduce syntax errors do:
```bash
isort -rc --atomic .
```

#### Worked example on **TEST** env:
```
Org ID: 177994338583572210389088925105933476529

Design Name: Target_RSX_7.7_Invoices_to_X12_4010_Transaction-810
```