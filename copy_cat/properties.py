import os

ENV = os.environ.get('ENVIRON', 'local')


def get_property(name, env=ENV):
    props = {
        'local':  {
            'IDENTITY_URL': 'https://test.id.spsc.io',
            'TRANSFORMATION_DESIGNER_URL': 'https://design-ui-api.test.spsapps.net'
        },
        'test': {
            'IDENTITY_URL': 'https://test.id.spsc.io',
            'TRANSFORMATION_DESIGNER_URL': 'https://design-ui-api.test.spsapps.net',
        },
        'prod': {
            'IDENTITY_URL': 'https://id.spsc.io',
            'TRANSFORMATION_DESIGNER_URL': 'https://design-ui-api.spsapps.net',
        }
    }
    return props[env][name]
