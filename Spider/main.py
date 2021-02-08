import os
import pandas as pd
import glob
import re
import argparse
from make_spiders import make_spider_projects
import Preprocessing


def make_dataset(append):
    if append:
        if os.path.exists('../Data/unpreprocessed_dataset.csv'):
            final_csv_file = pd.read_csv('../Data/unpreprocessed_dataset.csv')
        else:
            final_csv_file = pd.DataFrame(columns=['body', 'tag', 'title'])
    else:
        final_csv_file = pd.DataFrame(columns=['body', 'tag', 'title'])
    csv_file_path = '/body_tag_title.csv'
    print('--- Start to merge datafames ---')
    for file_name in glob.glob('spider_*'):
        print('----- ', file_name)
        matrix_main = pd.read_csv('./' + file_name + csv_file_path)
        for i in range(len(matrix_main)):
            matrix_main['tag'][i] = re.sub('active|,\'active\'|,\'active\',|\'active\',|page=2', '',
                                           matrix_main['tag'][i])
            if matrix_main['tag'][i] == '':
                matrix_main['tag'][i] = None
        matrix_main = matrix_main.dropna(axis=0, inplace=False).reset_index(drop=True)
        counter = 0
        max_counter = 5
        rows_per_iter = 1500
        first_len = len(matrix_main)
        while True:
            counter += 1
            print('counter: ', counter)
            temp_matrix = pd.DataFrame(columns=['body', 'tag', 'title'])
            pre_len = len(matrix_main)
            for i in range(0, 1 + len(matrix_main) // rows_per_iter):
                loop_matrix = matrix_main.loc[
                              i * rows_per_iter:min(first_len - i * rows_per_iter, (i + 1) * rows_per_iter), :]
                loop_matrix = loop_matrix.dropna(axis=0).reset_index(drop=True)
                for title in loop_matrix['title']:
                    indexes = loop_matrix.loc[loop_matrix['title'] == title].index
                    if len(indexes) > 0:
                        tags = set(loop_matrix.loc[loop_matrix['title'] == title]['tag'])
                        tags = re.sub('\{|\}', '', str(tags))
                        tags = re.sub('[\']+|[\"]+', '\'', tags)
                        loop_matrix.at[indexes[0], 'title'] = str(title).strip()
                        loop_matrix.at[indexes[0], 'tag'] = tags
                        loop_matrix = loop_matrix.drop(axis=0, index=indexes[1:]).reset_index(drop=True)
                temp_matrix = temp_matrix.append(loop_matrix)
                print('  - loop:', len(loop_matrix))
            if len(temp_matrix) > 0:
                matrix_main = temp_matrix.sample(frac=1).reset_index(drop=True)
            print(' - per count: ', len(matrix_main))
            if (counter > max_counter) or (len(matrix_main) == pre_len):
                break
        final_csv_file = final_csv_file.append(matrix_main)

    final_csv_file.loc[:, ['body', 'tag']].to_csv('../Data/unpreprocessed_dataset.csv', index=False)
    print(len(final_csv_file), 'texts was scripted, Done !')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--re_crawl_all',metavar='re_crawl_all',
                        help='some sites are crawled yet, True it if you want to repeat',default=False)
    parser.add_argument('--rebuild_dataset', metavar='rebuild_dataset',
                        help='collect and clean data, from all scripted sites.', default=False)
    parser.add_argument('--append_dataset', metavar='rebuild_dataset',
                        help='True it if you want append datas to dataset', default=True)
    parser.add_argument('--preprocess', metavar='preprocess',
                        help='preprocess the un-preprocessed dataset',default=False)

    args = parser.parse_args()
    re_crawl_all = args.recrawl_all
    rebuild_dataset = args.rebuild_dataset
    append_dataset = args.append_dataset
    preprocess = args.preprocess

    sites_dict = {'virgool': 'virgool.io/tag/', 'sokanacademy': 'sokanacademy.com/search?q='
        , '7learn': '7learn.com/archive?s=', 'roocket': 'roocket.ir/search?search=',
        'zerotohero': 'zerotohero.ir/?s='}

    make_spider_projects(sites_dict)

    spiders = glob.glob('spider_*')
    for i in range(len(spiders)):

        if (not os.path.exists('./' + spiders[i] + '/body_tag_title.csv')) or re_crawl_all:
            # part 1 :
            print('- 2 ---- starting to scrap ' + spiders[i])
            os.chdir('./' + spiders[i])
            spider = 's_1_' + spiders[i].split('_')[-1]
            os.system('scrapy crawl ' + spider + ' -o body_tag_title.csv')
            os.chdir('..')

    # part 2 : link each founded links in any search result to the tags
    if (not os.path.exists('./Data/unpreprocessed_dataset.csv')) or rebuild_dataset:
        make_dataset(append=append_dataset)

    if preprocess:
        Preprocessing.preprocess_hazm()

    print(f'recrawl_all:{re_crawl_all} \nrebuild_dataset:{rebuild_dataset}',
          f'preprocess:{preprocess} \nFinished!')
