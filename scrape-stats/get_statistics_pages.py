"""Given the address of a landing page, find the addresses of all
linked statistics pages."""

def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser(description='Given the address of a landing page, find the addresses of all linked statistics pages.')
    parser.add_argument('--url', '-u', required=True, help='URL of the landing page having links to statistics pages')
    return parser.parse_args()

def get_statistics_pages(url):
    """
    Arguments
    ---------
    url : str
        URL of the landing page having links to statistics pages

    Returns
    -------
    statistics_pages : list
        list of strings representing URLs of statistics pages
    """
    pass

def main():
    """Parse commandline arguments & report the addresses of
    linked statistics pages."""
    args = parse_args()
    statistics_pages = get_statistics_pages(args.url)
    for statistics_page in statistics_pages:
        print(statistics_page)

