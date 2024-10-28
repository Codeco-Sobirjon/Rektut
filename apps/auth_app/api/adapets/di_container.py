from apps.auth_app.api.adapets import oauth_adapters


class DIContainer:
    """Dependency Injection Container"""

    def __init__(self):
        self._providers = {}

    def register(self, interface, provider):
        self._providers[interface] = provider

    def get(self, interface):
        provider = self._providers.get(interface)
        if provider is None:
            raise ValueError(f"No provider registered for {interface}")
        return provider


container = DIContainer()

# OAuth providers
container.register("google_auth", oauth_adapters.GoogleAuth)
