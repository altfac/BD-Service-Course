import uvicorn

if __name__ == "__main__":
    uvicorn.run("users:users_router", host="127.0.0.10", port=8009, log_level="info", reload=True)
