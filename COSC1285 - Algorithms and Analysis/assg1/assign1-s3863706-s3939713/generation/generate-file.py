import random
import sys
import numpy as np


def random_to_array(lst_size, full_list):
    try:
        for idx in range(lst_size):
            random_no = random.randrange(200000)
            full_list.append(random_no)
        return full_list
    except ValueError as e:
        print('Incorrect number of arguments.')


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        try:
            list_size = int(args[1])
            if list_size <= 200000:
                arr = []
                arr = random_to_array(list_size, arr)
                while list_size > len(set(arr)):
                    arr = random_to_array(list_size - len(set(arr)), list(set(arr)))
                indices = list(set(arr))
                sample_data = np.loadtxt('../sampleData200k.txt', dtype='str', delimiter="\n")
                extracted_data = np.take(sample_data, indices)

                with open('sampleData-{}.txt'.format(list_size), 'w') as f:
                    for line in extracted_data.tolist():
                        f.write("%s\n" % line)
                f.close()

            else:
                print('Input cannot be larger than 200000.')
        except ValueError as e:
            print('Incorrect number of arguments.')
    else:
        print('Incorrect number of arguments.')