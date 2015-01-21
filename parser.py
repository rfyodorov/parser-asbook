#!/usr/bin/python
# -*- coding: utf-8 -*-
import lxml.html as html
import urllib, json

def getPlaylist(book_link):
    # Format string - http://asbook.net/abooks/detectives/6910-otravlenie-v-shutku-dzhon-dikson-karr.html
    digital_code = filter(str.isdigit, book_link)
    str_pl = "http://asbook.net/pll/" + str(digital_code) + "/1/2/"
    return str_pl


def parsePlaylist(playlist_url):
    response = urllib.urlopen(playlist_url);
    #html = response.read()
    data = json.load(response)
    #pprint(data)
    # Format json - dict[ list{  dict[ comment, file] }  ]
    clear_playlist = {}

    for item in data['playlist']:
        track_name = item['comment']
        track_url = item['file']
        #print '"%s", %s' % (track_name, track_url)
        clear_playlist[track_name] = track_url
        #print clear_playlist.items()

    return clear_playlist

def print_header():
    page = ('<!DOCTYPE html>\n'
            '<html>\n'
            '   <head>\n'
            '   <meta charset="utf-8">\n'
            '   <title>test</title>\n'
            '   <link rel="stylesheet" href="css/style.css" type="text/css">\n'
            '   </head>\n'
            '<body>\n'
            '<div class="allpage">\n'
            '<div class="books_block">\n'
            )
    return page


def print_footer(count_download_button_id):
    page = '</div>\n</div>\n'

    for count in range(1, count_download_button_id):
        page += ('<script src="js/multi-download.js"></script>\n'
            '<script>\n'
            'document.querySelector(\'#download-btn' + str(count) + '\').addEventListener(\'click\', function (e) {\n'
            '   var files = e.target.dataset.files.split(\' \');\n'
            '    multiDownload(files);\n'
            '});\n'
            '</script>\n')
    page += ('</body>\n'
            '</html>\n')
    return page

def getPage(page_number):
    main_domain = 'http://asbook.net'
    page = html.parse('%s/page/%s/' % (main_domain, page_number))

    books_list = page.getroot().find_class('b-showshort')
    #print "Numbers of books on page: %s" % len(books_list)

    page = ""
    page += print_header()

    #if (0 != 1):
    #    div_book = books_list[0].getchildren()

    count_download_button_id = 1
    for book in books_list:
        div_book = book.getchildren()
        #print "Count of div in one book %s" % len(div_book)

        # Get Title
        ahref = div_book[1].find_class('b-showshort__title_link')
        book_title = ahref[0].text_content()
        book_url = ahref[0].get('href')

        # Get playlist
        book_link = ahref[0].get('href')
        playlist_url = getPlaylist(book_link)

        # Parse playlist
        current_playlist = {}
        current_playlist = parsePlaylist(playlist_url)

        # Get cover
        aimg = div_book[0].find_class('b-showshort__cover_image')
        cover_url = aimg[0].get('src')

        # Get time
        atime = div_book[2].find_class('table b-showshort__data')
        book_timerec = atime.pop().getchildren().pop().getchildren().pop(1).getchildren().pop().getchildren().pop(0).getchildren().pop(1).text_content()

        # ----
        # create html
        page += ('<div class="book_main">\n'
                ' \n'
                '<div class="book_cover">\n'
                '   <img src=' + cover_url + '>\n'
                '</div>\n'
                ' \n'
                '<div class="book_title">\n'
                '   <a class="book_link" href=' + book_url + ' target=_blank>' + book_title +'</a>\n'
                '</div>\n'
                ' \n'
                '<div class="book_time">\n'
                '   Time: ' + book_timerec + ' \n'
                '</div>\n')

        page += ('<div class="book_playlist">\n'
                '<button id="download-btn' + str(count_download_button_id) + '" class="btn btn-primary btn-lg" data-files=\'')
 
        cpl_sort = current_playlist.keys()
        cpl_sort.sort()
        for name in cpl_sort:
            page += current_playlist[name] + ' '
        page = page[:-1]

        #for name, url in current_playlist.items():
        #    page += '    <a href=' + url + '> ' + name + ' <a><br>\n'

        page += ('\'>Download all mp3</button></br>\n'
                '</div>\n'
                ' \n'
                '</div>\n')

        count_download_button_id += 1

    
    page += ('</div>\n'
            '<div class="navigate">\n')

    if int(page_number) > 1:
        page += ' <a class="navigate" href="/' + str(int(page_number)-1) + '"> ' + str(int(page_number)-1) + ' < </a> ' + str(page_number)
    else:
        page += str(page_number)

    page += (' <a class="navigate" href="/' + str(int(page_number)+1) + '">> ' + str(int(page_number)+1) + '</a>'
            '</div>\n')

    page += print_footer(count_download_button_id)
    page_complete = page.encode("utf-8")
    return page_complete
