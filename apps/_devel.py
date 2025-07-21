import uvicorn

from apps.main import create_app

component = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "apps._devel:component",
        host="0.0.0.0",  # nosec: B104
        port=8000,
        reload=True,
        reload_dirs=["apps"],
        log_level="debug",
    )
