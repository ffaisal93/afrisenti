import glob
import os
import random
import re
import sys
# import emoji

def clean_tweet(tweet):
    # remove the @user from the tweet
    tweet = tweet.replace("@user", "")

    # remove the urls from the tweet
    tweet = re.sub(r"http\S+", "", tweet)

    # remove the multiple consecutive punctuations from the tweet
    tweet = re.sub(r"([#@$%^&*()-+_!?.~':;:,]){2,}", r"\1", tweet)

    # remove mulitple consecutive " from the tweet
    tweet = re.sub(r"\"{2,}", "\"", tweet)
    
    # remove the concurrences of the same character (e.g. "hellooooo" to "helloo")
    tweet = re.sub(r"(\w)\1{2,}", r"\1\1", tweet)

    # remove "RT : " from the tweet
    tweet = re.sub(r"RT : ", "", tweet)

    # remove "RT " from the tweet if it is at the beginning of the tweet
    tweet = re.sub(r"^RT ", "", tweet)

    # remove " RT " from the tweet if it is in the middle of the tweet
    tweet = re.sub(r" RT ", " ", tweet)

    # remove RT ":  from the tweet
    tweet = re.sub(r"RT :\"", "", tweet)


    # remove the hashtags from the tweet
    # tweet = re.sub(r"#\S+", "", tweet)

    # remove the numbers from the tweet
    # tweet = re.sub(r"\d+", "", tweet)

    # change emojis from the tweet to text
    # tweet = emoji.demojize(tweet) 

    # remove the extra spaces from the tweet
    tweet = re.sub(r"\s+", " ", tweet)

    # remove the leading and trailing spaces from the tweet
    tweet = tweet.strip()

    return tweet


# process each train and dev file in the data folder and save the processed data in the processed folder
def process_data(input_folder, output_folder):
    # get statistics about the data
    total_tweets = 0
    clean_tweets = 0

    for file in glob.glob(os.path.join(input_folder, "*.tsv")):
        # print("Processing file: ", os.path.basename(file))

        with open(file, "r", encoding="utf-8") as f:
            
            lines = f.readlines()
            # skip first line
            lines = lines[1:]
            processed_lines = []

            # if the file is train.tsv, then the first column is the label
            # if "train" in file:
            for line in lines:
                total_tweets += 1

                try:
                    tweet, label = line.split("\t")
                except:
                    print("Error in line: ", line)
                    print("File: ", file)
                    continue

                tweet = clean_tweet(tweet)

                if tweet != "" and tweet != " " and tweet != "\t":
                    processed_lines.append(f"{tweet}\t{label}")
                    clean_tweets += 1
                else:
                    print("Empty tweet: ", line)

            # if the file is dev.tsv, then the first column is the id
            # else:
            #     for line in lines:
                    
                    
            #         total_tweets += 1

            #         try:
            #             id, tweet = line.split("\t")
            #         except:
            #             print("Error in line: ", line)
            #             print("File: ", file)
            #             continue
            #         tweet = clean_tweet(tweet) + "\n"

            #         if tweet != "" and tweet != " " and tweet != "\t":
            #             processed_lines.append(f"{id}\t{tweet}")
            #             clean_tweets += 1

        # save the processed data in the processed folder
        with open(os.path.join(output_folder, os.path.basename(file)), "w", encoding="utf-8") as f:
  #          if "train" in file:
            f.write("tweet\tlabel\n")
            # else:
            #     f.write("id\ttweet\n")
            f.write("".join(processed_lines))

        print(f"{os.path.basename(file)} has {total_tweets} total tweets")
        print("Clean tweets: ", clean_tweets)
        print("*" * 50)

def split_train_data_with_labels(train_file_folder, output_split_folder):
    for file in glob.glob(os.path.join(train_file_folder, "*.tsv")):
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # skip first line
            lines = lines[1:]

            # shuffle the lines
            random.shuffle(lines)

            # split the lines into train and dev
            train_lines = lines[:int(len(lines) * 0.8)]
            dev_lines = lines[int(len(lines) * 0.8):]

            # save the train and test data in the with_labels folder
            # get the file name without the extension
            file_name = os.path.basename(file).split(".")[0].split("_")[0]
            train_file_folder = os.path.join(output_split_folder, "train")
            dev_file_folder = os.path.join(output_split_folder, "dev")

            if not os.path.exists(train_file_folder):
                os.makedirs(train_file_folder)
            if not os.path.exists(dev_file_folder):
                os.makedirs(dev_file_folder)

            with open(os.path.join(train_file_folder, f"{file_name}_train.tsv"), "w", encoding="utf-8") as f:
                f.write("tweet\tlabel\n")
                f.write("".join(train_lines))
                print("Processed train file: ", os.path.basename(file))
                print("Train data size: ", len(train_lines))

            with open(os.path.join(dev_file_folder, f"{file_name}_test.tsv"), "w", encoding="utf-8") as f:
                f.write("tweet\tlabel\n")
                f.write("".join(dev_lines))
                print("Processed test file: ", os.path.basename(file))
                print("Test data size: ", len(dev_lines))
                print("*" * 50)

def main(input_data_folder, output_data_folder):


    for folder in ["train", "dev", "test"]:

        input_folder = os.path.join(input_data_folder, folder)
        output_folder = os.path.join(output_data_folder, folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        process_data(input_folder, output_folder)

    #split the train data into train and dev
    # split_labeled_folder = os.path.join(input_data_folder, "fully_processed","with_labels")
    # if not os.path.exists(split_labeled_folder):
    #     os.makedirs(split_labeled_folder)
    # split_train_data_with_labels(os.path.join(input_data_folder, "fully_processed", "train"), split_labeled_folder)


if __name__ == '__main__':
       # help message
    # if len(sys.argv) != 3:
    #     print("Usage: python data_processing.py input_data_folder output_data_folder")
    #     print("Note: This script is for SubtaskA. The input data folders should contain train, dev, and test data")
    #     print("Example: python tfidf.py input/data/folder output/data/folder")
    #     exit()

    # # get command line arguments for file path and number of top words
    # input_data_folder = sys.argv[1]
    # output_data_folder = int(sys.argv[2])
 
    #main(input_data_folder, output_data_folder)
    main("/scratch/rxie/afrisenti/SubtaskA/processed_data/with_labels","/scratch/rxie/afrisenti/data/SubtaskA/processed")