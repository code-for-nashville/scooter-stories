# Scooter Rides: Weekend vs Weekday
# scooter-rides-weekend-vs-weekday.R
# Author: Owen Thompson
# Contact: octhompson19@gmail.com
# Date Created: 09.25.19


# 0 Set up ####
if (!require("pacman")) install.packages("pacman")
library(pacman)
p_load(tidyverse, scales, lubridate, ggthemes, ggpubr)

# Download Code for Nashville's "open-data-portal" repo from Krys Mathis
raw_data_url <- "https://raw.githubusercontent.com/code-for-nashville/open-data-portal/feature/scooter-2019-09-clean-up/nashville/scooter-data/scooter_extract_2019-07-20_to_2019-09-09.csv"
# 1 Data Wrangling ####

scoot <- read_csv(raw_data_url, 
               col_types = cols(.default = col_character(),
                                availability_duration = col_double(),
                                availability_start_date = col_date(format = ""),
                                availability_start_time = col_time(format = ""),
                                gps_latitude = col_double(),
                                gps_longitude = col_double(),
                                real_time_fare = col_double(),
                                availability_start_date_cst = col_date(format = ""),
                                availability_start_time_cst = col_time(format = ""),
                                availability_duration_seconds = col_double(),
                                first_extract_date_cst = col_date(format = ""),
                                first_extract_time_cst = col_time(format = ""),
                                first_extract_date_utc = col_date(format = ""),
                                first_extract_time_utc = col_time(format = ""), 
                                last_extract_date_cst = col_date(format = ""),
                                last_extract_time_cst = col_time(format = ""),
                                last_extract_date_utc = col_date(format = ""),
                                last_extract_time_utc = col_time(format = "")))

## Check dates of scotter rides:
##scoot %>% 
##  summarise(min_datetime = min(last_extract_date_cst), 
##            max_datetime = max(last_extract_date_cst))
## 7/20/19 to 9/20/19

explore_scoot <- scoot %>% 
  filter(gps_longitude < -50) %>%  # filter to remove scooters west of -50 degrees longitude
  arrange(sumd_id, last_extract_date_cst, last_extract_time_cst) %>% 
  group_by(sumd_id) %>% 
  mutate(id = row_number()) %>% 
  mutate(prev_avail_seconds = lag(availability_duration_seconds, n = 1, order_by = id)) %>% 
  filter(availability_duration_seconds < prev_avail_seconds) %>% 
  mutate(prev_lat = lag(gps_latitude, n = 1), 
         prev_lon = lag(gps_longitude, n = 1)) %>% 
  filter(!is.na(prev_lat)) %>% 
  ungroup() %>% 
  mutate(hr = hour(availability_start_time_cst)) %>% 
  mutate(day_type = if_else(wday(availability_start_date_cst, week_start = 1) > 5, "Weekend", "Weekday"), 
         dow = wday(availability_start_date_cst, label = T, abbr = F), 
         wk = floor_date(availability_start_date_cst, "week") %>% format("%m-%d"))

# 3 Data viz ####
explore_scoot %>% 
  ggplot(aes(x = hr, fill = day_type, group = last_extract_date_cst)) + 
  geom_histogram(bins = 24, alpha = 0.2, position = "identity") +
  # stat_bin(geom = "step", bins = 23, binwidth = 1, position = "identity") +
  scale_x_continuous(labels = c("5am","8am","Noon","5pm","8pm"),
                     breaks = c(5, 8, 12, 17, 20)) + 
  scale_y_continuous(labels = comma_format()) + 
  theme_fivethirtyeight() + 
  theme(strip.background = element_rect(fill = "#FFFFFF")) + 
  facet_wrap(.~day_type, nrow = 1) +
  labs(fill = "", 
       title = "Scooter ride distribution\nWeekday vs. Weekend") + 
  scale_fill_fivethirtyeight() %>% 
  ggsave("scooter-rides-weekday-vs-weekend.png)
