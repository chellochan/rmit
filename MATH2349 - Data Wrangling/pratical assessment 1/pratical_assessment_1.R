
# Install Library ---------------------------------------------------------

install.packages(readr)
install.packages(stringr)


# library used ------------------------------------------------------------

library(readr)
library(stringr)

# Step 2 Read -------------------------------------------------------------

wd <- readline(prompt="Enter working directory (Default is ~): ") #require to input working directory

#set wd to "~" as default directory 
if (str_trim(wd) == "") {
  wd <- "~/Desktop/RMIT/Math2349 - Data Wrangling/pratical assessment 1"
}

#process working directory with separator
wd_last_char <- str_sub(wd, start= -1) 

#get system separator
if (wd_last_char == .Platform$file.sep) {
  separator <- ""
} else {
  separator <- .Platform$file.sep
}

#Concatenate working directory with row data file
path <- paste(wd, "Superstore.csv", sep=separator)
print(path)

#Check data file exist
if (!file.exists(path)) {
  print("Working Directory is wrong. Please check and rerun Line 15 to set working directory.")
}

#To read file Superstore.csv to variable raw_data
raw_data <- read_csv(path)

#head of data set
head(raw_data)


# Step 3 description of the data and its source ---------------------------

url <- "https://www.kaggle.com/vivek468/superstore-dataset-final/version/1"

#print source of data
print(paste("URL of data:", url))

#print clear description of data (ref: https://www.kaggle.com/vivek468/superstore-dataset-final/version/1 Context)
print(paste("Clear description of data:", "With growing demands and cut-throat competitions in the market, a Superstore Giant is seeking your knowledge in understanding what works best for them. They would like to understand which products, regions, categories and customer segments they should target or avoid."))

#ref: https://www.kaggle.com/vivek468/superstore-dataset-final/version/1 MetaData
desc <- "Row ID => Unique ID for each row.
Order ID => Unique Order ID for each Customer.
Order Date => Order Date of the product.
Ship Date => Shipping Date of the Product.
Ship Mode=> Shipping Mode specified by the Customer.
Customer ID => Unique ID to identify each Customer.
Customer Name => Name of the Customer.
Segment => The segment where the Customer belongs.
Country => Country of residence of the Customer.
City => City of residence of of the Customer.
State => State of residence of the Customer.
Postal Code => Postal Code of every Customer.
Region => Region where the Customer belong.
Product ID => Unique ID of the Product.
Category => Category of the product ordered.
Sub-Category => Sub-Category of the product ordered.
Product Name => Name of the Product
Sales => Sales of the Product.
Quantity => Quantity of the Product.
Discount => Discount provided.
Profit => Profit/Loss incurred."

# print variable description 
print("variable description: ")
cat(desc)


# Step 4 Inspect the dataset and variables --------------------------------

# ● Check the dimensions of the data frame. 
print("Dimensions of data:")
print("total number of rows:")
print(dim(raw_data)[1]) #dim(object)[1] get object rows
print("total number of columns:")
print(dim(raw_data)[2]) #dim(object)[2] get object columns

# ● Check the column names in the data frame, rename them if required. 

head(raw_data, n=0) #print column names (no need to rename)

# ● Summarise the types of variables by checking the data types (i.e., character, numeric, 
#                                                                integer, factor, and logical) of the variables in the data set. If variables are not in the 
data <- head(raw_data, n=1)
typeof(data[1])

# aaa <- read_csv(path, col_types = cols(
#   'Row ID' = "i",
#   'Order ID' = "c",
#   'Order Date' = col_date("%m/%d/%Y"),
#   'Ship Date' = col_date("%m/%d/%Y"),
#   'Ship Mode' = col_factor(levels = c("Same Day", "First Class", "Second Class", "Standard Class"), ordered = c("Same Day", "First Class", "Second Class", "Standard Class")),
#   Segment = col_factor(levels = c("Consumer", "Corporate", "Home Office")),
#   'Postal Code' = "i",
#   Region = col_factor(levels = c("South", "East", "Central", "West")),
#   Category = "f",
#   'Sub-Category' = "f",
#   Quantity = "i"
#   ))

aaa <- read_csv(path, col_types = cols(
  'Row ID' = "i",
  'Order ID' = "c",
  'Order Date' = col_date("%m/%d/%Y"),
  'Ship Date' = col_date("%m/%d/%Y"),
  'Ship Mode' =  col_factor(levels = c("Same Day", "First Class", "Second Class", "Standard Class"), ordered = TRUE),
  Segment = col_factor(levels = c("Consumer", "Corporate", "Home Office")),
  'Postal Code' = "i",
  Region = col_factor(levels = c("South", "East", "Central", "West")),
  Category = col_factor(levels = c("Furniture", "Technology", "Office Supplies")),
  'Sub-Category' = col_factor(levels = c("Bookcases", "Chairs", "Tables", "Furnishings", "Phones", "Accessories", "Copiers", "Machines", "Binders", "Art", "Appliances", "Labels", "Storage", "Supplies", "Paper", "Fasteners", "Envelopes")),
  Quantity = "i"
))
spec(aaa)
subset <- tail(aaa, n=10)
m <- as.matrix(subset)

struct <- c("is.character"  = is.character(m),
  "is.numeric" = is.numeric(m),
  "is.integer"  = is.integer(m),
  "is.factor" = is.factor(m),
  "is.logical" = is.logical(m))

print(struct)
#it is a character matrix as it mixed with character vector.

# correct data type, apply proper type conversions. 
# ● Check the levels of factor variables, rename/rearrange them if required. 
# ● Provide the R codes with outputs and explain everything that you do in this step. 



# Step 6 ------------------------------------------------------------------



num_vector <- c(1:10)
num_vector
seq_vector <- seq.int(1, 20, by=2)
seq_vector
class(num_vector)
char_vector <- c("a", "b", "c", "d", "f", "g", "h", "i", "j", "k")
char_vector
class(char_vector)

mat <- cbind(seq_vector, char_vector)
mat
is.numeric(mat)
is.character(mat)


df1 <- data.frame (col1 = 1:3,
                   col2 = c ("credit", "debit", "Paypal"),
                   col3 = c (TRUE, FALSE, TRUE),
                   col4 = c (25.5, 44.2, 54.9))