from django.contrib import admin
from .models import *

admin.site.site_title = 'Clarusway Title'
admin.site.site_header = 'Clarusway Header'
admin.site.index_title = 'Clarusway Index Page'

# -----------------------------------------------------
# ProductModelAdmin

# Ürünlerin yorumlarını ürün-detay sayfasında göster:
class ReviewInline(admin.TabularInline):  # Alternatif: StackedInline (farklı görünüm aynı iş)
    model = Review # Model
    extra = 1 # Yeni ekleme için ekstra boş alan
    classes = ['collapse'] # Görüntülme tipi (default: tanımsız)


class ProductModelAdmin(admin.ModelAdmin):
    # Tablo sutunları:
    list_display = ['id', 'name', 'is_in_stock', 'create_date', 'update_date']
    # Tablo üzerinde güncelleyebilme:
    list_editable = ['is_in_stock']
    # Kayda gitmek için linkleme:
    list_display_links = ['id', 'name']
    # Filtreleme (arama değil):
    list_filter = ['is_in_stock', 'create_date', 'update_date']
    # Arama:
    search_fields = ['id', 'name']
    # Default Sıralama:
    ordering = ['-create_date', '-id']
    # Sayfa başına kayıt sayısı:
    list_per_page = 20
    # Arama bilgilendirme yazısı: 
    search_help_text = 'Arama Yapmak için burayı kullanabilirsiniz.'
    # Otomatik kaıyıt oluştur:
    prepopulated_fields = {'slug' : ['name']}
    # Tarihe göre filtreleme başlığı:
    date_hierarchy = 'create_date'
    # Form liste görüntüleme
    fields = (
        ('name', 'is_in_stock'),
        ('slug'),
        ('description')
    )
    '''
    # Detaylı form liste görüntüleme
    fieldsets = (
        (
            'General Settings', {
                "classes": ("wide",),
                "fields": (
                    ('name', 'slug'),
                    "is_in_stock"
                ),
            }
        ),
        (
            'Optionals Settings', {
                "classes": ("collapse",),
                "fields": ("description",),
                'description': "You can use this section for optionals settings"
            }
        ),
    )
    '''
    inlines = [ReviewInline]

    def set_stock_in(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f'{count} adet "Stokta Var" olarak işaretlendi.')
    

    def set_stock_out(self, request, queryset):
        count = queryset.update(is_in_stock=False)
        self.message_user(request, f'{count} adet "Stokta Yok" olarak işaretlendi.')

    actions = ('set_stock_in', 'set_stock_out')
    set_stock_in.short_description = 'İşaretli ürünleri stokta VAR olarak güncelle'
    set_stock_out.short_description = 'İşaretli ürünleri stokta YOK olarak güncelle'

    # Kaç gün önce eklendi:
    def added_days_ago(self, object):
        from django.utils import timezone
        different = timezone.now() - object.create_date
        return different.days
    
    # list_display = ['id', 'name', 'is_in_stock', 'added_days_ago', 'create_date', 'update_date']
    list_display += ['added_days_ago']

    # Kaçtane yorum var:
    def how_many_reviews(self, object):
        count = object.reviews.count()
        return count

    list_display += ['how_many_reviews']

admin.site.register(Product, ProductModelAdmin)

# -----------------------------------------------------
# ReviewModelAdmin

class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    # raw_id_fields = ('product',) 

admin.site.register(Review, ReviewModelAdmin)