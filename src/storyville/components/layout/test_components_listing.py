# from storyville.components.sections_listing.stories import these_stories
#
#
# def test_components_listing():
#     stories = these_stories().items
#
#     assert 'li' == stories[0].vdom.tag
#     link = stories[0].vdom.children[0]
#     assert 'some_dotted_path-99.html' == link.props['href']
#     assert 'Some Story Title' == link.children[0]
#
#     s1 = stories[1]
#     assert 'li' == s1.vdom.tag
#     assert 'a' == s1.vdom.children[0].tag
#     assert 'some_dotted_path.html' == s1.vdom.children[0].props['href']
#     assert 'some_dotted_path' == s1.vdom.children[0].children[0]
#     assert 'ul' == s1.vdom.children[1].tag
#     links = s1.html.select('ul.stories li a')
#     assert 1 == len(links)
#     assert 'some.dotted.path-1.html' == links[0].attrs['href']
#
#     h2 = stories[0].html
#     links = h2.select('li a')
#     assert 1 == len(links)
#     assert 'Some Story Title' == links[0].text
#     assert 'some_dotted_path-99.html' == links[0].attrs['href']
