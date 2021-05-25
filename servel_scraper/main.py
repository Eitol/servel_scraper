import os
import pathlib

from servel_scraper.servel_pipeline.servel_pipeline import ServelPipeline, PipelineStage

current_path = str(pathlib.Path(__file__).parent.absolute())

DEFAULT_PDF_DOWNLOAD_PATH = os.path.join(current_path, '..', 'out', 'pdf')
DEFAULT_GENERATED_CSV_PATH = os.path.join(current_path, '..', 'out', 'csv')

if __name__ == '__main__':
    os.makedirs(DEFAULT_PDF_DOWNLOAD_PATH)
    os.makedirs(DEFAULT_GENERATED_CSV_PATH)
    p = ServelPipeline(DEFAULT_PDF_DOWNLOAD_PATH, DEFAULT_GENERATED_CSV_PATH)
    p.run_pipeline([
        PipelineStage.DOWNLOAD_PDFS,
        PipelineStage.EXTRACT_CSV_FROM_PDF
    ])
