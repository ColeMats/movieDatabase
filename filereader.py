import csv

with open("title.basics.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    num = 0
    nullstr = '\\\\N'
    with open('movies.csv', 'w') as f:
        for line in tsv_file:
            if 'N' in line[5]:
                print('skipped')
            elif line[1] == 'movie' and int(line[5]) > 1980:
                line.pop(3)
                line.pop(3)
                line.pop(4)
                line.pop(4)
                line.pop(1)
                line.pop(3)
                line[0] = f"{line[0]}"
                line[1] = f"{line[1]}"
                line[2] = f"{line[2]}"
                print(line)
                csvwriter = csv.writer(f)
                csvwriter.writerow(line)
                print("Line: " + str(line) + ' was written')
            num += 1
        print(num)
print('Done')
