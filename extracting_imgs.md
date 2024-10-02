How to extract images and captions. 

Step 1:
`git clone https://github.com/allenai/pdffigures2.git`

Step 2:
-> go to pdffigures2 
-> Add below code in build.sbt

libraryDependencies ++= Seq(
  "com.github.jai-imageio" % "jai-imageio-core" % "1.2.1",
  "com.github.jai-imageio" % "jai-imageio-jpeg2000" % "1.3.0",
  "com.levigo.jbig2" % "levigo-jbig2-imageio" % "1.6.5"
)

Step 3:
-> Install sdkman if not already installed (https://sdkman.io/install/)

Step 4:
-> install sbt using sdkman (https://www.scala-sbt.org/1.x/docs/Installing-sbt-on-Linux.html)

Step 5:
-> Execute code below in pdffigures2
`sbt compile`
`sbt assembly`

Step 6:
-> Modify directories in the code below before running.

`sbt "runMain org.allenai.pdffigures2.FigureExtractorBatchCli /path/to/pdf_directory/ -s /output/folder/stat_file.json -m /output/folder/image_prefix -d /output/folder/data_prefix"`

sbt "runMain org.allenai.pdffigures2.FigureExtractorBatchCli /projects/bdata/llm_for_timeseries/scientific-paper-extraction/data/modified_pdfs/ -s stat_file.json -m /projects/bdata/llm_for_timeseries/scientific-paper-extraction/data/image_extraction/image_prefix -d /projects/bdata/llm_for_timeseries/scientific-paper-extraction/data/stats_extraction/data_prefix"

find /projects/bdata/llm_for_timeseries/scientific-paper-extraction/data -name "*.json" -type f -exec cp {} /projects/bdata/llm_for_timeseries/scientific-paper-extraction/data/stats_image_extraction/ \; -exec rm {} +