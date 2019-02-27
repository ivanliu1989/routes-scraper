Sys.getlocale()
Sys.setlocale(category = "LC_ALL", locale = "chs")
library(data.table)

dat = fread("./1_ad310000_poi110000.csv", encoding = 'UTF-8')
head(dat)
View(dat)
