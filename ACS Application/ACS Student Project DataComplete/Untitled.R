library(tidyverse)
library(readxl)

# Load data
df <- read_excel("Multilingual_PostOp_Instructions.xlsx")

# --- 1. Define New Target Scores ---
targets <- tibble(
  `Reading Level` = c("Child", "Average Adult", "High School Graduate"),
  FKGL = c(3, 7, 10),
  SMOG = c(4.5, 8.5, 10.5),
  `Flesch-Ease` = c(90, 75, 60)
)

# --- 2. Calculate GPT Means from Your Data ---
gpt_means <- df %>%
  mutate(`Reading Level` = recode(`Reading Level`,
                                  "2nd Grade" = "Child",
                                  "6th Grade" = "Average Adult",
                                  "High School" = "High School Graduate")) %>%
  group_by(`Reading Level`) %>%
  summarise(
    FKGL = mean(FKGL, na.rm = TRUE),
    SMOG = mean(SMOG, na.rm = TRUE),
    `Flesch-Ease` = mean(`Flesch-Ease`, na.rm = TRUE)
  )

# --- 3. Reshape for Plotting ---
gpt_long <- pivot_longer(gpt_means, cols = -`Reading Level`, names_to = "Metric", values_to = "GPT")
target_long <- pivot_longer(targets, cols = -`Reading Level`, names_to = "Metric", values_to = "Target")

# Combine both
plot_data <- left_join(gpt_long, target_long, by = c("Reading Level", "Metric"))

# Flip Flesch-Ease for better visual consistency
plot_data <- plot_data %>%
  mutate(
    GPT_flipped = ifelse(Metric == "Flesch-Ease", -GPT, GPT),
    Target_flipped = ifelse(Metric == "Flesch-Ease", -Target, Target),
    Metric = ifelse(Metric == "Flesch-Ease", "Flesch-Ease (flipped)", Metric)
  )

# --- 4. Set X-axis Order ---
plot_data$`Reading Level` <- factor(plot_data$`Reading Level`,
                                    levels = c("Child", "Average Adult", "High School Graduate"))

# --- 5. Plot ---
ggplot(plot_data, aes(x = `Reading Level`)) +
  geom_line(aes(y = GPT_flipped, group = 1, color = "GPT Output"), size = 1.2) +
  geom_line(aes(y = Target_flipped, group = 1, color = "Target"), linetype = "dashed", size = 1.2) +
  facet_wrap(~ Metric, scales = "free_y") +
  scale_color_manual(values = c("GPT Output" = "blue", "Target" = "orange")) +
  labs(
    title = "Comparison of GPT-Generated Readability vs Literacy Benchmarks",
    y = "Readability Score\n(All Metrics: UP = More Difficult)",
    color = "Legend"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "top",
    strip.text = element_text(face = "bold")
  )


# Merge target values into main data
df_joined <- df %>%
  left_join(target_table, by = "Reading Level")

# --- Flesch Reading Ease Heatmap ---
heat_data <- df_joined %>%
  group_by(Language, `Reading Level`, Stage) %>%
  summarize(AvgFlesch = mean(`Flesch-Ease`, na.rm = TRUE), .groups = "drop")

ggplot(heat_data, aes(x = `Reading Level`, y = Language, fill = AvgFlesch)) +
  geom_tile(color = "white") +
  geom_text(aes(label = round(AvgFlesch, 1)), color = "black") +
  facet_wrap(~Stage) +
  scale_fill_gradient2(low = "#d73027", mid = "#ffffbf", high = "#1a9850", midpoint = 60) +
  labs(title = "Flesch Reading Ease by Language, Level, and Stage",
       x = "Reading Level", y = "Language", fill = "Flesch Score") +
  theme_minimal(base_size = 14)



library(tidyverse)
library(readxl)

# Load your data
df <- read_excel("Multilingual_PostOp_Instructions.xlsx")

# Set target Flesch scores
target_table <- tibble(
  `Reading Level` = c("Child", "Average Adult", "High School Graduate"),
  TargetFlesch = c(90, 75, 60)
)

# Recode and merge targets
df_joined <- df %>%
  mutate(`Reading Level` = recode(`Reading Level`,
                                  "2nd Grade" = "Child",
                                  "6th Grade" = "Average Adult",
                                  "High School" = "High School Graduate")) %>%
  left_join(target_table, by = "Reading Level")

# Calculate Δ from target
heat_data <- df_joined %>%
  group_by(Language, `Reading Level`, Stage) %>%
  summarize(
    AvgFlesch = mean(`Flesch-Ease`, na.rm = TRUE),
    TargetFlesch = first(TargetFlesch),
    DiffFromTarget = AvgFlesch - TargetFlesch,
    .groups = "drop"
  )

# Make heatmap
ggplot(heat_data, aes(x = `Reading Level`, y = Language, fill = DiffFromTarget)) +
  geom_tile(color = "white") +
  geom_text(aes(label = sprintf("%+.1f", DiffFromTarget)), color = "black") +
  facet_wrap(~Stage) +
  scale_fill_gradient2(
    low = "#d73027", mid = "#ffffbf", high = "#1a9850", midpoint = 0,
    name = "Δ from Target\n(+ = Easier)"
  ) +
  labs(
    title = "GPT Output Reading Level Compared to Target Readability",
    subtitle = "Flesch Reading Ease: Positive = Easier than Target, Negative = Harder",
    x = "Intended Reading Level", y = "Language"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    strip.text = element_text(face = "bold"),
    legend.position = "right"
  )