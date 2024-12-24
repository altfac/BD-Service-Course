import uvicorn

if __name__ == "__main__":
    uvicorn.run("education_tasks:education_router", host="127.0.0.4", port=8003, log_level="info", reload=True)
