health_summary <- function(path, plot_path = NULL) {
  if (grepl("\.json$", path)) {
    library(jsonlite)
    df <- jsonlite::read_json(path, simplifyVector = TRUE)
    df <- as.data.frame(df)
  } else {
    df <- read.csv(path)
  }
  df$timestamp <- as.POSIXct(df$timestamp)
  stats <- c(
    temp_avg = mean(df$cpu_temp, na.rm = TRUE),
    cpu_avg = mean(df$cpu_percent, na.rm = TRUE),
    mem_avg = mean(df$memory_percent, na.rm = TRUE),
    disk_avg = mean(df$disk_percent, na.rm = TRUE)
  )
  if (!is.null(plot_path)) {
    library(ggplot2)
    ggplot(df, aes(x = timestamp, y = cpu_temp)) +
      geom_line() + theme_minimal() -> p
    ggsave(plot_path, plot = p, width = 4, height = 2)
  }
  stats
}

if (!interactive()) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) < 1) {
    stop('usage: Rscript health_summary.R <file> [plot.png]')
  }
  res <- health_summary(args[[1]], if (length(args) >= 2) args[[2]] else NULL)
  print(res)
}
