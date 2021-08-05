import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json

from estnltk import Text
from estnltk import synthesize

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({}).encode())
        return

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body.decode('utf-8'))

        self.send_response(200)
        self.end_headers()

        output = self.__make_output(path=self.path, data=data)

        self.wfile.write(json.dumps(output).encode())
        return

    def __make_output(self, path, data):
        text = Text(data['text'])
        output = {}
        if path == '/postags':
            output = self.__make_postags(text)
        elif path == '/tag-analysis':
            output = self.__make_tag_analysis(text)
        elif path == '/analysis':
            output = self.__make_analysis(text)
        elif path == '/forms':
            output = self.__make_forms(text)
        elif path == '/synthesize':
            output = self.__make_synthesis(data)
        else:
            pass
        return output

    def __make_postags(self, text):
        postags_list = list(text.get.word_texts.postags.postag_descriptions.as_zip)
        output = []
        for word, tag, desc in postags_list:
            output.append({'word': word, 'tag': tag, 'desc': desc})
        return {'postags': output}

    def __make_tag_analysis(self, text):
        return text.tag_analysis()

    def __make_analysis(self, text):
        return text.analysis

    def __make_forms(self, text):
        forms_list = list(text.get.word_texts.forms.descriptions.as_zip)
        output = []
        for word, form, desc in forms_list:
            output.append({'word': word, 'form': form, 'desc': desc})
        return {'forms': output}

    def __make_synthesis(self, data):
        output = synthesize(data['word'], form=data['form'], partofspeech=data['pos'])
        return {'synthesized': output}


if __name__ == '__main__':
    server = HTTPServer((os.getenv('ADDRESS'), int(os.getenv('PORT'))), RequestHandler)
    server.serve_forever()