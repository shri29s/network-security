from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.pipeline.batch_prediction import BatchPrediction
from mongo.load_data import DataETL
from networksecurity import constants
from networksecurity.utils.utils import init_dagshub
from networksecurity.logging.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles

import os

logging.info("Starting the application....")
init_dagshub()

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), "static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/train")
async def train_route():
    try:
        train_pipe = TrainingPipeline()
        modelTrainerArtifact = train_pipe.run_pipeline()
        return Response(f"Training successful, model trainer artifact: {modelTrainerArtifact}", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/load_data")
async def load_data_mongo():
    try:
        etlPipe = DataETL("./Network_Data/phisingData.csv", constants.DATA_INGESTION_DATABASE_NAME, constants.DATA_INGESTION_COLLECTION_NAME)
        etlPipe.convert_json() # Extract
        etlPipe.push_mongo() # Load
        return Response("ETL pipeline successful", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/predict")
async def batch_prediction(request: Request, file: UploadFile = File(...)):
    try:
        batchPrediction = BatchPrediction()
        df = batchPrediction.batch_prediction(file=file.file)
        table_html = df.to_html()
        return templates.TemplateResponse(request=request, name="table.html", context={"table": table_html})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__=="__main__":
    port = int(os.getenv("PORT", 8080))
    app_run(app, host="0.0.0.0", port=port)