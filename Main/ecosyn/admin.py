from django.contrib import admin

from .models import Sujet, Secteur, Page, Section, Picture, PictureDim
from .models import Icon, Lien, Illustration, GraphNode, GraphArrow

class EventAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Sujets":1,
            "Secteurs":2,
            "Pages":3,
            "Liens":4,
            "Illustrations":5,
            "Pictures":6,
            "Picture dims":7,
            "Icons":8,
        }
        app_dict = self._build_app_dict(request)
        # a.sort(key=lambda x: b.index(x[0]))
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

class SectionInLine(admin.StackedInline):
    model = Section
    extra = 2
    list_filter = ["order"]
    
class SujetSection(SectionInLine):
    exclude = ("secteur","page")

class SecteurSection(SectionInLine):
    exclude = ("sujet","page")
    
class PageSection(SectionInLine):
    exclude = ("secteur","sujet")
    
class SujetAdmin(admin.ModelAdmin):
    inlines = [SujetSection]
    list_filter = ["secteur"]
    list_display = ["name","secteur"]

class SecteurAdmin(admin.ModelAdmin):
    inlines = [SecteurSection]
    list_filter = ["name"]
    list_display = ["name"]

class PageAdmin(admin.ModelAdmin):
    inlines = [PageSection]
    list_display = ('name','id')
    list_filter = ["date_created"]

class DimsAdmin(admin.ModelAdmin):
    model = PictureDim
    
class PictureAdmin(admin.ModelAdmin):
    model = Picture
    
class IconAdmin(admin.ModelAdmin):
    model = Icon
    
class LienAdmin(admin.ModelAdmin):
    model = Lien
    list_display=["cause","consequence"]
    list_filter =["cause","consequence"]
  
class GraphNodeInLine(admin.StackedInline):
    model = GraphNode
    fk_name = "illustration"
    extra = 0

class GraphArrowInLine(admin.StackedInline):
    model = GraphArrow
    fk_name = "illustration"
    extra = 0
    
class IllustrationAdmin(admin.ModelAdmin):
    model = Illustration
    inlines = [GraphNodeInLine,GraphArrowInLine]
    list_display = ('name','id')
    list_filter = ["section__page", "section__secteur","section__sujet","section"]
    
admin.site = EventAdminSite()
    
admin.site.register(Sujet, SujetAdmin)
admin.site.register(Secteur, SecteurAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(PictureDim, DimsAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Icon,IconAdmin)
admin.site.register(Lien, LienAdmin)
admin.site.register(Illustration,IllustrationAdmin)
