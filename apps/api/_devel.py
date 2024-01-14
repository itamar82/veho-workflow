import uvicorn

from apps.api.component import create_app

component = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "apps.api._devel:component",
        host="0.0.0.0",  # nosec: B104
        port=5000,
        reload=True,
        reload_dirs=["components", "settings"],
    )
