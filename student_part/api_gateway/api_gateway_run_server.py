import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.7", port=8006, log_level="info", reload=True)
