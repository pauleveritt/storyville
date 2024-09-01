# from viewdom.render import html
#
# import storytime
# from . import ComponentsListing, ComponentListing, StoryListing
#
# story0 = StoryInfo(
#     dotted_path='some.dotted.path',
#     story_id=1,
#     title='Some Story 1',
#     vdom=html('<div>Some VDOM</div>'),
#     html='<div>Some HTML</div>',
# )
#
#
# def these_stories() -> Stories:
#     assert (ComponentsListing, ComponentListing, StoryListing)
#     return Stories(
#         Story(
#             target=StoryListing,
#             props=dict(
#                 dotted_path='some_dotted_path',
#                 story_id=99,
#                 story_title='Some Story Title'
#             ),
#         ),
#         Story(
#             target=ComponentListing,
#             props=dict(
#                 component_info=ComponentInfo(
#                     dotted_path='some_dotted_path',
#                     stories=[story0],
#                     title='Some Component Title',
#                 )
#             )
#         ),
#         Story(
#             template=html('<{ComponentsListing} />'),
#         ),
#         plugins=(storytime,),
#     )
