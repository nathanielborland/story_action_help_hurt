from bs4 import BeautifulSoup
from bs4 import element

def get_episode_summaries(filepath:str) -> list[str]:
    with open(filepath, 'r') as f:
        raw_html = f.read()
    soup = BeautifulSoup(raw_html, 'html.parser')

    summary_divs = soup.find_all('div', attrs={'class': 'shortSummaryText'}, recursive=True)
    summaries = []
    for div in summary_divs:
        summary = ''
        for content in div.contents:
            if isinstance(content, element.Tag):
                if content.name == 'table' or content.name == 'style' or content.name == 'link':
                    continue
                if not (content.name == 'a' or content.name == 'b' or content.name == 'i'):
                    print(f'found unexpected tag: {content.name}')
            summary += content.get_text()
        summaries.append(summary.strip())
    return summaries

header_classes = ['mw-heading', 'mw-heading2']
def get_plot_summary(filepath:str) -> str:
    with open(filepath, 'r') as f:
        raw_html = f.read()
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    summary = ''
    plot_h2 = soup.find('h2', attrs={'id': 'Plot'}, recursive=True)
    if plot_h2 is not None:
        cur_tag = plot_h2.parent.find_next_sibling()
        while True:
            if cur_tag is None or (cur_tag.name == 'div' and cur_tag.has_attr('class') and cur_tag.attrs['class'] == header_classes):
                break
            if cur_tag.name == 'p':
                summary += cur_tag.get_text()
            cur_tag = cur_tag.find_next_sibling()
    return summary

# all_summaries = get_episode_summaries('wiki_html/List of The 100 episodes - Wikipedia.html')
# for single_summary in all_summaries:
#     input()
#     print(single_summary)

# movie_summary = get_plot_summary('wiki_html/Aladdin (1992 Disney film) - Wikipedia.html')
# print(movie_summary)