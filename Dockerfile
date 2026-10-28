FROM ghcr.io/fedlearnnet/python-tool-api/base-r-dep-biocmanager:0.7.15.dev

USER root
ENV MAKEFLAGS=-j2

RUN apk add --no-cache libuv-dev cmake make gcc

RUN R -q -e 'options(repos = c(CRAN = "https://cloud.r-project.org"), Ncpus = 2); \
    dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE, showWarnings = FALSE); \
    .libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()));'

RUN R -q -e 'options(repos = c(CRAN = "https://cloud.r-project.org"), Ncpus = 2); install.packages("fs");'

RUN R -q -e 'options(repos = c(CRAN = "https://cloud.r-project.org"), Ncpus = 2);  \
    install.packages(c("BiocManager", "png", "htmlwidgets", "rmarkdown"), lib = Sys.getenv("R_LIBS_USER"), dependencies = NA);'

RUN R -q -e 'options(repos = c(CRAN = "https://cloud.r-project.org"), Ncpus = 2); install.packages(c("htmlTable", "Hmisc"), lib = Sys.getenv("R_LIBS_USER"), dependencies = NA); \
    BiocManager::install(c("Biostrings", "KEGGREST", "AnnotationDbi", "GO.db", "preprocessCore", "impute", "limma"), ask = FALSE, update = FALSE, lib = Sys.getenv("R_LIBS_USER")); \
    install.packages("WGCNA", lib = Sys.getenv("R_LIBS_USER"), dependencies = NA); \
    library(WGCNA, lib.loc = Sys.getenv("R_LIBS_USER"))'

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R nonroot:nonroot /app /opt/venv /usr/lib/R /usr/share/R /app/R/ \
 && chmod -R u+rwX,g+rwX /app /opt/venv /usr/lib/R /usr/share/R /app/R/

ENV MPLBACKEND=Agg

USER nonroot:nonroot

CMD ["python", "-m", "main"]
