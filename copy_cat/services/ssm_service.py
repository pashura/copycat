import boto3


class SSMSecrets:
    def __init__(self, env, region='us-east-1'):
        self.parameters = {}
        self.env = env
        self.region = region

    def _get_by_path(self):
        ssm = boto3.client("ssm", region_name=self.region)
        parameters = []
        path = "{}/{}/".format("/tpd/jenkins/xtencil-to-design", self.env)
        args = dict(Path=path, WithDecryption=True, Recursive=True)
        res = ssm.get_parameters_by_path(**args)
        parameters.extend(res['Parameters'])
        self.parameters = {item['Name'].replace(path, ''): item['Value'] for item in parameters}

    def get_key(self, key):
        if not self.parameters:
            self._get_by_path()
        return self.parameters.get(key)
