from apps.api.endpoints import Endpoint

endpoint = Endpoint(prefix="/broadcast")


@endpoint.router.post("/github/hook")
def handle_github_hook():
    pass
