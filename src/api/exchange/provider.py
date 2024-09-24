class ProviderServiceInterface:
    def __init__(self, provider):
        self.provider = provider

    def get_price_history(self, *args, **kwargs):
        raise NotImplementedError

    def get_price(self, *args, **kwargs):
        raise NotImplementedError