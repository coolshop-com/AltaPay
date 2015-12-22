__title__ = 'altapay'
__version__ = '0.1.dev1'
__author__ = 'Coolshop.com'
__license__ = 'MIT'
__github_url__ = 'https://github.com/coolshop-com/AltaPay'
__api_base_url__ = {
    'test': 'https://testgateway.altapaysecure.com/merchant/',
    'production': 'https://{shop_name}.altapaysecure.com/merchant/'
}

from .api import API  # NOQA
from .payment import Payment  # NOQA
from .resource import Resource  # NOQA
