library(kableExtra)
library(magrittr)

library(readr)
library(dplyr)
library(lubridate)
library(stringr)
library(readxl)
library(MVN)
library(outliers)


# 4. Data [Plain text & R code & Output] ----------------------------------


getwd()
setwd('/Users/chello/Desktop/RMIT/Math2349 - Data Wrangling/pratical assessment 2')
property <- read_csv('data/property.csv')
usr_act <- read_csv('data/user_activity.csv')
evt_types <- read_excel('data/event_types.xlsx')

head(property)
head(usr_act)
head(evt_types)

# requirement 1
#merged <- merge(x=property, y=usr_act, by = "item_id")
usr_act_detail <- merge(x=usr_act, y=evt_types, 
                by.x = c("event_type"), by.y = c("Event type") )
head(usr_act_detail)

# requirement 2
str(usr_act_detail)

dim(property)
dim(usr_act)
dim(evt_types)
dim(usr_act_detail)

c(evt_types['Event type'])


evt_types_lv = evt_types[['Event type']]

# requirement 3 & 4
usr_act_detail$event_type <-
  factor(usr_act_detail$event_type,
         levels = evt_types_lv,
         ordered = TRUE)
head(usr_act_detail)

str(usr_act_detail['event_type'])


# 5. Understand [Plain text & R code & Output]: ---------------------------

# create a new column as create_date from create_timestamp
usr_act_detail$create_date <- as.Date(usr_act_detail$create_timestamp)
# another data type conversions done in section 4 for event_type

print('Type of usr_act_detail:')
typeof(usr_act_detail)
print('Data Structure of usr_act_detail:')
str(usr_act_detail)
print('Class of usr_act_detail:')
class(usr_act_detail)
print('dimension of usr_act_detail:')
dim(usr_act_detail)



# 6. Tidy & Manipulate Data I [Plain text & R code & Output]: -------------
replace_0_na <- function(x) {
  ifelse(x == 0, NA, x)
}

# deposit, monthly_rent, unit_area - replace 0 to NA for statistics mis-calculation
# building_floor_count - replace 0 to NA as impossible is 0
property <- property %>%
  mutate(across(
    c(
      'deposit',
      'monthly_rent',
      'unit_area',
      'building_floor_count'
    ),
    replace_0_na
  ))


# unit floor 225 outliers

# check uniqueness for item_id
length(unique(property$item_id)) == dim(property)[1]
length(unique(property$district_uuid)) == dim(property)[1]
length(unique(usr_act_detail$uesr_id)) == dim(usr_act_detail)[1]

# unit floor -2 -1 0 may represent underground or ground floor


# 7. Tidy & Manipulate Data II [Plain text & R code & Output] -------------


property <- property %>%
  mutate(
    weekly_rent = monthly_rent * 12 / 52,
  )

# for step 9
property <- property %>%
  mutate(
    deposit_rent_area_ratio = deposit / (monthly_rent * unit_area),
  )

# 8. Scan I [Plain text & R code & Output] --------------------------------

district_deposit_mean <- property %>%
  group_by(district_uuid) %>%
  summarise(across(deposit, mean, .names="district_deposit_mean", na.rm = TRUE))

property <- merge(x=property, y=district_deposit_mean, 
                  by = "district_uuid" )

property <- property %>%
  mutate(cleaned_deposit = ifelse(
    is.na(monthly_rent),
    `district_deposit_mean`,
    `monthly_rent`
  ))

district_monthly_rent_mean <- property %>%
  group_by(district_uuid) %>%
  summarise(across(monthly_rent, 
                   mean, 
                   .names = "district_monthly_rent_mean", 
                   na.rm = TRUE))

property <- merge(x = property, y = district_monthly_rent_mean,
                  by = "district_uuid")

property <- property %>%
  mutate(cleaned_monthly_rent = ifelse(
    is.na(monthly_rent),
    `district_monthly_rent_mean`,
    `monthly_rent`
  ))

# 9. Scan II [Plain text & R code & Output] -------------------------------
options(scipen = 999)
property$cleaned_deposit %>% 
  boxplot(main="Cleaned Deposit", ylab="deposit($)", col = "grey")
property$cleaned_monthly_rent %>% 
  boxplot(main="Cleaned Monthly Rent", ylab="rent($)", col = "grey")
property$room_qty %>% 
  boxplot(main="Room Qty", ylab="Qty", col = "grey")
property$unit_area %>% 
  boxplot(main="Unit Area", ylab="Area", col = "grey")
property$building_floor_count %>% 
  boxplot(main="Building Floor Count", ylab="Count", col = "grey")
property$unit_floor %>% 
  boxplot(main="Unit Floor", ylab="Floor", col = "grey")
property$property_age %>% 
  boxplot(main="Property Age", ylab="Age(year)", col = "grey")


p <- property %>% select('cleaned_deposit', 'cleaned_monthly_rent','district_uuid') %>% group_by(district_uuid)
p
results <-
  mvn(
    data = property %>% select('cleaned_deposit', 'cleaned_monthly_rent'),
    multivariateOutlierMethod = "adj",
    showOutliers = TRUE,
    bc = TRUE, bcType="optimal"
  )
results$multivariateOutliers

p2 <- property %>% select('unit_floor', 'building_floor_count')

results <-
  mvn(
    data = p2,
    univariatePlot="box",
    multivariateOutlierMethod = "quan",
    showOutliers = TRUE
  )
results$multivariateOutliers

# 10. Transform [Plain text & R code & Output] ----------------------------
scale_df1 <- scale(property['cleaned_deposit'], center = TRUE, scale = TRUE)

list(log(scale_df1))
