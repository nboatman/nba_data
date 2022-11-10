Python 3.9.2 (tags/v3.9.2:1a79785, Feb 19 2021, 13:44:55) [MSC v.1928 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import requests
>>> from lxml import html
>>> from lxml.html import HtmlComment
>>> 
>>> 
>>> url = 'https://www.basketball-reference.com/boxscores/202211060LAC.html'
>>> r = requests.get(url=url, allow_redirects=False)
>>> h = html.fromstring(r.content)
>>> box_score_comments = [element for element in h.iter() if isinstance(element, HtmlComment)]
>>> len(h)
3
>>> h
<Element html at 0x288b9be83b0>
>>> len(box_score_comments)
73
>>> line_score_comments = [element for element in box_score_comments if element.text.contains('id="div_line_score"')]
Traceback (most recent call last):
  File "<pyshell#12>", line 1, in <module>
    line_score_comments = [element for element in box_score_comments if element.text.contains('id="div_line_score"')]
  File "<pyshell#12>", line 1, in <listcomp>
    line_score_comments = [element for element in box_score_comments if element.text.contains('id="div_line_score"')]
AttributeError: 'str' object has no attribute 'contains'
>>> line_score_comments = [element for element in box_score_comments if 'id="div_line_score"' in element.text]
>>> len(line_score_comments)
1
>>> line_score_comments[0]
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
>>> ls = html.fragment_fromstring(line_score_comments[0].text)
>>> ls
<Element div at 0x288b9c2f900>
>>> len(ls)
1
>>> ls.children
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    ls.children
AttributeError: 'HtmlElement' object has no attribute 'children'
>>> ls_head = ls.xpath('//thead')
>>> ls_head
[<Element thead at 0x288b9c2fa90>]
>>> ls_head[0]
<Element thead at 0x288b9c2fa90>
>>> _.text_content()
'\n\n      \n      \n         Scoring\n      \n            \n      \n         \xa0\n         1\n         2\n         3\n         4\n         T\n      \n      '
>>> ls_head_r = ls_head[0].xpath('//tr')
>>> ls_head_r
[<Element tr at 0x288b9c112c0>, <Element tr at 0x288b9c39950>, <Element tr at 0x288b9c39900>, <Element tr at 0x288b9c398b0>]
>>> ls_head_r[-1].text_content()
'LAC29272917102'
>>> ls_head_r = ls_head[0].xpath('/tr')
>>> ls_head_r
[]
>>> ls_head_r = ls_head[0].xpath('./tr')
>>> ls_head_r
[<Element tr at 0x288b9c2f950>, <Element tr at 0x288b9c39a90>]
>>> ls_head_r = ls_head[0].xpath('./tr/th')
>>> ls_head_r
[<Element th at 0x288b9c39860>, <Element th at 0x288b9c39b80>, <Element th at 0x288b9c39950>, <Element th at 0x288b9c39900>, <Element th at 0x288b9c398b0>, <Element th at 0x288b9c39c70>, <Element th at 0x288b9c39a40>]
>>> ls_head_r[-1].text_content()
'T'
>>> ls_head_r = ls_head[0].xpath('./tr/th[@data-over-header="Scoring"')
Traceback (most recent call last):
  File "<pyshell#34>", line 1, in <module>
    ls_head_r = ls_head[0].xpath('./tr/th[@data-over-header="Scoring"')
  File "src\lxml\etree.pyx", line 1599, in lxml.etree._Element.xpath
  File "src\lxml\xpath.pxi", line 305, in lxml.etree.XPathElementEvaluator.__call__
  File "src\lxml\xpath.pxi", line 225, in lxml.etree._XPathEvaluatorBase._handle_result
lxml.etree.XPathEvalError: Invalid predicate
>>> ls_head_r = ls_head[0].xpath('./tr/th[@data-over-header="Scoring"]')
>>> ls_head_r
[<Element th at 0x288b9c39b80>, <Element th at 0x288b9c39950>, <Element th at 0x288b9c39900>, <Element th at 0x288b9c398b0>, <Element th at 0x288b9c39c70>, <Element th at 0x288b9c39a40>]
>>> ls_head_r.content
Traceback (most recent call last):
  File "<pyshell#37>", line 1, in <module>
    ls_head_r.content
AttributeError: 'list' object has no attribute 'content'
>>> ls_head_r.text
Traceback (most recent call last):
  File "<pyshell#38>", line 1, in <module>
    ls_head_r.text
AttributeError: 'list' object has no attribute 'text'
>>> ls_head_r.content.text_content()
Traceback (most recent call last):
  File "<pyshell#39>", line 1, in <module>
    ls_head_r.content.text_content()
AttributeError: 'list' object has no attribute 'content'
>>> ls_head_r[-1]
<Element th at 0x288b9c39a40>
>>> ls_head_r[-1].text
'T'
>>> 