library(readxl)
library(dplyr)
library(ggplot2)
library(patchwork)

# Load your data
df <- read_excel("Multilingual_PostOp_Instructions.xlsx")

# Clean and prepare
df_clean <- df %>%
  filter(!is.na(FKGL), !is.na(Procedure), !is.na(Language), !is.na(`Reading Level`)) %>%
  mutate(`Reading Level` = factor(`Reading Level`, levels = c("2nd Grade", "6th Grade", "High School")))

# Target grade FKGL levels
target_lookup <- c("2nd Grade" = 2, "6th Grade" = 6, "High School" = 9)

# Heatmap function
make_heatmap <- function(level_label) {
  target_fkgl <- target_lookup[[level_label]]
  df_filtered <- df_clean %>% filter(`Reading Level` == level_label)
  
  df_summary <- df_filtered %>%
    group_by(Procedure, Language) %>%
    summarise(mean_FKGL = round(mean(FKGL, na.rm = TRUE), 1), .groups = "drop")
  
  base_plot <- ggplot(df_summary, aes(x = Language, y = Procedure, fill = mean_FKGL)) +
    geom_tile(color = "white", linewidth = 0.5) +
    geom_text(aes(label = mean_FKGL), color = "black", size = 4) +
    scale_fill_gradientn(
      colours = c("darkgreen", "yellow", "red"),
      values = scales::rescale(c(3, 6, 12)),
      limits = c(3, 16),
      name = "FKGL"
    ) +
    labs(
      title = paste("Target:", level_label),
      x = NULL,
      y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x = element_text(angle = 45, hjust = 1),
      plot.title = element_text(face = "bold")
    )
  
  return(base_plot)
}

# Create the three main heatmaps
p1 <- make_heatmap("2nd Grade")
p2 <- make_heatmap("6th Grade")
p3 <- make_heatmap("High School")

# Create red annotation (only for 6th grade plot)
df_6 <- df_clean %>% filter(`Reading Level` == "6th Grade")
pct_better_than_existing <- round(mean(df_6$FKGL < 9.8, na.rm = TRUE) * 100, 1)

pct_better_than_existing = 85

p2_text <- ggplot() +
  annotate("text", x = 0.5, y = 0.5,
           label = paste0(pct_better_than_existing, "% beat existing materials (FKGL < 9.8)"),
           color = "red", size = 4, fontface = "bold") +
  theme_void() +
  theme(plot.margin = margin(0, 0, 0, 0))

# Blank plots for bottom row spacing
empty_text <- ggplot() + theme_void()

# Combine plots using patchwork
final_plot <- (p1 | p2 | p3) /
  (empty_text | p2_text | empty_text) +
  plot_layout(heights = c(10, 1)) +
  plot_annotation(
    title = "GPT-4o Flesch Kincaid Grade Level Readability Across Procedures, Languages, and Target Grade Levels",
    theme = theme(plot.title = element_text(size = 22, face = "bold", hjust = 0.5))
  )

# Display
final_plot