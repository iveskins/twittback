import json

import twittback.client.twitter_client


with_urls = r"""
{
    "entities": {
      "urls": [
        {
          "url": "https://t.co/d0FHGsSYqE",
          "expanded_url": "https://dmerej.info/blog/pages/links/",
          "display_url": "dmerej.info/blog/pages/lin\u2026",
          "indices": [
            18,
            41
          ]
        },
        {
          "url": "https://t.co/zpSMb6fPLz",
          "expanded_url": "https://hackernoon.com/12-signs-youre-working-in-a-feature-factory-44a5b938d6a2",
          "display_url": "hackernoon.com/12-signs-youre\u2026",
          "indices": [
            88,
            111
          ]
        }
      ],
    "media": []
    },
    "text": "New link added to https://t.co/d0FHGsSYqE\n12 Signs You\u2019re Working in a Feature Factory: https://t.co/zpSMb6fPLz"
}
"""

with_image = r"""
{
  "entities": {
    "urls": [],
    "media": [
      {
        "indices": [
          64,
          87
        ],
        "media_url_https": "https://pbs.twimg.com/media/Co4H3jYWEAAnzFg.jpg"
      }
    ]
  },
  "text": "Is #XKCD's CSS broken or is it just me ?\n(Using firefox 47.0.1) https://t.co/FbpnFuBouY"
}
"""

with_escaped_html = """
{
  "entities": {
    "urls": [],
    "media": []
  },
  "text": "Use git grep foo &lt;branch&gt; -- &lt;path&gt;"
}
"""


def test_fix_urls():
    json_data = json.loads(with_urls)
    text = json_data["text"]
    markdown = twittback.client.twitter_client.to_markdown(text, json_data)
    assert markdown == """New link added to [dmerej.info/blog/pages/lin…](https://dmerej.info/blog/pages/links/)
12 Signs You’re Working in a Feature Factory: [hackernoon.com/12-signs-youre…](https://hackernoon.com/12-signs-youre-working-in-a-feature-factory-44a5b938d6a2)"""


def test_fix_media():
    json_data = json.loads(with_image)
    text = json_data["text"]
    markdown = twittback.client.twitter_client.to_markdown(text, json_data)
    assert markdown == """Is #XKCD's CSS broken or is it just me ?
(Using firefox 47.0.1) ![image](https://pbs.twimg.com/media/Co4H3jYWEAAnzFg.jpg)"""



def test_unescape_html():
    json_data = json.loads(with_escaped_html)
    text = json_data["text"]
    markdown = twittback.client.twitter_client.to_markdown(text, json_data)
    assert markdown == "Use git grep foo <branch> -- <path>"