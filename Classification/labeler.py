import csv

def label(text):
    print("Text: \n" + text + "\n")
    label = input("Insert the label: (pos, neg, neu, stop)\n")
    if label == "pos":
        label = "positive"
    elif label == "neg":
        label = "negative"
    elif label == "neu":
        label = "neutral"
    elif label == "stop":
        return -1
    return label

if __name__ == "__main__":
    with open('../data/rawDataset.csv') as csv_file:
        with open('tweets_final_labeled.csv', 'a+') as labeled_csv_file:
            print("Running tweet labeler..")
        with open('tweets_final_labeled.csv','r+') as labeled_csv_file:
            line_to_skip = 0
            csv_reader = csv.reader(labeled_csv_file)
            for line in csv_reader:
                if line != "\n":
                    line_to_skip += 1
            labeled_csv_file.seek(0)
            first_char = labeled_csv_file.read(1)
            with open('tweets_final_labeled.csv', 'a') as labeled_csv_file:
                writer = csv.writer(labeled_csv_file, delimiter=',')
                if not first_char:
                    header = ['Datetime', 'Tweet', 'Id', 'Text', 'Username', 'Label']
                    writer.writerow(header)
                else:
                    labeled_csv_file.seek(0)
                numLine = 0
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if numLine == 0 or numLine < line_to_skip:
                        numLine = numLine + 1
                        continue
                    numLine = numLine + 1
                    result = label(row[2])
                    if result == -1:
                        break
                    row = row + [result]
                    writer.writerow(row)

