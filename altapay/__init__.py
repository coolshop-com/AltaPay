__title__ = 'altapay'
__version__ = '1.2.1'
__author__ = 'Coolshop.com'
__license__ = 'MIT'
__github_url__ = 'https://github.com/coolshop-com/AltaPay'
__api_base_url__ = {
    'test': 'https://testgateway.altapaysecure.com/merchant/',
    'production': 'https://{shop_name}.altapaysecure.com/merchant/'
}

from altapay.api import API  # NOQA
from altapay.callback import Callback  # NOQA
from altapay.funding import CustomReport, Funding, FundingList  # NOQA
from altapay.payment import Payment  # NOQA
from altapay.resource import Resource  # NOQA
from altapay.transaction import Transaction  # NOQA
