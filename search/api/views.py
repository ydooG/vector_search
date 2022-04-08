import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from search.utils import get_search_results


@method_decorator(csrf_exempt, name='dispatch')
class MakeSearchView(View):
    http_method_names = ['post']

    def post(self, request):
        data = json.dumps(dict(results=get_search_results(self.request.POST['q'])))
        return HttpResponse(data, status=200, content_type='application/json')
