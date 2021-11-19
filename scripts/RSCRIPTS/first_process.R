library('argparse')
parser <- ArgumentParser(description='Input, and output filepaths')
parser$add_argument('--input_file_path', help='The input file path')
parser$add_argument('--output_file_path', help='The output file path')
args <- parser$parse_args()

df <- read.csv(file.path(args$input_file_path,"diabetes.csv"))
df['SkinThick_to_BMI'] <- df['TricepsThickness'] / df['BMI']
write.csv(df, file = file.path(args$output_file_path,"preprocessed_diabetes.csv"))
cat("The data frame is exported", "\n")
