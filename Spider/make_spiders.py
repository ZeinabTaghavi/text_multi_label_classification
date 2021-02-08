import os
def make_spider_projects(sites_dict):
    i = 0
    for name in sites_dict:
        file_path ='spider_1_'+str(i)+'/spider_1_'+str(i)+'/spiders/s_1_'+str(i)+'.py'
        if not os.path.exists(file_path):
            print(name)
            os.system('scrapy startproject spider_1_'+str(i))
            os.chdir('spider_1_'+str(i))
            os.system('scrapy genspider s_1_'+str(i)+' '+sites_dict[name])
            file = open('spider_1_'+str(i)+'/settings.py','a')
            file.write('''DOWNLOADER_MIDDLEWARES = {
                    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
                }''')
            os.chdir('..')
            with open(file_path,'a'):
                os.utime(file_path, None)
            print('----------- '+name+' spider created ------------')
        else :
            print('----------- '+name+' spider was created before ------------')
        i +=1


if __name__ == "__main__":
    sites_dict = {'virgool': 'virgool.io/tag/', 'sokanacademy': 'sokanacademy.com/search?q='
                  , '7learn':'7learn.com/archive?s=','roocket':'roocket.ir/search?search=',
                  'zerotohero':'zerotohero.ir/?s='}
    make_spider_projects(sites_dict)