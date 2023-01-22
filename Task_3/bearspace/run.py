#!/usr/bin/python


from scrapy import cmdline

name = 'bearspace'
if __name__ == '__main__':
    command = 'scrapy crawl {0}'.format(name).split()
    cmdline.execute(command)


