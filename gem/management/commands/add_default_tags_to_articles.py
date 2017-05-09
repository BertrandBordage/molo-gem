from __future__ import absolute_import, unicode_literals

import csv
from django.core.management.base import BaseCommand
from molo.core.models import (
    Languages, Tag, ArticlePage, ArticlePageTags, Main, SectionIndexPage,
    TagIndexPage)


class Command(BaseCommand):
    def handle(self, **options):
        mains = Main.objects.all()
        articles = {}
        with open('articles_tags.csv') as articles_tags:
            reader = csv.reader(articles_tags)
            if mains:
                for row in reader:
                    key = row[0]
                    articles[key] = row[1:]

        for main in mains:
            section_index = SectionIndexPage.objects.child_of(main).first()
            tag_index = TagIndexPage.objects.child_of(main).first()
            main_lang = Languages.for_site(main.get_site()).languages.filter(
                is_active=True, is_main_language=True).first()
            if section_index and tag_index and main_lang:
                if main_lang.locale == "en":
                    for article_slug in articles:
                        article = ArticlePage.objects.descendant_of(
                            section_index).filter(slug=article_slug).first()
                        if article:
                            for tag_title in articles.get(article_slug):
                                tag = Tag.objects.child_of(
                                    tag_index).filter(title=tag_title).first()
                                if tag:
                                    if not article.nav_tags.filter(
                                            tag__title=tag):
                                        article_page_tag = ArticlePageTags(
                                            page=article, tag=tag)
                                        article_page_tag.save()
                                    else:
                                        self.stdout.write(self.style.WARNING(
                                            'Tag "%s" has been already asigned'
                                            ' to "%s" in "%s"'
                                            % (tag, article, main)))
                                else:
                                    self.stdout.write(self.style.NOTICE(
                                        'Tag "%s" does not exist in "%s"'
                                        % (tag_title, main)))
                        else:
                            self.stdout.write(self.style.ERROR(
                                'Article "%s" does not exist in "%s"'
                                % (article_slug, main.get_site())))
                else:
                    self.stdout.write(self.style.NOTICE(
                        'Main language of "%s" is not English.'
                        ' The main language is "%s"'
                        % (main.get_site(), main_lang)))
            else:
                if not section_index:
                    self.stdout.write(self.style.NOTICE(
                        'Section Index Page does not exist in "%s"' % main))
                if not tag_index:
                    self.stdout.write(self.style.NOTICE(
                        'Tag Index Page does not exist in "%s"' % main))
                if not main_lang:
                    self.stdout.write(self.style.NOTICE(
                        'Main language does not exist in "%s"' % main))
