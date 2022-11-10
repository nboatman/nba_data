Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import requests
>>> from lxml import html
>>> 
>>> 
>>> url = 'https://www.basketball-reference.com/boxscores/202211060LAC.html'
>>> r = requests.get(url=url, allow_redirects=False)
>>> h = html.fromstring(r.content)
>>> h1 = h.xpath('//div[@id="div_line_score"]')
>>> h1.content
Traceback (most recent call last):
  File "<pyshell#8>", line 1, in <module>
    h1.content
AttributeError: 'list' object has no attribute 'content'
>>> len(h1)
0
>>> h1
[]
>>> help(h)

>>> h.content
Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    h.content
AttributeError: 'HtmlElement' object has no attribute 'content'
>>> h.text_content
<bound method HtmlMixin.text_content of <Element html at 0x1aa928c92c0>>
>>> h.text_content()

>>> h1 = h.xpath('.//div[@id="div_line_score"]')
>>> len(h1)
0
>>> comments = [child for child in h.iter() if isinstance(child, lxml.HtmlComment)]
Traceback (most recent call last):
  File "<pyshell#17>", line 1, in <module>
    comments = [child for child in h.iter() if isinstance(child, lxml.HtmlComment)]
  File "<pyshell#17>", line 1, in <listcomp>
    comments = [child for child in h.iter() if isinstance(child, lxml.HtmlComment)]
NameError: name 'lxml' is not defined
>>> from lmxl.html import HtmlComment
Traceback (most recent call last):
  File "<pyshell#18>", line 1, in <module>
    from lmxl.html import HtmlComment
ModuleNotFoundError: No module named 'lmxl'
>>> from lxml.html import HtmlComment
>>> comments = [child for child in h.iter() if isinstance(child, HtmlComment)]
>>> len(comments)
73
>>> comments[0]
<!-- Quantcast Choice. Consent Manager Tag v2.0 (for TCF 2.0) -->
>>> comments[1]
<!-- End Quantcast Choice. Consent Manager Tag v2.0 (for TCF 2.0) -->
>>> comments[63]
<!-- /div.#fs_fs_rails_left -->
>>> comments[25]
<!-- div#fs_fs_general_header  -->
>>> comments

>>> for x in comments[:15]
SyntaxError: invalid syntax
>>> for x in comments[:15]:
	print(x)

	
<!-- Quantcast Choice. Consent Manager Tag v2.0 (for TCF 2.0) -->
<!-- End Quantcast Choice. Consent Manager Tag v2.0 (for TCF 2.0) -->
<!-- Google Tag Manager -->
<!-- End Google Tag Manager -->
<!-- include:start ="/inc/klecko_header_bbr.html_f" -->
<!-- no:cookie fast load the css.           -->
<!-- CSS start -->
<!-- CSS END -->
<!-- JS START -->
<!-- JS END -->
<!-- include:end ="/inc/klecko_header_bbr.html_f" -->
<!-- HeaderSeoSocial -->
<!-- HeaderSeoSocial:END -->
<!-- tiles, touch, favicons -->
<!--[if IE]>
    <link rel="shortcut icon"                                href="https://cdn.ssref.net/req/202210281/favicons/bbr/favicon.ico"><![endif]-->
>>> for x in comments[15:30]:
	print(x)

	

>>> for x in comments[30:45]:
	print(x)

	
<!-- div#fs_fs_btf_3  -->
<!-- /div.#fs_fs_btf_3 -->
<!--

<div class="table_container" id="div_line_score">
    
    <table class="suppress_all stats_table" id="line_score" data-cols-to-freeze="0">
    <caption>Line Score Table</caption>
    

   <colgroup><col><col><col><col><col><col></colgroup>
   <thead>

      
      <tr class="over_header">
         <th aria-label="" data-stat="header_tmp" colspan="6" class=" over_header center" >Scoring</th>
      </tr>
            
      <tr>
         <th aria-label="&nbsp;" data-stat="team" scope="col" class=" poptip center" data-over-header="Scoring" >&nbsp;</th>
         <th aria-label="1" data-stat="1" scope="col" class=" poptip center" data-over-header="Scoring" >1</th>
         <th aria-label="2" data-stat="2" scope="col" class=" poptip center" data-over-header="Scoring" >2</th>
         <th aria-label="3" data-stat="3" scope="col" class=" poptip center" data-over-header="Scoring" >3</th>
         <th aria-label="4" data-stat="4" scope="col" class=" poptip center" data-over-header="Scoring" >4</th>
         <th aria-label="T" data-stat="T" scope="col" class=" poptip center" data-over-header="Scoring" >T</th>
      </tr>
      </thead>
