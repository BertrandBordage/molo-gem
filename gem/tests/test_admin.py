# -*- coding: utf-8 -*-
from datetime import date

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client
from molo.core.tests.base import MoloTestCaseMixin

from molo.profiles.models import UserProfile
from gem.admin import GemUserAdmin, download_as_csv_gem


class TestFrontendUsersAdminView(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.mk_main()
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='0000',
            is_staff=False)

        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='admin@example.com',
            password='0000',
            is_staff=True)

        self.client = Client()
        self.client.login(username='superuser', password='0000')

    def test_staff_users_are_not_shown(self):
        response = self.client.get(
            '/admin/modeladmin/auth/user/'
        )

        self.assertContains(response, self.user.username)
        self.assertNotContains(response, self.superuser.email)

    def test_export_csv(self):
        profile = self.user.profile
        profile.alias = 'The Alias'
        profile.date_of_birth = date(1985, 1, 1)
        profile.mobile_number = '+27784667723'
        profile.save()
        gem_profile = self.user.gem_profile
        gem_profile.gender = 'f'
        gem_profile.save()

        response = self.client.post('/admin/modeladmin/auth/user/')
        expected_output = (
            'username,alias,first_name,last_name,date_of_birth,'
            'email,mobile_number,is_active,date_joined,last_login,gender\r\n'
            'tester,The Alias,,,1985-01-01,tester@example.com,+27784667723'
        )

        self.assertContains(response, expected_output)
        self.assertContains(response, 'female')


class ModelsTestCase(TestCase, MoloTestCaseMixin):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='tester')
        self.mk_main()

    def test_download_csv(self):
        profile = self.user.profile
        profile.alias = 'The Alias'
        profile.mobile_number = '+27784667723'
        profile.save()
        date = str(self.user.date_joined.strftime("%Y-%m-%d %H:%M"))
        gem_profile = self.user.gem_profile
        gem_profile.gender = 'f'
        gem_profile.date_of_birth = date
        gem_profile.save()
        response = download_as_csv_gem(GemUserAdmin(UserProfile, self.site),
                                       None,
                                       User.objects.all())
        expected_output = (
            'Content-Type: text/csv\r\nContent-Disposition: attachment;filen'
            'ame=export.csv\r\n\r\nusername,email,first_name,last_name,is_sta'
            'ff,date_joined,alias,mobile_number,date_of_birth,gender\r\nte'
            'ster,tester@example.com,,,False,' + date + ',The Alias,+277'
            '84667723,,f\r\n')
        self.assertEquals(str(response), expected_output)

    def test_download_csv_no_gem_profile(self):
        gem_profile = self.user.gem_profile
        gem_profile.delete()
        response = download_as_csv_gem(GemUserAdmin(UserProfile, self.site),
                                       None,
                                       User.objects.all())
        expected_output = (
            'Content-Type: text/csv\r\nContent-Disposition: attachment;file'
            'name=export.csv\r\n\r\nusername,email,first_name,last_name,is_st'
            'aff,date_joined,alias,mobile_number,date_of_birth,gender\r\n')
        self.assertEquals(str(response), expected_output)
