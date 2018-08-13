# Load files
baseFile <- read.table("/Users/m006703/Index_Swap/HiSeq4000/HNFC3BBXX/result/filtered_sharedVariantCoverage.txt", header = TRUE)
compareFile <- read.table("/Users/m006703/Index_Swap/HiSeq4000/HNCN5BBXX/result/sharedVariantCoverage.txt", header = TRUE)

# Make new data frame and copy the column names from baseFile
resultFile <- data.frame(matrix(ncol = 36, nrow = 0), stringsAsFactors = FALSE)
colnames(resultFile) <- colnames(baseFile)

# Load the dplyr package to mutate the factor columns to characters
library(dplyr)

# Mutate the factor columns to characters, otherwise the new data frame will look weird
baseFile %>% mutate_if(is.factor, as.character) -> baseFile
compareFile %>% mutate_if(is.factor, as.character) -> compareFile

# Loop through all the positions in base file and if the position is found in compare file, copy the columns
# If not found, make a column with "NA"
for (i in 1:nrow(baseFile)) {
  if (baseFile[i, 1] %in% compareFile[, 1]) {
    cat("Found ", baseFile[i, 1], "\n")
    resultFile[(2*i - 1), ] <- baseFile[i, ]
    resultFile[(2*i), ] <- compareFile[which(compareFile[, 1] == baseFile[i, 1]), ]
  } else {
    cat("Did not find ", baseFile[i, 1], "\n")
    resultFile[(2*i - 1), ] <- baseFile[i, ]
    resultFile[(2*i), ] <- rep("NA")
  }
}

# Save resultFile dataframe
write.table(resultFile, "/Users/m006703/Index_Swap/HiSeq4000/SideB_Base.txt", sep = "\t", row.names = FALSE)