<tbody><tr ><th scope="row" class="center " data-stat="team" ><a href='/teams/UTA/2023.html'>UTA</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >34</td><td class="center " data-stat="3" >21</td><td class="center " data-stat="4" >26</td><td class="center " data-stat="T" ><strong>110</strong></td></tr>
<tr ><th scope="row" class="center " data-stat="team" ><a href='/teams/LAC/2023.html'>LAC</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >27</td><td class="center " data-stat="3" >29</td><td class="center " data-stat="4" >17</td><td class="center " data-stat="T" ><strong>102</strong></td></tr>

</table>


</div>
-->

<!-- global.nonempty_tables_num: 3, table_count: 3 -->
<!-- no Local/Partials/NoteBottom.tt2 -->
<!-- div#content -->
<!-- div#footer_header -->
<!-- Begin:In the News -->
<!-- End:In the News -->
<!-- Begin:All-Time Greats -->
<!-- End:All-Time Greats -->
<!-- Begin:Active Greats -->
<!-- End:Active Greats -->
<!-- Begin:Teams -->
>>> comments[37]
<!-- div#footer_header -->
>>> comments[38]
<!-- Begin:In the News -->
>>> comments[44]
<!-- Begin:Teams -->
>>> comments[40]
<!-- Begin:All-Time Greats -->
>>> comments[36]
<!-- div#content -->
>>> comments[33]

>>> comments[32]
<!--

<div class="table_container" id="div_line_score">
    
    <table class="suppress_all stats_table" id="line_score" data-cols-to-freeze="0">
    <caption>Line Score Table</caption>
    

   <colgroup><col><col><col><col><col><col></colgroup>
   <thead>

      
      <tr class="over_header">
         <th aria-label="" data-stat="header_tmp" colspan="6" class=" over_header center" >Scoring</th>
      </tr>
            
      <tr>
         <th aria-label="&nbsp;" data-stat="team" scope="col" class=" poptip center" data-over-header="Scoring" >&nbsp;</th>
         <th aria-label="1" data-stat="1" scope="col" class=" poptip center" data-over-header="Scoring" >1</th>
         <th aria-label="2" data-stat="2" scope="col" class=" poptip center" data-over-header="Scoring" >2</th>
         <th aria-label="3" data-stat="3" scope="col" class=" poptip center" data-over-header="Scoring" >3</th>
         <th aria-label="4" data-stat="4" scope="col" class=" poptip center" data-over-header="Scoring" >4</th>
         <th aria-label="T" data-stat="T" scope="col" class=" poptip center" data-over-header="Scoring" >T</th>
      </tr>
      </thead>
<tbody><tr ><th scope="row" class="center " data-stat="team" ><a href='/teams/UTA/2023.html'>UTA</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >34</td><td class="center " data-stat="3" >21</td><td class="center " data-stat="4" >26</td><td class="center " data-stat="T" ><strong>110</strong></td></tr>
<tr ><th scope="row" class="center " data-stat="team" ><a href='/teams/LAC/2023.html'>LAC</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >27</td><td class="center " data-stat="3" >29</td><td class="center " data-stat="4" >17</td><td class="center " data-stat="T" ><strong>102</strong></td></tr>

</table>


</div>
-->
>>> c = _
>>> type(c)
<class 'lxml.html.HtmlComment'>
>>> help(c)

