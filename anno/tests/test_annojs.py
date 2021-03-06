import json
import pytest
import os

from django.urls import reverse
from django.test import Client

from anno.anno_defaults import ANNOTATORJS_FORMAT
from anno.anno_defaults import CATCH_RESPONSE_FORMAT_HTTPHEADER
from anno.crud import CRUD
from anno.json_models import AnnoJS
from anno.json_models import Catcha
from anno.models import Anno
from consumer.models import Consumer

from .conftest import make_encoded_token
from .conftest import make_jwt_payload


@pytest.mark.skip('debugging fixture')
@pytest.mark.usefixtures('wa_list')
def x_test_fixture_wa_list(wa_list):
    print(json.dumps(wa_list, sort_keys=True, indent=2))
    assert wa_list == 'blah'


@pytest.mark.skip('debugging fixture')
@pytest.mark.usefixtures('js_list')
def x_test_fixture_js_list(js_list):
    print(json.dumps(js_list, sort_keys=True, indent=2))
    assert js_list == 'blah'


@pytest.mark.usefixtures('js_list')
@pytest.mark.django_db
def test_to_annotatorjs(js_list):
    for js in js_list:
        catcha = AnnoJS.convert_to_catcha(js)
        anno = CRUD.create_anno(catcha, catcha['creator']['name'])
        js_back = AnnoJS.convert_from_anno(anno)
        assert AnnoJS.are_similar(js, js_back)


def readfile_into_jsonobj(filepath):
    with open(filepath, 'r') as f:
        context = f.read()
    return json.loads(context)


