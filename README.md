# Scientific Paper Data Extraction Pipeline

This project provides a comprehensive pipeline for extracting and processing time series data from scientific papers. It automates the process of downloading papers from arXiv, filtering relevant PDFs, extracting images, and converting them into time series data.

## Project Overview

The pipeline consists of several Python scripts that work together to:

1. Download papers from arXiv
2. Filter PDFs based on specific criteria
3. Extract images and captions from papers
4. Process and crop PDFs
5. Identify line charts
6. Convert PDFs to SVG format
7. Extract time series data from SVG files

## Prerequisites

- Python 3.x
- Conda (for managing dependencies)
- SBT (Scala Build Tool)
- PDFFigures2 (for image extraction)
- pdf2svg package

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/scientific-paper-extraction.git
cd scientific-paper-extraction
```

2. Install pdf2svg using conda:

```bash
conda install -c conda-forge pdf2svg
```

3. Set up PDFFigures2 (required for image extraction):

```bash
git clone https://github.com/allenai/pdffigures2.git
cd pdffigures2
```

Add the following dependencies to `build.sbt`:

```scala
libraryDependencies ++= Seq(
  "com.github.jai-imageio" % "jai-imageio-core" % "1.2.1",
  "com.github.jai-imageio" % "jai-imageio-jpeg2000" % "1.3.0",
  "com.levigo.jbig2" % "levigo-jbig2-imageio" % "1.6.5"
)
```

4. Install SBT and compile PDFFigures2:

```bash
# Install SDKMAN (if not already installed)
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# Install SBT
sdk install sbt

# Compile PDFFigures2
sbt compile
sbt assembly
```

## Pipeline Steps

### 1. Downloading Papers (`downloading_arxiv.py`)

- Downloads scientific papers from arXiv based on specified criteria
- Usage: `python downloading_arxiv.py`

### 2. Filtering PDFs (`filtering_pdfs.py`)

- Processes downloaded PDFs and filters them based on specific criteria
- Usage: `python filtering_pdfs.py`

### 3. Extracting Images

- Uses PDFFigures2 to extract images and captions from papers
- Follow instructions in `extracting_imgs.md`
- Run PDFFigures2:

```bash
sbt "runMain org.allenai.pdffigures2.FigureExtractorBatchCli /path/to/pdf_directory/ -s /output/folder/stat_file.json -m /output/folder/ -d /output/folder/"
```

### 4. Processing PDFs (`crop2pdf.py`)

- Crops and processes PDF files
- Usage: `python crop2pdf.py`

### 5. Line Chart Detection (`isLine.py`)

- Identifies and classifies line charts in the extracted images
- Usage: `python isLine.py`

### 6. PDF to SVG Conversion (`pdf2svg.py`)

- Converts PDF files to SVG format
- Matches IDs with line chart detection results
- Usage: `python pdf2svg.py`

### 7. Time Series Extraction (`svg2time_series.py`)

- Extracts time series data from SVG files
- Usage: `python svg2time_series.py`

## Project Structure

```
scientific-paper-extraction/
├── downloading_arxiv.py    # ArXiv paper download script
├── filtering_pdfs.py       # PDF filtering and processing
├── extracting_imgs.md      # Image extraction documentation
├── crop2pdf.py            # PDF cropping utility
├── isLine.py              # Line chart detection
├── pdf2svg.py             # PDF to SVG conversion
├── svg2time_series.py     # Time series data extraction
└── chart_classification_model/ # Model for chart classification
```
