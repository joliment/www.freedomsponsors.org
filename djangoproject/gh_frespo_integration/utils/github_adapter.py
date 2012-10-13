import httplib2
from urlparse import urlparse
import re
from xml.dom.minidom import parseString
import json


def _fetch_json_objects_from_url(h, url):
    resp, content = h.request(url)
    if(resp.status == 200):
        try:
            return json.loads(content)
        except:
            raise BaseException("Could not parse JSON view from URL: %s" % url)
    else:
        raise BaseException("status %s: %s" % (resp.status, url))


def fetch_repos(username):
    h = httplib2.Http(disable_ssl_certificate_validation=True)
    repos = _fetch_json_objects_from_url(h, "https://api.github.com/users/%s/repos"%username)
    orgs = _fetch_json_objects_from_url(h, "https://api.github.com/users/%s/orgs"%username)
    for org in orgs:
        org_repos = _fetch_json_objects_from_url(h,"https://api.github.com/orgs/%s/repos"%org['login'])
        repos.extend(org_repos)
    return repos