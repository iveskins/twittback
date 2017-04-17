import arrow


class HTMLPresenter:

    @classmethod
    def gen_index(cls, start_timestamp, end_timestamp):

        date_format = "%Y %b %d"
        start_date = arrow.get(start_timestamp).strftime(date_format)
        end_date = arrow.get(end_timestamp).strftime(date_format)
        res = f"""
<h1>Welcome to TwittBack</h1>

<h2>All tweets</h2>

<p>
Listing tweets from {start_date} to {end_date}
</p>
"""
        return res
