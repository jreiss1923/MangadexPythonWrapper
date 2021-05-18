import requests
import json
import time

class MangadexAPI:

    def __init__(self, username, password):

        data = json.dumps({
                        "username":str(username),
                        "password":str(password)
                     })

        response = requests.post("https://api.mangadex.org/auth/login", data=data)
        self.session_token = json.loads(response.text)['token']['session']
        self.refresh_token = json.loads(response.text)['token']['refresh']
        self.json_session_token = {
            "authorization": "Bearer " + self.session_token
        }
        print("You are now logged into the Mangadex API.")

    def check_token(self):
        response = json.loads(requests.get("https://api.mangadex.org/auth/check", headers=self.json_session_token).text)
        if response['isAuthenticated']:
            print("You are currently authenticated in the Mangadex API.")
        else:
            print("You are not currently authenticated in the Mangadex API.")

    def logout(self):
        response = json.loads(requests.post("https://api.mangadex.org/auth/logout", headers=self.json_session_token).text)
        if response['result'] == "ok":
            print("You have been logged out of Mangadex.")
        else:
            print("Something went wrong! You are not logged out.")

    def refresh(self):

        data = json.dumps({
            "token": self.refresh_token
        })

        response = json.loads(requests.post("https://api.mangadex.org/auth/refresh", headers=self.json_session_token, data=data).text)
        if response['result'] == "ok":
            self.session_token = response['token']['session']
            self.refresh_token = response['token']['refresh']
            print("Your tokens have been refreshed and updated.")
        else:
            print("Something went wrong! Your tokens have not been refreshed.")

    def get_manga_list(self, limit=10, offset=0, title=None, authors=None, artists=None, year=None, includedTags=None, includedTagsMode=None, excludedTags=None, excludedTagsMode=None, status=None, originalLanguage=None, publicationDemographic=None, ids=None, contentRating=None, createdAtSince=None, updatedAtSince=None, order=None):

        params = {
            "limit": limit,
            "offset": offset,
            "title": title,
            "authors": authors,
            "artists": artists,
            "year": year,
            "includedTags": includedTags,
            "includedTagsMode": includedTagsMode,
            "excludedTags": excludedTags,
            "excludedTagsMode": excludedTagsMode,
            "status": status,
            "originalLanguage": originalLanguage,
            "publicationDemographic": publicationDemographic,
            "ids": ids,
            "contentRating": contentRating,
            "createdAtSince": createdAtSince,
            "updatedAtSince": updatedAtSince,
            "order": order
        }

        response = json.loads(requests.get("https://api.mangadex.org/manga", headers=self.json_session_token, params=params).text)
        if response['results'][0]['result'] == "ok":
            return response

    def ping(self):
        start = time.time()
        response = requests.get("https://api.mangadex.org/ping", headers=self.json_session_token).text
        end = time.time()
        print(response + " - That took " + str(round((end-start)*1000, 2)) + " ms.")

    def logged_user_details(self):
        response = json.loads(requests.get("https://api.mangadex.org/user/me", headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def get_user(self, user_id):

        url = "https://api.mangadex.org/user/" + str(user_id)
        response = json.loads(requests.get(url, headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def logged_user_followed_groups(self, limit=10, offset=0):

        params = {
            "limit": limit,
            "offset": offset
        }

        response = json.loads(requests.get("https://api.mangadex.org/user/follows/group", headers=self.json_session_token, params=params).text)
        if "results" in response:
            return response

    def logged_user_followed_user_list(self, limit=10, offset=0):

        params = {
            "limit": limit,
            "offset": offset
        }

        response = json.loads(requests.get("https://api.mangadex.org/user/follows/user", headers=self.json_session_token, params=params).text)
        if "results" in response:
            return response

    def logged_user_followed_manga_list(self, limit=10, offset=0):

        params = {
            "limit": limit,
            "offset": offset
        }

        response = json.loads(requests.get("https://api.mangadex.org/user/follows/manga", headers=self.json_session_token, params=params).text)
        if "results" in response:
            return response

    def legacy_id_mapping(self, type=None, ids=None):

        data = {
            "type": type,
            "ids": ids
        }

        response = json.loads(requests.post("https://api.mangadex.org/legacy/mapping", headers=self.json_session_token, data=data).text)
        if "results" in response:
            return response

    def view_manga(self, id):

        url = "https://api.mangadex.org/manga/" + str(id)

        response = json.loads(requests.get(url, headers=self.json_session_token).text)
        if "result" in response:
            return response

    def get_manga_feed(self, id, limit=10, offset=0, locales=None, createdAtSince=None, updatedAtSince=None, publishAtSince=None, order=None):

        url = "https://api.mangadex.org/manga/" + str(id) + "/feed"

        params = {
            "limit": limit,
            "offset": offset,
            "locales": locales,
            "createdAtSince": createdAtSince,
            "updatedAtSince": updatedAtSince,
            "publishAtSince": publishAtSince,
            "order": order
        }

        response = json.loads(requests.get(url, headers=self.json_session_token, params=params).text)
        if "results" in response:
            return response

    def manga_read_markers(self, id):

        url = "https://api.mangadex.org/manga/" + str(id) + "/read"

        response = json.loads(requests.get(url, headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def get_random_manga(self):

        response = json.loads(requests.get("https://api.mangadex.org/manga/random", headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def tag_list(self):

        response = json.loads(requests.get("https://api.mangadex.org/manga/tag", headers=self.json_session_token).text)
        if response[0]['result'] == "ok":
            return response


    def update_manga_reading_status(self, id, status):

        data = json.dumps({
            "status": status
        })

        url = "https://api.mangadex.org/manga/" + str(id) + "/status"

        response = json.loads(requests.post(url, headers=self.json_session_token, data=data).text)
        if response['result'] == "ok":
            return response

    def follow_manga(self, id):

        url = "https://api.mangadex.org/manga/" + str(id) + "/follow"

        response = json.loads(requests.post(url, headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def unfollow_manga(self, id):

        url = "https://api.mangadex.org/manga/" + str(id) + "/follow"

        response = json.loads(requests.delete(url, headers=self.json_session_token).text)
        if response['result'] == "ok":
            return response

    def author_list(self, limit=10, offset=0, ids=None, name=None):

        params = {
            "limit": limit,
            "offset": offset,
            "ids": ids,
            "name": name
        }

        response = json.loads(requests.get("https://api.mangadex.org/author", headers=self.json_session_token, params=params).text)
        if "results" in response:
            return response

    def get_author(self, id):

        url = "https://api.mangadex.org/author/" + str(id)

        response = json.loads(requests.get(url, headers=self.json_session_token).text)
        print(response)
        if response['result'] == "ok":
            return response
