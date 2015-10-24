"""
This file contains a small subset of the tests we will run on your backend submission
"""

import unittest
import os
import testLib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import traceback
import httplib
import sys
import json

class TestTenAnts(testLib.TenAntsTestCase):

    TESTING_EMAIL = 'testing@cs169.com'
    TESTING_PASSWORD = 'hunter2'
    ###
    ### THESE ARE THE ACTUAL TESTS
    ###
    def test_create_account1(self):
        """
        Test creating one account
        """
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

    def test_first_name_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshuahadda Mohhammed Cervantes Dongelo',
                                             'last_name' : 'Perline'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "First Name must be 32 characters or less", respCreate['errors'][0])
 
    def test_last_name_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perlinissimo Mohhammed Cervantes Dongelo'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "Last Name must be 32 characters or less", respCreate['errors'][0])


    def test_password_long_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        badPassword = 'hunter2hunter2hunter2hunter2hunter2hunterhunter2hunter2hunter2hunter2hunter2hunterhunter2hunter2hunter2hunter2hunter2hunter2hunter2hunter'
                                             

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : badPassword,
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "Password must be 128 characters or less", respCreate['errors'][0])

    def test_email_empty_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : '',
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "Email address must be nonempty", respCreate['errors'][0])

    def test_first_name_empty_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : '',
                                             'last_name' : 'Perline'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "First name must be nonempty", respCreate['errors'][0])

    def test_last_name_empty_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : ''
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "Last name must be nonempty", respCreate['errors'][0])

    def test_password_empty_error(self):
        """
        Test adding erroneous info while making account
        """

        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : '',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertFailedResponse(respCreate)
        self.assertEquals( "Password must be nonempty", respCreate['errors'][0])
    
    """
    Housing Post tests
    """

    TESTING_PRICE = 1000
    TESTING_BEDROOMS = 1
    TESTING_BATHROOMS = 1
    TESTING_RATING = 5
    TESTING_LONGITUDE = 10.5
    TESTING_LATITUDE = 10.5
    TESTING_LINE1 = '1234'
    TESTING_LINE2 = 'Durant Avenue'
    TESTING_CITY = 'Berkeley'
    TESTING_ZIP_CODE = '94705'
    TESTING_PROPERTY_NAME = 'Everest Properties'
    TESTING_TITLE = 'Your new home'
    TESTING_LAST_UPDATED = '10'
    TESTING_START_DATE = '2016-01-01'
    TESTING_END_DATE = '2017-01-01'
    TESTING_DESCRIPTION = 'blah blah blah'
    TESTING_NUM_PEOPLE = 4

    def test_price_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : -1,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER, #TODO: TEST WITH COOKIES AND SUCH
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitude' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'state_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        # TODO: CHANGE STATE_DATE YA DINGUS!!!!
        self.assertFailedResponse(respCreate)
        self.assertEquals("Invalid Price", respCreate['errors'][0])


    def test_bedrooms_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : -1,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Invalid Number of Bedrooms", respCreate['errors'][0])

        
    def test_bathrooms_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : -1,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Invalid Number of Bathrooms", respCreate['errors'][0])

    def test_rating_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : -1,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Invalid Rating", respCreate['errors'][0])

    def test_line1_empty_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : '',
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Line1 must be nonempty", respCreate['errors'][0])

    def test_line1_long_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        line1Long = "too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long "

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : line1Long,
                                            'line2' : self.TESTING_LINE2,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Line1 must be fewer than 95 characters", respCreate['errors'][0])
    
    def test_line2_empty_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : '',
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Line2 must be nonempty", respCreate['errors'][0])


    def test_line2_long_error(self):
        respDelete = self.makeRequest("/api/account", method="DELETE")
        self.assertSuccessResponse(respDelete)

        respCreate = self.makeRequest("/api/account", method="POST",
                                    data = { 'email' : self.TESTING_EMAIL,
                                             'password' : 'hunter2',
                                             'first_name' : 'Joshua',
                                             'last_name' : 'Perline'
                                             })
        self.assertSuccessResponse(respCreate)

        loginCreate = self.makeRequest("/api/login", method="POST",
                                        data = { 'email' : self.TESTING_EMAIL,
                                                 'password' : 'hunter2',
                                                })
        self.assertSuccessResponse(loginCreate)

        self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
                                         password=self.TESTING_PASSWORD)

        line2Long = "too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long too long "

        respCreate = self.makeRequest("/api/housing", method="POST",
                                    data = {
                                            'price' : self.TESTING_PRICE,
                                            'bedrooms' : self.TESTING_BEDROOMS,
                                            'bathrooms' : self.TESTING_BATHROOMS,
                                            # 'user' : self.TESTING_USER,
                                            'rating' : self.TESTING_RATING,
                                            'longitude' : self.TESTING_LONGITUDE,
                                            'latitutde' : self.TESTING_LATITUDE,
                                            'line1' : self.TESTING_LINE1,
                                            'line2' : line2Long,
                                            'city' : self.TESTING_CITY,
                                            'zip_code' : self.TESTING_ZIP_CODE,
                                            'property_name' : self.TESTING_PROPERTY_NAME,
                                            'title' : self.TESTING_TITLE,
                                            'last_updated' : self.TESTING_LAST_UPDATED,
                                            'start_date' : self.TESTING_START_DATE,
                                            'end_date' : self.TESTING_END_DATE,
                                            'description' : self.TESTING_DESCRIPTION,
                                            'num_people' : self.TESTING_NUM_PEOPLE
                                            })
        self.assertFailedResponse(respCreate)
        self.assertEquals("Line2 must be fewer than 95 characters", respCreate['errors'][0])

    """
    Housing Search
    """

    TESTING_ORDER_BY = 'last_updated'
    TESTING_MIN_PRICE = 100
    TESTING_MAX_PRICE = 200
    TESTING_NUM_BEDROOMS = 1
    TESTING_NUM_BATHROOMS = 1

    def makeGETRequest(self, url, method="GET", data={ }):
        useAnd = False
        for param in data:
            if data[param] == None:
                continue
            firstString = '?'
            if useAnd:
                firstString = '&'
            else:
                useAnd = True
            paramString = firstString + str(param) + '=' + str(data[param])
            url += paramString
        respData = self.makeRequest(url, method="GET")
        return respData

    def test_search_success(self):
        # respDelete = self.makeRequest("/api/account", method="DELETE")
        # self.assertSuccessResponse(respDelete)

        # respCreate = self.makeRequest("/api/account", method="POST",
        #                             data = { 'email' : self.TESTING_EMAIL,
        #                                      'password' : 'hunter2',
        #                                      'first_name' : 'Joshua',
        #                                      'last_name' : 'Perline'
        #                                      })
        # self.assertSuccessResponse(respCreate)

        # loginCreate = self.makeRequest("/api/login", method="POST",
        #                                 data = { 'email' : self.TESTING_EMAIL,
        #                                          'password' : 'hunter2',
        #                                         })
        # self.assertSuccessResponse(loginCreate)

        # self.TESTING_USER = authenticate(username=self.TESTING_EMAIL,
        #                                  password=self.TESTING_PASSWORD)

        # print 'testing_order_by: ' + self.TESTING_ORDER_BY
        # print 'testing_min_price: ' + str(self.TESTING_MIN_PRICE)
        # print 'testing_max_price: ' + str(self.TESTING_MAX_PRICE)
        # print 'testing_num_bedrooms: ' + str(self.TESTING_NUM_BEDROOMS)
        # print 'testing_num_bathrooms: ' + str(self.TESTING_NUM_BATHROOMS)
        respCreate = self.makeGETRequest("/api/housing", method='GET', data={'order_by' : self.TESTING_ORDER_BY,
                                            'min_price' : self.TESTING_MIN_PRICE,
                                            'max_price' : self.TESTING_MAX_PRICE,
                                            'num_bedrooms' : self.TESTING_NUM_BEDROOMS,
                                            'num_bathrooms' : self.TESTING_NUM_BATHROOMS
                                        })
        self.assertSuccessResponse(respCreate)

