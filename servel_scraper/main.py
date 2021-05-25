from servel_scraper.servel_pipeline.servel_pipeline import ServelPipeline, PipelineStage

DEFAULT_PDF_DOWNLOAD_PATH = "out/pdf"
DEFAULT_GENERATED_CSV_PATH = 'out/csv'

if __name__ == '__main__':
    p = ServelPipeline(DEFAULT_PDF_DOWNLOAD_PATH, DEFAULT_GENERATED_CSV_PATH)
    p.run_pipeline([
        PipelineStage.DOWNLOAD_PDFS,
        PipelineStage.EXTRACT_CSV_FROM_PDF
    ])
