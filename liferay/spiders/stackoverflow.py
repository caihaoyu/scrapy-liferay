from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
import dateutil.parser
from liferay.items import Question, Comment, Answer, Author


class Stackoverflow(CrawlSpider):
    allowed_domains = ["stackoverflow.com"]
    name = 'liferay'

    domain = 'http://stackoverflow.com/'
    list_type = 'json'
    first_list_url = ('http://stackoverflow.com/search?pagesize=50'
                      '&q=liferay')
    page_url = ('http://stackoverflow.com/search?page=%s'
                '&q=liferay&pagesize=50')
    page_sum_xpath = '//div[@class="pager fl"]/a[5]/@href'
    list_items_xpath = '//div[@class="question-summary search-result"]'
    item_url_xpath = '//div[@class="result-link"]/span/a/@href'
    item_date_xpath = '//span[@class="relativetime"]/@title'
    item_title_xpath = '//div[@class="result-link"]/span/a/@title'
    item_tags_xpath = '//a[@class="post-tag"]/text()'
    item_answer_count_xpath = '//div[@class="status answered"]/strong/text()'
    item_votes_xpath = '//span[@class="vote-count-post "]/strong/text()'
    item_author_name_xpath = '//div[@class="user-details"]/a/text()'
    item_author_url_xpath = '//div[@class="user-details"]/a/@href'
    content_xpath = '//div[@class="post-text"]'
    question_id_xpath = '//div[@class="question"]/@data-questionid'
    list_comments_xpath = '//td[@class="comment-text"]'
    comment_context_xpath = '//span[@class="comment-copy"]/text()'
    comment_time_xpath = '//span[@class="relativetime-clean"]/text()'
    comment_id_xpath = '//a[@class="comment-link"]/@href'
    author_xpath_dict = {'comment': '//a[@class="comment-user"]/%s',
                         'q&a': '//div[@class="user-details"]/a/', }

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'DNSCACHE_ENABLED': True,
    }

    def get_author(self, selector, type_):
        xpath = self.author_xpath_dict.get(type_, None)
        if xpath:
            name = selector.xpath(xpath % ('text()')).extract_first().strip()
            url = (self.domain +
                   selector.xpath(xpath % ('@href')).extract_first().strip())
            return Author(name=name, url=url)
        else:
            return {}

    def start_requests(self):
        url = self.first_list_url
        yield Request(url, dont_filter=True, callback=self.parse_first_list)

    def parse_first_list(self, response):
        i = 1
        page_sum = self.get_page_sum(response)
        print(page_sum)
        while i <= page_sum:
            url = self.get_page_url(response, i)
            yield Request(url, dont_filter=True, callback=self.parse_list)
            i += 1

    def get_page_url(self, response, index):
        return self.page_url % (str(index))

    def parse_list(self, response):
        # import pdb
        # pdb.set_trace()
        selector = Selector(response)
        items = selector.xpath(self.list_items_xpath).extract()
        for item in items:
            s = Selector(text=item)
            question = Question()
            link = self.domain + s.xpath(self.item_url_xpath).extract_first()
            if link:
                question['url'] = link
                if self.item_date_xpath:
                    question['publish_time'] = dateutil.parser.parse(
                        s.xpath(self.item_date_xpath).extract_first())
                question['title'] = s.xpath(
                    self.item_title_xpath).extract_first().strip()
                question['tags'] = s.xpath(self.item_tags_xpath).extract()
                answer_count = s.xpath(
                    self.item_answer_count_xpath).extract_first() or 0
                question['answer_count'] = int(answer_count)
                votes = ''.join(s.xpath(
                    self.item_votes_xpath).extract()) or 0
                question['votes'] = int(votes)
                # print(question)
                yield Request(link, meta={'question': question},
                              dont_filter=True, callback=self.parse_question)

    def get_page_sum(self, response):
        return 2
        selector = Selector(response)
        page_sum_url = selector.xpath(self.page_sum_xpath).extract_first()
        page_sum = ''.join(list(filter(str.isdigit, str(page_sum_url))))
        # print(page_sum)
        return int(page_sum)

    def parse_question(self, response):
        selector = Selector(response)
        question = response.meta['question']
        q_id = selector.xpath(self.question_id_xpath).extract_first().strip()
        question['_id'] = q_id
        context = ''.join(selector.xpath(self.content_xpath).extract())
        question['context'] = context
        # print(question)
        yield question
        comments = self.parse_comment(
            response=response, ctype='question', type_id=q_id)
        for c in comments:
            yield c

    def parse_comment(self, response, ctype, type_id):
        selector = Selector(response)
        items = selector.xpath(self.list_comments_xpath).extract()
        result = []
        for item in items:
            s = Selector(text=item)
            comment = Comment(
            c_id =
            comment['type'] = ctype
            comment['type_id'] = type_id
            comment['context'] = ''.join(
                s.xpath(self.comment_context_xpath).extract())
            publish_time = s.xpath(self.comment_time_xpath).extract_first()
            comment['publish_time'] = dateutil.parser.parse(publish_time)
            comment['author'] = self.get_author(selector=s, type_='comment')
            # yield comment
            result.append(comment)
        return result
