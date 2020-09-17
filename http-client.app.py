# -*- coding: utf-8 -*-
import sys
import http
from http import client


TRUE_STR_LIST = ['true', 'on']


HTTP_METHOD_GET = 'GET'
HTTP_METHOD_HEAD = 'HEAD'
HTTP_METHOD_POST = 'POST'
HTTP_METHOD_PUT = 'PUT'
HTTP_METHOD_DELETE = 'DELETE'
HTTP_METHOD_CONNECT = 'CONNECT'
HTTP_METHOD_OPTIONS = 'OPTIONS'
HTTP_METHOD_TRACE = 'TRACE'
HTTP_METHOD_PATCH = 'PATCH'


enable_ssl = False
url = ''
port = 80
timeout = 10
url_path = ''
method = HTTP_METHOD_GET
headers_dic = {}
body_type = 'text'


def print_log(tag, msg):
    sys.stdout.write(f"[http-client.{tag}] {msg}\n")
    sys.stdout.flush()


def on_set(k, v):
    if k == "enable_ssl":
        global enable_ssl
        enable_ssl = True if v.lower() in TRUE_STR_LIST else False
    elif k == "url":
        global url
        url = v
    elif k == "port":
        global port
        port = int(v)
    elif k == "timeout":
        global timeout
        timeout = int(v)
    elif k == "url_path":
        global url_path
        url_path = v
    elif k == "method":
        global method
        method = v
    elif k == "headers":
        global headers_dic
        headers_dic = parse_header(v, '&')
    elif k == "body_type":
        global body_type
        body_type = v


def on_get(k):
    if k == "enable_ssl":
        return str(enable_ssl)
    elif k == "url":
        return url
    elif k == "port":
        return str(port)
    elif k == "timeout":
        return str(timeout)
    elif k == "url_path":
        return url_path
    elif k == "method":
        return method
    elif k == "headers":
        return convert_header_to_str(headers_dic)
    elif k == "body_type":
        return body_type


def on_run(input_body):
    connection = get_connection(enable_ssl, url, port, timeout)

    request(connection, method, url_path, body_type, input_body, headers_dic)

    response = connection.getresponse()

    print_log('on_run', f"status : {response.status}, body: {response.read()}")

    return {}


def get_connection(ssl, url, port, timeout):
    if ssl:
        return client.HTTPSConnection(url, port, timeout=timeout)
    else:
        return client.HTTPConnection(url, port, timeout=timeout)


def get_body(type_body, body):
    if type_body == 'text':
        return ''.join([chr(x) for x in body])
    else:
        return ''


def request(connection, method, path, body_t, body, headers):
    if method in [HTTP_METHOD_GET, HTTP_METHOD_HEAD, HTTP_METHOD_DELETE, HTTP_METHOD_TRACE]:
        body = None

    if body_t == 'text':
        b = ''.join([chr(x) for x in body])
    else:
        b = body.tobytes()

    # print_log('request', f'm: {method}, p: {path}, b: {b}, h: {headers}')
    connection.request(method, path, body=b, headers=headers)


def parse_header(header_str, delimiter):
    HEADER_NAME_DELIMITER = ':'
    headers = header_str.split(delimiter)
    headers = headers.split(HEADER_NAME_DELIMITER)
    header_dic = {}
    for i in range(0, len(headers), 2):
        header_dic[headers[i]] = headers[i + 1]
    return header_dic


def convert_header_to_str(header_dic):
    headers_str = ''
    for k, v in header_dic:
        headers_str += k + ':' + v + '&'
    headers_str = headers_str[:-1]
    return headers_str


if __name__ == '__main__':
    pass