>>> c.text
'\n\n<div class="table_container" id="div_line_score">\n    \n    <table class="suppress_all stats_table" id="line_score" data-cols-to-freeze="0">\n    <caption>Line Score Table</caption>\n    \n\n   <colgroup><col><col><col><col><col><col></colgroup>\n   <thead>\n\n      \n      <tr class="over_header">\n         <th aria-label="" data-stat="header_tmp" colspan="6" class=" over_header center" >Scoring</th>\n      </tr>\n            \n      <tr>\n         <th aria-label="&nbsp;" data-stat="team" scope="col" class=" poptip center" data-over-header="Scoring" >&nbsp;</th>\n         <th aria-label="1" data-stat="1" scope="col" class=" poptip center" data-over-header="Scoring" >1</th>\n         <th aria-label="2" data-stat="2" scope="col" class=" poptip center" data-over-header="Scoring" >2</th>\n         <th aria-label="3" data-stat="3" scope="col" class=" poptip center" data-over-header="Scoring" >3</th>\n         <th aria-label="4" data-stat="4" scope="col" class=" poptip center" data-over-header="Scoring" >4</th>\n         <th aria-label="T" data-stat="T" scope="col" class=" poptip center" data-over-header="Scoring" >T</th>\n      </tr>\n      </thead>\n<tbody><tr ><th scope="row" class="center " data-stat="team" ><a href=\'/teams/UTA/2023.html\'>UTA</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >34</td><td class="center " data-stat="3" >21</td><td class="center " data-stat="4" >26</td><td class="center " data-stat="T" ><strong>110</strong></td></tr>\n<tr ><th scope="row" class="center " data-stat="team" ><a href=\'/teams/LAC/2023.html\'>LAC</a></th><td class="center " data-stat="1" >29</td><td class="center " data-stat="2" >27</td><td class="center " data-stat="3" >29</td><td class="center " data-stat="4" >17</td><td class="center " data-stat="T" ><strong>102</strong></td></tr>\n\n</table>\n\n\n</div>\n'
>>> help(h)

>>> fragment_fromstring(c)
Traceback (most recent call last):
  File "<pyshell#49>", line 1, in <module>
    fragment_fromstring(c)
NameError: name 'fragment_fromstring' is not defined
>>> html.fragment_fromstring(c)
Traceback (most recent call last):
  File "<pyshell#50>", line 1, in <module>
    html.fragment_fromstring(c)
  File "C:\Users\boatm\AppData\Local\Programs\Python\Python39\lib\site-packages\lxml\html\__init__.py", line 829, in fragment_fromstring
    elements = fragments_fromstring(
  File "C:\Users\boatm\AppData\Local\Programs\Python\Python39\lib\site-packages\lxml\html\__init__.py", line 790, in fragments_fromstring
    if not _looks_like_full_html_unicode(html):
TypeError: expected string or bytes-like object
>>> html.fragments_fromstring(c)
Traceback (most recent call last):
  File "<pyshell#51>", line 1, in <module>
    html.fragments_fromstring(c)
  File "C:\Users\boatm\AppData\Local\Programs\Python\Python39\lib\site-packages\lxml\html\__init__.py", line 790, in fragments_fromstring
    if not _looks_like_full_html_unicode(html):
TypeError: expected string or bytes-like object
>>> html.fragment_fromstring(c.text)
<Element div at 0x1aa93156630>
>>> z = _
>>> len(z)
1
>>> z[0]
<Element table at 0x1aa931564f0>
>>> z[0].text_content()
'\n    Line Score Table\n    \n\n   \n   \n\n      \n      \n         Scoring\n      \n            \n      \n         \xa0\n         1\n         2\n         3\n         4\n         T\n      \n      \nUTA29342126110\nLAC29272917102\n\n'
>>> z[0].xpath('//thead')
[<Element thead at 0x1aa93156680>]
>>> z1 = _
>>> len(z1)
1
>>> z1[0].text_content()
'\n\n      \n      \n         Scoring\n      \n            \n      \n         \xa0\n         1\n         2\n         3\n         4\n         T\n      \n      '
>>> z2 = z1.xpath('//tr')
Traceback (most recent call last):
  File "<pyshell#61>", line 1, in <module>
    z2 = z1.xpath('//tr')
AttributeError: 'list' object has no attribute 'xpath'
>>> z2 = z1[0].xpath('//tr')
>>> len(z2)
4
>>> z2[0].text_content()
'\n         Scoring\n      '
>>> z2[1].text_content()
'\n         \xa0\n         1\n         2\n         3\n         4\n         T\n      '
>>> z2[2].text_content()
'UTA29342126110'
>>> z[0].xpath('//tbody')[0]
<Element tbody at 0x1aa93156bd0>
>>> z[0].xpath('//tbody')[0].text.content()
Traceback (most recent call last):
  File "<pyshell#68>", line 1, in <module>
    z[0].xpath('//tbody')[0].text.content()
AttributeError: 'NoneType' object has no attribute 'content'
>>> len(z[0].xpath('//tbody'))
1
>>> type(z[0].xpath('//tbody'))
<class 'list'>
>>> type(z[0].xpath('//tbody')[0])
<class 'lxml.html.HtmlElement'>
>>> z[0].xpath('//tbody')[0].text_content()
'UTA29342126110\nLAC29272917102\n\n'
>>> 