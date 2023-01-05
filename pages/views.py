from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from . models import *
from django.template import loader


def showpage(request, pageslug):
    mpage = get_object_or_404(Page, page_slug=pageslug)

    template = loader.get_template('pages/page.html')
    context = {
        'page': mpage,
    }
    return HttpResponse( template.render(context, request) )
